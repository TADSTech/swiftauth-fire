import { signInWithPopup, GoogleAuthProvider } from "firebase/auth";

/**
 * Trigger a Google Sign In Popup.
 * @param {import("firebase/auth").Auth} auth - The initialized Firebase Auth instance.
 * @returns {Promise<import("firebase/auth").UserCredential>} The user credential on success.
 */
export const signInWithGoogle = async (auth) => {
  const provider = new GoogleAuthProvider();
  provider.setCustomParameters({ prompt: "select_account" });
  return await signInWithPopup(auth, provider);
};

/**
 * Helper to easily fetch the JWT ID Token for backend verification.
 * @param {import("firebase/auth").User} user - The Firebase User object.
 * @returns {Promise<string>} The JWT token.
 */
export const getAuthToken = async (user) => {
  if (!user) return null;
  return await user.getIdToken(true);
};
