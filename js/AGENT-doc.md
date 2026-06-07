# SwifttAuth-Fire (JavaScript/NPM)

This is the frontend component of `swifttauth-fire`. It provides an extremely simple setup for Google Authentication using Firebase.

## Installation

```bash
npm install swifttauth-fire firebase
# Or using bun:
bun add swifttauth-fire firebase
```

## Setup Instructions for Future Self

### 1. Firebase Project Setup
1. Go to your Firebase Console and create a project.
2. Enable **Authentication** and choose the **Google** provider.
3. In Project Settings, create a Web App to get your config object.

### 2. Environment Variables
Add these to your `.env` or `.env.local`:
```env
NEXT_PUBLIC_FIREBASE_API_KEY=your_api_key
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
NEXT_PUBLIC_FIREBASE_PROJECT_ID=your_project_id
NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=your_project.appspot.com
NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=your_sender_id
NEXT_PUBLIC_FIREBASE_APP_ID=your_app_id
```

### 3. Initialize Firebase
Create a `firebase.js` or `firebase.ts` file in your project:
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

---

## Usage

### Vanilla JS / Vite (Without React)
```javascript
import { auth } from "./firebase.js";
import { signInWithGoogle, getAuthToken } from "swifttauth-fire";

const loginButton = document.getElementById("login");

loginButton.addEventListener("click", async () => {
  const credential = await signInWithGoogle(auth);
  console.log("Logged in:", credential.user);
  
  // Need to call your backend? Get the token!
  const token = await getAuthToken(credential.user);
  console.log("Bearer Token:", token);
});
```

### React / Next.js
Use the built-in React hook for reactive auth state:

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
        {/* Pass the token to your backend API via headers */}
      </div>
    );
  }

  return <button onClick={login}>Sign In with Google</button>;
}
```
