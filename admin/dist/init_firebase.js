"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.functions = exports.db = exports.auth = void 0;
const app_1 = require("firebase-admin/app");
const auth_1 = require("firebase-admin/auth");
const firestore_1 = require("firebase-admin/firestore");
const functions_1 = require("firebase-admin/functions");
const app = (0, app_1.initializeApp)({
    credential: (0, app_1.applicationDefault)(),
});
// Initialize Auth
exports.auth = (0, auth_1.getAuth)(app);
// Initialize Firestore
exports.db = (0, firestore_1.getFirestore)(app);
// Initialize functions with emulator
exports.functions = (0, functions_1.getFunctions)(app);
