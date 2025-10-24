// Firebase Auth Configuration
const firebaseConfig = {
  apiKey: "AIzaSyAoOu8P7aGPMlhlb8Ckk2GlcqWLiGu3rWs",
  authDomain: "mlcl-website.firebaseapp.com",
  projectId: "mlcl-website",
  storageBucket: "mlcl-website.firebasestorage.app",
  messagingSenderId: "655483104521",
  appId: "1:655483104521:web:8f761078cbb712901db7d8",
  measurementId: "G-8BTXQVQXH7"
};

// Initialize Firebase
import { initializeApp } from 'https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js';
import { getAuth, signInWithPopup, GoogleAuthProvider, onAuthStateChanged, signOut } from 'https://www.gstatic.com/firebasejs/10.7.1/firebase-auth.js';

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const provider = new GoogleAuthProvider();

// Check if user is authenticated and has @mlcl.ai email
export async function checkAuth() {
  return new Promise((resolve) => {
    onAuthStateChanged(auth, (user) => {
      if (user && user.email && user.email.endsWith('@mlcl.ai')) {
        resolve(true);
      } else {
        resolve(false);
      }
    });
  });
}

// Sign in with Google
export async function signInWithGoogle() {
  try {
    const result = await signInWithPopup(auth, provider);
    const user = result.user;
    
    if (!user.email.endsWith('@mlcl.ai')) {
      await signOut(auth);
      throw new Error('Only @mlcl.ai email addresses are allowed');
    }
    
    return user;
  } catch (error) {
    throw error;
  }
}

// Sign out
export async function signOutUser() {
  await signOut(auth);
}

// Get current user
export function getCurrentUser() {
  return auth.currentUser;
}

// Redirect to login if not authenticated
export async function requireAuth() {
  const isAuthenticated = await checkAuth();
  if (!isAuthenticated && !window.location.pathname.includes('login.html')) {
    window.location.href = '/login.html';
  }
  return isAuthenticated;
}

