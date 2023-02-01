import * as functions from 'firebase-functions';
import { checkUserAuthAndDoc } from './helpers';
import { admin, db } from './initialize';
import { generateRandom4DigitPin, sendEmail } from './utils';

type Role = 'student' | 'unknown';

interface CreateUserData {
	fullName: string;
	rollNumber: string;
	pin: string;
	role: Role;
	phoneNumber: string;
}

export const createUser = functions
	.region('asia-south1')
	.https.onCall(async (data: CreateUserData, context) => {
		/*
			This function creates a new user in Firestore if it isn't already present.
			param: data = {
			fullName: string,
			rollNumber: string,
			role: string,
			}
		*/

		/*
			Pre-conditions:
			1. User is authenticated
			2. User does not already exist
			3. Same roll number is not already registered
		*/

		if (!context.auth) {
			throw new functions.https.HttpsError(
				'unauthenticated',
				'User is not authenticated'
			);
		}

		const uid: string = context.auth.uid;
		const role: Role = data.role === 'student' ? 'student' : 'unknown';
		const ref = db.collection('users').doc(uid);

		const snapshot = await ref.get();
		const docAlreadyExists: boolean = snapshot.exists;

		if (docAlreadyExists) {
			throw new functions.https.HttpsError(
				'already-exists',
				'User document already exists in Firestore'
			);
		}

		// Get the sender details from Firestore
		const userQueryRef = db
			.collection('users')
			.where('rollNumber', '==', data.rollNumber);
		const senderSnapshot = await userQueryRef.get();
		if (!senderSnapshot.empty) {
			throw new functions.https.HttpsError(
				'already-exists',
				'User with the roll number already exists in Firestore'
			);
		}

		/*
			Handle Success
		*/

		await admin.auth().updateUser(uid, {
			displayName: data.fullName,
		});

		// generate a string of 4 digits instead of a number
		const randomPin = generateRandom4DigitPin();

		// save otp in firestore
		await db.collection('otps').doc(uid).set({
			otp: randomPin,
		});

		// send email to the user
		const studentEmail = data.rollNumber + '@lums.edu.pk';
		const subject = 'CardPay | Email Verification';
		const text = `Your 4-digit pin is: ${randomPin}`;
		const htmlBody = `Your 4-digit pin is: <b>${randomPin}</b>`;
		await sendEmail(studentEmail, subject, text, htmlBody);

		return ref.set({
			id: uid,
			fullName: data.fullName.trim(),
			personalEmail: '',
			email: studentEmail,
			pendingDeposits: false,
			pin: data.pin,
			phoneNumber: data.phoneNumber,
			rollNumber: data.rollNumber,
			verified: false,
			role: role,
			balance: 0,
			transactions: [],
		});
	});

interface VerifyEmailOtpData {
	otp: string;
}

export const verifyEmailOtp = functions
	.region('asia-south1')
	.https.onCall(async (data: VerifyEmailOtpData, context) => {
		/*
    This function verifies the calling user's email
    param: data = {
      otp: string
    }
  */

		if (!context.auth) {
			throw new functions.https.HttpsError(
				'unauthenticated',
				'User is not authenticated'
			);
		}

		const uid: string = context.auth.uid;

		const userOtp = data.otp;

		if (userOtp.length !== 4) {
			throw new functions.https.HttpsError(
				'invalid-argument',
				'User OTP must be exactly 4 digits long'
			);
		}

		const doc = await db.collection('otps').doc(uid).get();
		if (!doc.exists) {
			throw new functions.https.HttpsError(
				'not-found',
				'Users OTP doesnt exist in db'
			);
		}
		const originalOtp = doc.data()!.otp;

		if (originalOtp !== userOtp) {
			throw new functions.https.HttpsError(
				'failed-precondition',
				'Incorrect OTP'
			);
		}

		const ref = db.collection('users').doc(uid);
		return ref.update({
			verified: true,
		});
	});

export const resendOtpEmail = functions
	.region('asia-south1')
	.https.onCall(async (data, context) => {
		const { uid, userSnapshot } = await checkUserAuthAndDoc(context);

		const doc = await db.collection('otps').doc(uid).get();
		let originalOtp = '';
		if (!doc.exists) {
			// generate a string of 4 digits instead of a number
			const randomPin = generateRandom4DigitPin();

			// save otp in firestore
			await db.collection('otps').doc(uid).set({
				otp: randomPin,
			});
			originalOtp = randomPin;
		} else {
			originalOtp = doc.data()!.otp;
		}

		// send email to the user
		const studentEmail = userSnapshot.data()!.rollNumber + '@lums.edu.pk';
		const subject = 'CardPay | Email Verification';
		const text = `Your 4-digit pin is: ${originalOtp}`;
		const htmlBody = `Your 4-digit pin is: <b>${originalOtp}</b>`;
		return sendEmail(studentEmail, subject, text, htmlBody);
	});

interface ChangeUserPinData {
	pin: string;
}

export const changeUserPin = functions
	.region('asia-south1')
	.https.onCall(async (data: ChangeUserPinData, context) => {
		/*
			This function changes the calling user's pin
			param: data = {
			pin: string
			}
		*/

		/*
			Pre-conditions:
			1. Can only change pin of an existent user and verified user
		*/

		if (!context.auth) {
			throw new functions.https.HttpsError(
				'unauthenticated',
				'User is not authenticated'
			);
		}

		const newPin = data.pin;

		if (newPin.length !== 4) {
			throw new functions.https.HttpsError(
				'invalid-argument',
				'User pin must be exactly 4 digits long'
			);
		}

		const regex = /^[0-9]{4}$/g; // Matches 4 digits only 0-9
		const found = newPin.match(regex);

		if (found === null) {
			throw new functions.https.HttpsError(
				'invalid-argument',
				'User pin must only contain 0-9 digits'
			);
		}

		const uid: string = context.auth.uid;
		const ref = db.collection('users').doc(uid);

		const snapshot = await ref.get();
		const docAlreadyExists: boolean = snapshot.exists;

		if (!docAlreadyExists) {
			throw new functions.https.HttpsError(
				'not-found',
				'User document does not exist in Firestore'
			);
		}

		/*
			Handle Success
		*/

		return ref.update({
			pin: data.pin,
		});
	});
