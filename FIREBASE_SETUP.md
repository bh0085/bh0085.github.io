# Firebase Authentication Setup Guide

## Step 1: Create Firebase Project

1. Go to https://console.firebase.google.com/
2. Click **"Add project"**
3. Project name: `mlcl-website` (or whatever you prefer)
4. Disable Google Analytics (you can skip this)
5. Click **"Create project"**
6. Wait for it to finish, then click **"Continue"**

## Step 2: Enable Google Authentication

1. In your Firebase Console, click **"Authentication"** in the left sidebar
2. Click **"Get started"** button
3. Click the **"Sign-in method"** tab at the top
4. Click on **"Google"** in the providers list
5. Toggle the **"Enable"** switch to ON
6. Under "Authorized domains", add:
   - `mlcl.ai`
   - `www.mlcl.ai`
7. Click **"Save"**

## Step 3: Register Web App & Get Config

1. Go back to Project Overview (home icon in sidebar)
2. Click the **"</>"** (web) icon to add a web app
3. App nickname: `mlcl-website`
4. **DO NOT** check "Also set up Firebase Hosting"
5. Click **"Register app"**
6. You'll see a code block with `firebaseConfig` - **COPY THIS ENTIRE OBJECT**

It looks like:
```javascript
const firebaseConfig = {
  apiKey: "AIzaSy...",
  authDomain: "mlcl-website-xxxxx.firebaseapp.com",
  projectId: "mlcl-website-xxxxx",
  storageBucket: "mlcl-website-xxxxx.appspot.com",
  messagingSenderId: "123456789",
  appId: "1:123456789:web:abcdef123456"
};
```

7. **SEND ME THIS CONFIG** and I'll update the auth.js file

## Step 4: Configure Google Cloud Console (Optional but Recommended)

1. Go to https://console.cloud.google.com/
2. Select your Firebase project from the dropdown
3. Go to **APIs & Services** → **Credentials**
4. Find the **Web client** (auto created by Firebase)
5. Click to edit it
6. Under **Authorized JavaScript origins**, add:
   - `https://mlcl.ai`
   - `https://www.mlcl.ai`
7. Under **Authorized redirect URIs**, add:
   - `https://mlcl.ai/__/auth/handler`
   - `https://www.mlcl.ai/__/auth/handler`
8. Click **Save**

## Step 5: Send Me Your Config

**Copy the firebaseConfig object from Step 3** and send it to me. I'll update the `auth.js` file with your actual credentials.

## What's Already Done

✅ Login page created (`/login.html`)  
✅ Auth system created (`/auth.js`)  
✅ All pages protected (index, branding, moodboards)  
✅ Sign-out buttons added  
✅ @mlcl.ai email restriction enabled  

## After I Update Your Config

Once I add your Firebase credentials to `auth.js`, the site will:

1. Redirect unauthenticated users to `/login.html`
2. Show Google sign-in button
3. Only allow `@mlcl.ai` email addresses
4. Keep users signed in across page refreshes
5. Show sign-out buttons on protected pages

## Testing Locally (Optional)

If you want to test locally before pushing:

1. Run a local server: `python3 -m http.server 8000`
2. Visit: `http://localhost:8000`
3. Add `localhost:8000` to Firebase **Authorized domains** in Authentication settings

## Questions?

Let me know if you hit any snags during the Firebase setup!

