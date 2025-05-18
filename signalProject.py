#Noise-Resilient Signal Encryption
#Idea: Add a secret message to specific DFT frequencies while adding random noise to the rest. The message can be decrypted only if the right key (e.g. frequency index map) is known.

#Application: Can simulate sending a "hidden" message in a noisy channel.

import numpy as np
import hashlib
import random
import matplotlib.pyplot as plt

# === Helper Functions ===
def message_to_bits(message):
    return ''.join(format(ord(char), '08b') for char in message)

def bits_to_message(bits):
    chars = [chr(int(bits[i:i+8], 2)) for i in range(0, len(bits), 8)]
    return ''.join(chars)

def get_scrambled_indices(password, num_indices, signal_length):
    hash_bytes = hashlib.sha256(password.encode()).digest()
    seed = int.from_bytes(hash_bytes, 'big')
    rng = random.Random(seed)
    all_indices = list(range(10, signal_length // 2))  # Avoid low-frequency/DC components
    rng.shuffle(all_indices)
    return all_indices[:num_indices]

def embed_bits_in_signal(signal, bits, password):
    fft_signal = np.fft.fft(signal)
    indices = get_scrambled_indices(password, len(bits), len(fft_signal))
    
    for i, bit in enumerate(bits):
        if bit == '1':
            fft_signal[indices[i]] *= 1.5
        else:
            fft_signal[indices[i]] *= 0.5


    return np.fft.ifft(fft_signal).real

def extract_bits_from_signal(signal, password, bit_count, reference_fft):
    fft_signal = np.fft.fft(signal)
    indices = get_scrambled_indices(password, bit_count, len(fft_signal))

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
    base_signal = 5 * np.sin(2 * np.pi * 100 * t)

    message = "HELLO"
    password = "my_secret_password"

    binary = message_to_bits(message)
    encoded_signal = embed_bits_in_signal(base_signal, binary, password)

    # Add optional Gaussian noise
    noisy_signal = encoded_signal + np.random.normal(0, 0.005, len(encoded_signal))  # less noise

    reference_fft = np.fft.fft(base_signal)



    # Decode
    extracted_bits = extract_bits_from_signal(noisy_signal, password, len(binary), reference_fft)
    decoded_message = bits_to_message(extracted_bits)

    # Results
    print("Original Message: ", message)
    print("Decoded Message:  ", decoded_message)
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
