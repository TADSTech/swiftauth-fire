"use client";

import { useState, useEffect } from "react";
import { onAuthStateChanged } from "firebase/auth";
import { signInWithGoogle, getAuthToken } from "./index.js";

/**
 * React hook for SwifttAuth.
 * Works seamlessly in React, Next.js (client components), and Vite.
 * @param {import("firebase/auth").Auth} auth - The initialized Firebase Auth instance.
 */
export const useSwifttAuth = (auth) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [token, setToken] = useState(null);

  useEffect(() => {
    if (!auth) return;
    
    const unsubscribe = onAuthStateChanged(auth, async (currentUser) => {
      setUser(currentUser);
      if (currentUser) {
        const jwt = await getAuthToken(currentUser);
        setToken(jwt);
      } else {
        setToken(null);
      }
      setLoading(false);
    });

    return () => unsubscribe();
  }, [auth]);

  const login = async () => {
    setLoading(true);
    try {
      await signInWithGoogle(auth);
    } catch (error) {
      console.error("Google Sign-In Error:", error);
    } finally {
      setLoading(false);
    }
  };

  const logout = async () => {
    if (auth) {
      await auth.signOut();
    }
  };

  return { user, loading, token, login, logout };
};
