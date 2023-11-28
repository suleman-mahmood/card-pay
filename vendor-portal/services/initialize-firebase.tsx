// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getStorage, ref, uploadBytes, getDownloadURL } from "firebase/storage";
// import { getAnalytics } from "firebase/analytics";

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyAXEhK6txqjYGdCf7i2Mt3OzECAESDupaM",
  authDomain: "cardpay-1.firebaseapp.com",
  projectId: "cardpay-1",
  storageBucket: "cardpay-1.appspot.com",
  messagingSenderId: "674516928217",
  appId: "1:674516928217:web:48efa604e11ddeb1d220c8",
  measurementId: "G-MTM971QTES"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
export const storage = getStorage(app);
// Initialize Auth
export const auth = getAuth(app);
// export const analytics = getAnalytics(app);