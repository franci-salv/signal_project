#Noise-Resilient Signal Encryption
#Idea: Add a secret message to specific DFT frequencies while adding random noise to the rest. The message can be decrypted only if the right key (e.g. frequency index map) is known.

#Application: Can simulate sending a "hidden" message in a noisy channel.

import numpy as np
import hashlib
import random
import matplotlib.pyplot as plt

# === Helper Functions ===
def message_to_bits(message):#as name suggests it changes the messages to bits
    return ''.join(format(ord(char), '08b') for char in message)

def bits_to_message(bits):#converts binary to letters (chr() command converts ASCII back to letters)
    chars = [chr(int(bits[i:i+8], 2)) for i in range(0, len(bits), 8)]
    return ''.join(chars)

def get_scrambled_indices(password, num_indices, signal_length, reference_fft):
    hash_bytes = hashlib.sha256(password.encode()).digest()
    seed = int.from_bytes(hash_bytes, 'big')
    rng = random.Random(seed)

    magnitudes = np.abs(reference_fft)
    threshold = np.max(magnitudes) * 0.001
    valid_indices = [i for i in range(10, signal_length // 2) if magnitudes[i] > threshold]

    if len(valid_indices) < num_indices:
        print(f"[!] Only {len(valid_indices)} bins available. Reducing message size from {num_indices} to {len(valid_indices)}.")
        num_indices = len(valid_indices)

    rng.shuffle(valid_indices)
    return valid_indices[:num_indices]


def embed_bits_in_signal(signal, bits, password):
    fft_signal = np.fft.fft(signal)
    indices = get_scrambled_indices(password, len(bits), len(fft_signal), reference_fft)
    #this is the actual message being converted into the signal so now the signal contains the message

    for i, bit in enumerate(bits):
        original = fft_signal[indices[i]]
        if bit == '1':
            fft_signal[indices[i]] *= 3.0
        else:
            fft_signal[indices[i]] *= 0.3
        modified = fft_signal[indices[i]]
        print(f"Index {indices[i]:3d}: bit={bit}  before={abs(original):.4f}  after={abs(modified):.4f}")
    
    return np.fft.ifft(fft_signal).real


def extract_bits_from_signal(signal, password, bit_count, reference_fft):
    #this function is supposed to extract the bits back from that signal
    fft_signal = np.fft.fft(signal)
    indices = get_scrambled_indices(password, bit_count, len(fft_signal), reference_fft)

    bits = ''
    for idx in indices:
        ref_mag = abs(reference_fft[idx])
        received_mag = abs(fft_signal[idx])
        bits += '1' if received_mag > ref_mag else '0'
    return bits



# === Main Test ===
if __name__ == "__main__":
    Fs = 1024  # Sampling frequency
    t = np.arange(0, 1, 1/Fs)
    # Generate a broad spectrum signal with energy across many frequencies
    base_signal = np.random.normal(0, 1, len(t))
    base_signal = np.convolve(base_signal, np.ones(10)/10, mode='same')  # Smooth it a bit
    base_signal /= np.max(np.abs(base_signal))  # Normalize

    message = "Mihai_is_hiding_in_the_closet"
    password = "my_secret_password"

    binary = message_to_bits(message)
    reference_fft = np.fft.fft(base_signal)
    encoded_signal = embed_bits_in_signal(base_signal.copy(), binary, password)
    

    # Add optional Gaussian noise
    noisy_signal = encoded_signal + np.random.normal(0, 0.005, len(encoded_signal))  # less noise


    # Decode
    extracted_bits = extract_bits_from_signal(noisy_signal, password, len(binary), reference_fft)
    decoded_message = bits_to_message(extracted_bits)

    fft_before = np.fft.fft(base_signal)
    fft_after = np.fft.fft(encoded_signal)

    plt.figure(figsize=(10, 4))
    plt.plot(abs(fft_before), label="Before")
    plt.plot(abs(fft_after), label="After")
    plt.title("FFT Magnitude Before vs After Embedding")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    fft_signal = np.fft.fft(base_signal)
    fft_signal[100] *= 3.0
    test_signal = np.fft.ifft(fft_signal).real
    print("Mag diff @ 100:", abs(np.fft.fft(test_signal)[100]) - abs(np.fft.fft(base_signal)[100]))

    # Results
    print("Original Message: ", message)
    print("Decoded Message:  ", decoded_message)
    print("Message length in bits:", len(binary))  # Should be 5 * 8 = 40
    print("Extracted bits length:", len(extracted_bits))  # Must be 40 too
    for i, (a, b) in enumerate(zip(binary, extracted_bits)):
        print(f"{i:02d}: original={a}  extracted={b}  {'✔️' if a == b else '❌'}")
    print("Ref mag @ idx 50:", abs(reference_fft[50]))
    print("Enc mag @ idx 50:", abs(np.fft.fft(encoded_signal)[50]))
    print("Indices used:", get_scrambled_indices(password, len(binary), len(base_signal), reference_fft))
    print("Bit Accuracy:     ", sum([a == b for a, b in zip(binary, extracted_bits)]) / len(binary) * 100, "%")

    # Plot
    plt.figure(figsize=(10, 5))
    plt.plot(base_signal, label="Original Signal")
    plt.plot(encoded_signal, label="Encoded Signal")
    plt.plot(noisy_signal, label="Noisy Signal", alpha=0.6)

    plt.legend()
    plt.title("Signal Encryption & Decryption (DFT-based)")
    plt.xlabel("Sample Index")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


    plt.plot(abs(reference_fft), label="Reference FFT")
    plt.plot(abs(np.fft.fft(noisy_signal)), label="Noisy FFT")
    plt.legend()
    plt.title("FFT Magnitudes")
    plt.grid(True)
    plt.show()
