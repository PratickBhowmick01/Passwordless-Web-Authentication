# Passwordless Web-service authentication

A passwordless authentication implementation leveraging the **WebAuthn.io** flow. This system replaces traditional credential (password) based login with public-key cryptography, ensuring high-level security so that server no longer becomes a target, prevents phishing and avoids weak/reusing passwords.

## ✨ Features
- **Biometric Authentication:** Supports Windows Hello, TouchID, and FaceID.
- **Hardware-Bound Security:** Private keys never leave the user's physical device.
- **Phishing Protection:** Credentials are bound to the specific `RP_ID` (domain), preventing cross-site attacks.
- **Replay Protection:** Implements signature counter (`sign_count`) tracking to prevent intercepted credential reuse.

## 🛠️ Tech Stack
- **Backend:** Python (FastAPI)
- **Frontend:** HTML5, JavaScript (SimpleWebAuthn)
- **Library:** `py-webauthn` (Python implementation of the WebAuthn spec)
- **Environment:** Uvicorn, AnyIO

## 🚀 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/PratickBhowmick01/Passwordless-Web-Authentication/tree/main
   cd Codes
   
2. **Install Dependencies:**
   ```bash
   pip install fastapi uvicorn webauthn 

3. **Configurations:**
   ```bash
   # main.py
   RP_ID = "your-unique-id.ngrok-free.app"
   ORIGIN = "https://your-unique-id.ngrok-free.app"

4. 
