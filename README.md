# 🔐 Cipherus

**Cipherus** is a powerful, personal encryption tool built with precision and pride. At its core, Cipherus uses **Fernet encryption**, which combines **AES-128 (CBC mode)** with **HMAC-SHA256**, ensuring both confidentiality and integrity of your files. It’s layered with signature checks, optional obfuscation, and foolproof validation to prevent misuse or tampering.

---

## 🧠 Why Cipherus?

This isn’t just another file locker. Cipherus is a tool I’ve built and hardened from scratch, combining modern cryptographic standards with custom logic. It’s minimal, elegant, and **as of now, uncrackable** by any known brute-force or cryptanalytic method — unless someone has your key.

> 🔐 "If you don’t have the key, you don’t get the file. Period."

I'm genuinely proud of what Cipherus has become — it’s not only secure but also smart:
- Prevents re-encryption of encrypted files ✅  
- Verifies `.cphkey` compatibility ✅  
- Protects you from yourself with clear checks and confirmations ✅  

---

## 💡 What Cipherus Uses

- **AES-128 (CBC)** via Fernet (Cryptography library)
- **HMAC-SHA256** for message authentication
- **Base64-encoded key storage**
- **Custom `.cphkey` format** with embedded signature
- **Tamper detection**, **overwrite protection**, and more

---

## ⚠️ Trust the Code, Not Just the Hype

Cipherus doesn’t rely on security by obscurity. It follows strong, proven standards.

> **If you edit the encrypted file or key manually, you're done.  
Cipherus knows, and it won’t decrypt garbage.**

---

## ⚙️ Features

- 🔒 File encryption and decryption using `cryptography.fernet`
- 🧠 Unique hash generation tied to your key
- 🔐 Custom `.cphkey` format with embedded signature
- 🛡️ Prevents re-encryption of already encrypted files
- ✅ Marker validation to ensure file integrity
- 📄 Menu-driven terminal interface
- 💾 Option to save encrypted/decrypted output to a new file
- 🚫 Error handling and user-friendly messages

---

## 🧪 Requirements

Install requirements using:

```bash
pip install -r requirements.txt
```

---

## 📝 How to Use

1. **Run the script**  
```bash
python cipherus.py
```

2. **Choose an option**

    1: Encrypt a file

    2: Decrypt a file

    3: Help

    4: Exit (or press 'ctrl + c' to quit)

    #### 🔐 During Encryption:
      - You’ll be asked to create or load a .cphkey

      - Optionally overwrite the original file or save to a new one

    #### 🔓 During Decryption:
      - Load the correct .cphkey file

      - Output can overwrite the original or be saved separately

3. **Follow instructions on screen**

    - You can create a new .cphkey file or load an existing one.

    - Choose whether to overwrite the file or save as a new file.

    - Press Enter when prompted to continue.

## ⚠️ Important
[!] Do NOT modify the secret key or encrypted files manually.
Tampering will cause decryption to fail.

## Notes
- Works fully offline

- Designed for individual use or educational purposes

- Can easily extend it with CLI arguments or a GUI

## 📁 License
This project is licensed under the Creative Commons Non-Commercial License.