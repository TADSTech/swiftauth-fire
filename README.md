# SwifttAuth-Fire

[![NPM Version](https://img.shields.io/npm/v/swifttauth-fire.svg?style=flat-square)](https://www.npmjs.com/package/swifttauth-fire)
[![PyPI Version](https://img.shields.io/pypi/v/swifttauth-fire.svg?style=flat-square)](https://pypi.org/project/swifttauth-fire/)
[![Bun Compatible](https://img.shields.io/badge/bun-compatible-black.svg?style=flat-square&logo=bun)](https://bun.sh)
[![License](https://img.shields.io/github/license/TADSTech/swiftauth-fire.svg?style=flat-square)](https://github.com/TADSTech/swiftauth-fire/blob/main/LICENSE)

SwifttAuth-Fire provides Google Sign-In authentication scaffolding for Firebase across frontend and backend applications. It simplifies the configuration of Firebase Auth popups on the frontend and token verification on the backend, enabling rapid prototyping and integration.

---

## Agent-First Documentation Scaffolding

This library is designed with an AI-agent-first approach. When you or your coding agent installs the packages, SwifttAuth-Fire automatically drops developer-friendly documentation directly into your workspace.

- **Frontend (NPM/Bun):** Installing the package automatically places `AGENT-doc.md` at your project root.
- **Backend (PIP):** Running the CLI command `swifttauth-init` drops `AGENT-doc.md` into your current working directory.

An AI agent (like Antigravity) can read this file immediately and implement the full authentication flow for you.

---

## Installation

### Frontend (JavaScript/TypeScript)

Install via Bun:

```bash
bun add swifttauth-fire firebase
```

Or NPM:

```bash
npm install swifttauth-fire firebase
```

### Backend (Python)

Install via Pip:

```bash
pip install swifttauth-fire firebase-admin
```

---

## Frontend Setup (JavaScript)

### 1. Environment Variables

Define the following variables in your frontend environment settings (e.g., `.env.local`):

```env
NEXT_PUBLIC_FIREBASE_API_KEY=your_api_key
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
NEXT_PUBLIC_FIREBASE_PROJECT_ID=your_project_id
NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=your_project.appspot.com
NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=your_sender_id
NEXT_PUBLIC_FIREBASE_APP_ID=your_app_id
```

### 2. Initialize Firebase

Create a utility file (e.g., `firebase.js`) to initialize the SDK:

```javascript
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";

const firebaseConfig = {
  apiKey: process.env.NEXT_PUBLIC_FIREBASE_API_KEY,
  authDomain: process.env.NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN,
  projectId: process.env.NEXT_PUBLIC_FIREBASE_PROJECT_ID,
  storageBucket: process.env.NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: process.env.NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID,
  appId: process.env.NEXT_PUBLIC_FIREBASE_APP_ID
};

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
```

### 3. Usage Examples

#### Vanilla JavaScript / Vite
```javascript
import { auth } from "./firebase.js";
import { signInWithGoogle, getAuthToken } from "swifttauth-fire";

const loginButton = document.getElementById("login");

loginButton.addEventListener("click", async () => {
  try {
    const credential = await signInWithGoogle(auth);
    const token = await getAuthToken(credential.user);
    console.log("Bearer Token:", token);
  } catch (error) {
    console.error("Sign-in failed:", error);
  }
});
```

#### React / Next.js Client Components
```javascript
"use client";
import { auth } from "./firebase.js";
import { useSwifttAuth } from "swifttauth-fire/react";

export default function LoginButton() {
  const { user, loading, token, login, logout } = useSwifttAuth(auth);

  if (loading) return <p>Loading...</p>;

  if (user) {
    return (
      <div>
        <p>Welcome, {user.displayName}</p>
        <button onClick={logout}>Sign Out</button>
      </div>
    );
  }

  return <button onClick={login}>Sign In with Google</button>;
}
```

---

## Backend Setup (Python)

### 1. Firebase Service Account

1. Generate a private key JSON from the Firebase Console (Project Settings > Service accounts).
2. Save the key JSON file securely in your backend project folder. **Do not commit this file to Git.**
3. Define the environment variable pointing to the key file path:

```env
FIREBASE_SERVICE_ACCOUNT_PATH=/path/to/your/firebase-adminsdk.json
```

Alternatively, initialize the SDK manually in your application startup code:

```python
from swifttauth_fire import init_firebase
init_firebase("path/to/firebase-adminsdk.json")
```

### 2. Scaffold Agent Documentation

Generate the local documentation file in your backend directory:

```bash
swifttauth-init
```

### 3. Usage Examples

#### Django Integration
Protect views using the `@swiftt_auth_required` decorator. This extracts the Bearer token and assigns the verified user payload to `request.firebase_user`.

```python
from django.http import JsonResponse
from swifttauth_fire.django import swiftt_auth_required

@swiftt_auth_required
def protected_dashboard(request):
    user = request.firebase_user
    return JsonResponse({
        "message": f"Welcome back, {user.get('name')}!",
        "email": user.get('email'),
        "uid": user.get('uid')
    })
```

#### FastAPI Integration
Protect routes using the `get_current_user` dependency.

```python
from fastapi import FastAPI, Depends
from swifttauth_fire.fastapi import get_current_user

app = FastAPI()

@app.get("/api/protected")
def protected_route(user: dict = Depends(get_current_user)):
    return {
        "message": "Access granted to protected route",
        "user_email": user.get("email"),
        "user_id": user.get("uid")
    }
```

---

## Development and Testing

### Running JavaScript Tests
```bash
cd js
bun install
bun test
```

### Running Python Tests
```bash
cd python
pip install pytest
pytest
```