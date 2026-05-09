# WebAuthn Secure Identity Management System

A passwordless authentication implementation leveraging the **FIDO2/WebAuthn** protocol. This system replaces traditional password-based login with hardware-bound, public-key cryptography, ensuring high-level security against phishing and credential stuffing.

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
   git clone <your-repo-link>
   cd secure-identity-system
