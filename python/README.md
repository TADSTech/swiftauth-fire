# SwifttAuth-Fire

SwifttAuth-Fire provides Google Sign-In authentication scaffolding for Firebase across frontend and backend applications. It offers a streamlined developer experience by simplifying the configuration of Firebase Auth popups on the frontend and token verification on the backend.

## Project Structure

The repository contains two packages:

1. **`js/`** (NPM Package): The frontend library supporting React, Next.js, Vite, and Vanilla JS.
2. **`python/`** (PIP Package): The backend validation library supporting Django and FastAPI.

---

## Frontend Setup (JavaScript)

### Installation

To install the package:

```bash
bun add swifttauth-fire firebase
```

Or using npm:

```bash
npm install swifttauth-fire firebase
```

### Environment Variables

Define the following environment variables in your frontend project's configuration (e.g., `.env.local`):

```env
NEXT_PUBLIC_FIREBASE_API_KEY=your_api_key
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
NEXT_PUBLIC_FIREBASE_PROJECT_ID=your_project_id
NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=your_project.appspot.com
NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=your_sender_id
NEXT_PUBLIC_FIREBASE_APP_ID=your_app_id
```

### Firebase Initialization

Create a utility file (e.g., `firebase.js`) to initialize the Firebase SDK:

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

### Usage Examples

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

### Installation

Install the package via pip:

```bash
pip install swifttauth-fire firebase-admin
```

### Firebase Service Account Credentials

For secure ID token verification, the backend requires a service account key JSON file.

1. Generate a private key JSON from the Firebase Console (Project Settings > Service accounts).
2. Save the key JSON file securely in your backend project directory. Add the file to your `.gitignore` to prevent committing it.
3. Define the environment variable pointing to your key file:

```env
FIREBASE_SERVICE_ACCOUNT_PATH=/path/to/your/firebase-adminsdk.json
```

Alternatively, pass the file path directly to the initializer in your application startup code:

```python
from swifttauth_fire import init_firebase
init_firebase("path/to/firebase-adminsdk.json")
```

### Usage Examples

#### Django Integration

Protect Django views with the `@swiftt_auth_required` decorator. This extracts the Bearer token from the `Authorization` header and assigns the decoded token payload to `request.firebase_user`.

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

Protect FastAPI routes using the `get_current_user` dependency.

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

Navigate to the `js` directory, ensure dependencies are installed, and execute tests:

```bash
cd js
bun install
bun test
```

### Running Python Tests

Navigate to the `python` directory, install testing dependencies, and execute tests:

```bash
cd python
pip install pytest
pytest
```
