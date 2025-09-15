# 🔒 Noise-Resilient Signal Encryption (DFT-based)

## 📖 Overview
This project demonstrates a simple **signal encryption and decryption scheme using the Discrete Fourier Transform (DFT)**.  
The idea is to **embed a secret message into specific frequency bins** of a signal, while filling the rest with random noise.  
The message can only be recovered if the correct **password-derived frequency map (the “key”)** is known.

> Think of it as hiding a note inside the “frequency space” of a noisy signal.  

---

## 🚀 Features
- 🔑 Password-based frequency scrambling  
- 🔄 Text ↔ Binary conversion  
- 🎛️ Embed bits into FFT magnitudes  
- 📡 Add Gaussian noise to simulate channels  
- 🔓 Extract & reconstruct hidden messages  
- 📊 Visualization of FFT before/after embedding  

---

## 🔑 How It Works
1. **Message → Bits**  
   Text is converted into binary (`message_to_bits`).  

2. **Password → Frequency Map**  
   A SHA-256 hash of the password seeds a RNG, which selects valid FFT indices.  

3. **Embedding**  
   - Bit `1` → scale FFT magnitude **×3**  
   - Bit `0` → scale FFT magnitude **×0.3**  

4. **Reconstruction**  
   Apply Inverse FFT → produces a time-domain signal containing the hidden message.  

5. **Decryption**  
   Using the same password, retrieve frequency bins, compare magnitudes to the reference FFT, and recover the bitstring → convert back to text.  

---

## 📊 Example
- **Original message:**  
Mihai_is_hiding_in_the_closet
- Encoded into a noisy signal with Gaussian noise.  
- Successfully recovered with **high accuracy** (100% if noise is low).  

Example plot outputs include:  
- FFT magnitude before vs. after embedding  
- Original vs. encoded vs. noisy signals  
- Frequency spectra comparisons  

---

## 🛠️ Requirements
- Python 3.x  
- [NumPy](https://numpy.org/)  
- [Matplotlib](https://matplotlib.org/)  

Install dependencies:  

pip install numpy matplotlib


This will:
- Generate a base noisy signal  
- Embed and encode the secret message  
- Add optional Gaussian noise  
- Decode and print the recovered message  
- Display FFT and signal plots  

---

## 🔒 Applications
- Simulating **secure communication in noisy channels**  
- Educational tool for:
  - Frequency-domain manipulation  
  - Signal encryption/decryption basics  
  - Noise resilience in communications  

---

## ⚠️ Disclaimer
This project is for **educational purposes only**.  
It is **not cryptographically secure** for real-world communication.  
But it’s a fun and insightful way to learn about **DFT, signal processing, and noise resilience**.  


## 📷 Example Results (Demo)

### 1️⃣ FFT Magnitude Before vs After Embedding
<img width="2343" height="1273" alt="FFT Magnitude Before vs After" src="https://github.com/user-attachments/assets/0164e146-f8b5-4a86-996c-b4bbe8b27386" />  

This plot compares the **FFT magnitude spectrum of the original base signal (blue)** with the **spectrum after embedding the hidden message (orange)**.  
- Both curves overlap closely most of the time → meaning the base signal’s frequency structure is largely preserved.  
- Small differences in specific bins correspond to where the secret bits were embedded (scaled up or down).  
- These modifications are subtle enough that the overall spectrum looks almost identical, which helps *hide* the message inside the noise.  

---

### 2️⃣ Signal Encryption & Decryption (Time Domain)
<img width="1474" height="710" alt="Signal Encryption & Decryption" src="https://github.com/user-attachments/assets/8e0b784f-b208-438f-80c4-a1516ffb0136" />  

This time-domain plot shows three signals overlaid:  
- **Original Signal (blue):** The random base signal used as a carrier.  
- **Encoded Signal (orange):** The signal after the hidden message has been embedded in the frequency domain, then transformed back to time domain.  
- **Noisy Signal (green):** The encoded signal with additional Gaussian noise added to simulate a real-world noisy channel.  

Key observations:  
- The encoded signal looks very similar to the original, with only minor differences invisible to the naked eye.  
- Even after adding noise, the hidden message can still be successfully recovered if the correct key is used.  

---

### 3️⃣ FFT Magnitudes (Reference vs Noisy)
<img width="1994" height="1249" alt="FFT Magnitudes" src="https://github.com/user-attachments/assets/e995f967-f8a2-4085-ba65-de39ae97ee38" />  

This plot compares the **reference FFT (blue)** with the **FFT of the noisy signal (orange)**:  
- The noise perturbs the spectrum slightly, but the key frequency bins where the message is embedded remain distinguishable.  
- This demonstrates the **noise-resilience** of the approach: even in a disturbed spectrum, the relative changes (upscaled or downscaled bins) can still be detected and mapped back to the original bits.

This model ended up having 99% character accuracy of a message with a bit length of any size. 

