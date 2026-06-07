import { test, expect, mock, beforeEach } from "bun:test";

let stateValues = {};
let stateSetters = {};
let effectCallback = null;
let onAuthStateChangedCallback = null;
let unsubscribeCalled = false;

// Mock react
mock.module("react", () => {
  return {
    useState: (initialValue) => {
      // We will trace state by initial value types or names for simple mock tracking
      let key = "unknown";
      if (initialValue === null) key = "userOrToken";
      else if (initialValue === true) key = "loading";

      // If key is userOrToken, we distinguish between user and token based on order:
      // First null is user, second null is token
      if (key === "userOrToken") {
        if (!stateValues.hasOwnProperty("user")) {
          key = "user";
        } else {
          key = "token";
        }
      }

      stateValues[key] = initialValue;
      stateSetters[key] = mock((val) => {
        stateValues[key] = val;
      });

      return [initialValue, stateSetters[key]];
    },
    useEffect: mock((callback) => {
      effectCallback = callback;
    })
  };
});

// Mock firebase/auth
mock.module("firebase/auth", () => {
  return {
    onAuthStateChanged: mock((auth, callback) => {
      onAuthStateChangedCallback = callback;
      return () => {
        unsubscribeCalled = true;
      };
    })
  };
});

// Mock ./index.js
mock.module("./index.js", () => {
  return {
    signInWithGoogle: mock(async (auth) => {
      if (auth === "fail") throw new Error("Google Sign-In failed");
      return { user: { email: "test@example.com" } };
    }),
    getAuthToken: mock(async (user) => {
      if (!user) return null;
      return "mocked-jwt-token";
    })
  };
});

import { useSwifttAuth } from "./react.js";
import { signInWithGoogle } from "./index.js";

beforeEach(() => {
  stateValues = {};
  stateSetters = {};
  effectCallback = null;
  onAuthStateChangedCallback = null;
  unsubscribeCalled = false;
});

test("useSwifttAuth initializes state correctly", () => {
  const mockAuth = { signOut: mock(() => {}) };
  const hook = useSwifttAuth(mockAuth);

  expect(hook.user).toBeNull();
  expect(hook.loading).toBe(true);
  expect(hook.token).toBeNull();
  expect(effectCallback).toBeDefined();
});

test("useSwifttAuth handles state change when user signs in", async () => {
  const mockAuth = { signOut: mock(() => {}) };
  useSwifttAuth(mockAuth);

  // Trigger useEffect
  const cleanup = effectCallback();

  // Trigger Auth state change to logged in user
  const mockUser = { email: "test@example.com" };
  await onAuthStateChangedCallback(mockUser);

  expect(stateSetters.user).toHaveBeenCalledWith(mockUser);
  expect(stateSetters.token).toHaveBeenCalledWith("mocked-jwt-token");
  expect(stateSetters.loading).toHaveBeenCalledWith(false);

  // Trigger cleanup
  cleanup();
  expect(unsubscribeCalled).toBe(true);
});

test("useSwifttAuth handles state change when user signs out", async () => {
  const mockAuth = { signOut: mock(() => {}) };
  useSwifttAuth(mockAuth);

  const cleanup = effectCallback();
  await onAuthStateChangedCallback(null);

  expect(stateSetters.user).toHaveBeenCalledWith(null);
  expect(stateSetters.token).toHaveBeenCalledWith(null);
  expect(stateSetters.loading).toHaveBeenCalledWith(false);

  cleanup();
});

test("useSwifttAuth login and logout wrapper methods work", async () => {
  const mockAuth = { signOut: mock(async () => {}) };
  const hook = useSwifttAuth(mockAuth);

  await hook.login();
  expect(stateSetters.loading).toHaveBeenCalledWith(true);
  expect(stateSetters.loading).toHaveBeenCalledWith(false);

  await hook.logout();
  expect(mockAuth.signOut).toHaveBeenCalledTimes(1);
});
