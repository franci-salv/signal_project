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

