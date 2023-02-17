// Import the functions you need from the SDKs you need
import { initializeApp } from 'firebase/app';
import { getAuth } from 'firebase/auth';
import { getFirestore } from 'firebase/firestore';
import { getFunctions, connectFunctionsEmulator } from 'firebase/functions';

const RUN_DEV = true;
const RUN_IN_EMULATOR = false;

// Your web app's Firebase configuration
const firebaseConfig = {
	apiKey: 'AIzaSyCelFqfRRov9iaep88Cjsl_O7pr-Zdx6vU',
	authDomain: 'card-pay-55c1b.firebaseapp.com',
	projectId: 'card-pay-55c1b',
	storageBucket: 'card-pay-55c1b.appspot.com',
	messagingSenderId: '501478058153',
	appId: '1:501478058153:web:09130f4d54dc445e8721b8',
};

const DevfirebaseConfig = {
	apiKey: 'AIzaSyDZMs9HgaJ5UrUXjkgPKQzIeKjHfuoyd9U',
	authDomain: 'card-pay-dev.firebaseapp.com',
	projectId: 'card-pay-dev',
	storageBucket: 'card-pay-dev.appspot.com',
	messagingSenderId: '451051195028',
	appId: '1:451051195028:web:e375314f89070d1b600281',
};

// Initialize Firebase
const app = initializeApp(RUN_DEV ? DevfirebaseConfig : firebaseConfig);

// Initialize Auth
export const auth = getAuth(app);

// Initialize Firestore
export const db = getFirestore(app);

// Initialize functions with emulator
const _functions = getFunctions(app, 'asia-south1');

// Connect with emulator
if (RUN_IN_EMULATOR) {
	connectFunctionsEmulator(_functions, 'localhost', 5001);
}
export const functions = _functions;
