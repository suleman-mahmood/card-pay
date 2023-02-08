// import * as functions from "firebase-functions";
// import * as admin from "firebase-admin";

// admin.initializeApp();

// // Start writing Firebase Functions
// // https://firebase.google.com/docs/functions/typescript
//
// export const helloWorld = functions.https.onRequest((request, response) => {
//   functions.logger.info("Hello logs!", {structuredData: true});
//   response.send("Hello from Firebase!");
// });

export {
	createUser,
	changeUserPin,
	resendOtpEmail,
	verifyEmailOtp,
	sendForgotPasswordEmail,
	verifyForgotPasswordOtp,
} from './auth';
export { addDepositRequest, handleDepositSuccess } from './deposit';
export { makeTransaction } from './makeTransaction';
export { transfer } from './transfer';

// Admin functions
export {
	getAllVendors,
	makeVendorAccount,
	reconcileVendor,
} from './admin/vendors';

export { getStudent } from './admin/students';
export { topUpUserVirtualCash } from './admin/transactions';
