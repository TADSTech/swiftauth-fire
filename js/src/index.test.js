import { test, expect, mock } from "bun:test";

// Mock firebase/auth before importing index.js
mock.module("firebase/auth", () => {
  return {
    signInWithPopup: mock(async (auth, provider) => {
      if (auth === "fail") {
        throw new Error("Auth failed");
      }
      return {
        user: {
          getIdToken: mock(async (forceRefresh) => {
            return "mocked-jwt-token";
          })
        }
      };
    }),
    GoogleAuthProvider: class {
      constructor() {
        this.customParameters = {};
      }
      setCustomParameters(params) {
        this.customParameters = params;
      }
    }
  };
});

import { signInWithGoogle, getAuthToken } from "./index.js";

test("signInWithGoogle calls firebase signInWithPopup and sets select_account", async () => {
  const mockAuth = {};
  const credential = await signInWithGoogle(mockAuth);
  
  expect(credential.user).toBeDefined();
  const token = await credential.user.getIdToken();
  expect(token).toBe("mocked-jwt-token");
});

test("getAuthToken returns null if no user is provided", async () => {
  const token = await getAuthToken(null);
  expect(token).toBeNull();
});

test("getAuthToken returns token if user is provided", async () => {
  const mockUser = {
    getIdToken: mock(async (forceRefresh) => {
      expect(forceRefresh).toBe(true);
      return "another-token";
    })
  };
  const token = await getAuthToken(mockUser);
  expect(token).toBe("another-token");
  expect(mockUser.getIdToken).toHaveBeenCalledTimes(1);
});
