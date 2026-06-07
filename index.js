import { signInWithPopup, GoogleAuthProvider } from "firebase/auth";

export const signInWithGoogle = async (auth) => {
  const provider = new GoogleAuthProvider();
  provider.setCustomParameters({ prompt: "select_account" });
  return await signInWithPopup(auth, provider);
};