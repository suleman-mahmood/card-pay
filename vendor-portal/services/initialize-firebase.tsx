// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getFunctions, connectFunctionsEmulator } from "firebase/functions";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
const firebaseConfig = {
    apiKey: "AIzaSyCelFqfRRov9iaep88Cjsl_O7pr-Zdx6vU",
    authDomain: "card-pay-55c1b.firebaseapp.com",
    projectId: "card-pay-55c1b",
    storageBucket: "card-pay-55c1b.appspot.com",
    messagingSenderId: "501478058153",
    appId: "1:501478058153:web:09130f4d54dc445e8721b8"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Initialize Auth
export const auth = getAuth(app);

// Initialize functions with emulator
const _functions = getFunctions(app);
// connectFunctionsEmulator(_functions, "localhost", 5001);
export const functions = _functions;
