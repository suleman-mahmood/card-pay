import * as functions from 'firebase-functions';
import { topUpUserVirtualCashHelper } from './admin/transactions';
import { checkUserAuthAndDoc, noDocumentWithRollNumber } from './helpers';
import { admin, db } from './initialize';
import { generateRandom4DigitPin, sendEmail, throwError } from './utils';
import {
	fourDigitPinValidated,
	fullNameWithTwoOrMoreWords,
	passwordValidated,
	phoneNumberValidated,
	rollNumberValidated,
	uidValidated,
} from './validations';

const INITIAL_BALANCE = 50;
const REFERRAL_COMMISSION = 30;

interface CreateUserData {
	fullName: string;
	rollNumber: string;
	password: string;
	pin: string;
	phoneNumber: string;
	referralRollNumber: string;
}

export const createUser = functions
	.region('asia-south1')
	.https.onCall(async (data: CreateUserData, _) => {
		/*
			This functions signups a new user

			Invariants:
			1. User doesn't need to be authenticated
			2. User does not already exist with the same roll number
		*/

		functions.logger.info('Args:', data);

		fullNameWithTwoOrMoreWords(data.fullName);
		rollNumberValidated(data.rollNumber);
		fourDigitPinValidated(data.pin);
		phoneNumberValidated(data.phoneNumber);
		passwordValidated(data.password);

		// Check if user has entered a referral roll number and validate it
		if (data.referralRollNumber && data.referralRollNumber.length !== 0) {
			rollNumberValidated(data.referralRollNumber);
		}

		const randomPin = generateRandom4DigitPin();
		const phoneNumber = `0${data.phoneNumber}`;
		const phoneNumberE164 = `+92${data.phoneNumber}`;
		const email = `${data.rollNumber}@lums.edu.pk`;

		// 2. User does not already exist with the same roll number
		noDocumentWithRollNumber(data.rollNumber);

		/*
			Handle Success:
			1. Create user in authentication
			2. Send otp to email
			3. Add user doc
		*/

		// 1. Create user in authentication
		let uid = '';
		try {
			const userRecord = await admin.auth().createUser({
				email: email,
				password: data.password,
				displayName: data.fullName,
				emailVerified: false,
				phoneNumber: phoneNumberE164,
			});
			uid = userRecord.uid;
		} catch (e) {
			throwError(
				'unknown',
				`Couldnt create user in authentication: ${e}`,
				e
			);
		}

		// 2. Send otp to email
		const ref = db.collection('users').doc(uid);
		try {
			await db.collection('otps').doc(uid).set({
				otp: randomPin,
			});
		} catch (e) {
			throwError('unknown', `Couldnt add otp in collection: ${e}`, e);
		}

		// Send email to the user
		const subject = 'CardPay | Email Verification';
		const text = `Your 4-digit pin is: ${randomPin}`;
		const htmlBody = `Your 4-digit pin is: <b>${randomPin}</b>`;
		try {
			await sendEmail(email, subject, text, htmlBody);
		} catch (e) {
			throwError('unknown', `Couldnt send email: ${e}`, e);
		}

		// 3. Add user doc
		await ref.set({
			id: uid,
			fullName: data.fullName.trim(),
			personalEmail: '',
			email: email,
			pendingDeposits: false,
			pin: data.pin,
			phoneNumber: phoneNumber,
			rollNumber: data.rollNumber,
			verified: false,
			role: 'student',
			balance: 0,
			transactions: [],
			referralRollNumber: data.referralRollNumber,
		});

		return uid;
	});

interface VerifyEmailOtpData {
	otp: string;
	uid: string;
}

export const verifyEmailOtp = functions
	.region('asia-south1')
	.https.onCall(async (data: VerifyEmailOtpData, _) => {
		/*
			This function verifies the calling user's email

			Invariants:
			1. User doesn't need to be authenticated
		*/

		functions.logger.info('Args:', data);

		fourDigitPinValidated(data.otp);
		await uidValidated(data.uid);

		const usersRef = db.collection('users').doc(data.uid);
		const userSnapshot = await usersRef.get();
		if (!userSnapshot.exists) {
			throwError('not-found', 'User does not exist in Firestore');
		}

		const doc = await db.collection('otps').doc(data.uid).get();
		if (!doc.exists) {
			throwError('not-found', 'Users OTP doesnt exist in db');
		}
		const originalOtp = doc.data()!.otp;

		if (originalOtp !== data.otp) {
			throwError('failed-precondition', 'Incorrect OTP');
		}

		await usersRef.update({
			verified: true,
		});

		await topUpUserVirtualCashHelper({
			amount: INITIAL_BALANCE.toString(),
			rollNumber: userSnapshot.data()!.rollNumber,
		});

		const referralRollNumber = userSnapshot.data()!.referralRollNumber;

		// Send Rs.30 to referral roll number if exists
		if (referralRollNumber && referralRollNumber.length !== 0) {
			// Referrall roll number exists
			return topUpUserVirtualCashHelper({
				amount: REFERRAL_COMMISSION.toString(),
				rollNumber: referralRollNumber,
			});
		} else {
			return {
				status: 'success',
				message: 'Sign up for successful',
			};
		}
	});

interface ResendOtpEmailData {
	uid: string;
}

export const resendOtpEmail = functions
	.region('asia-south1')
	.https.onCall(async (data: ResendOtpEmailData, _) => {
		/*
			This functions resends the otp email to the user

			Invariants:
			1. User doesn't need to be authenticated
		*/

		functions.logger.info('Args:', data);

		await uidValidated(data.uid);

		const uid = data.uid;
		const usersRef = db.collection('users').doc(uid);
		const userSnapshot = await usersRef.get();
		if (!userSnapshot.exists) {
			throwError('not-found', 'User does not exist in Firestore');
		}

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
	oldPin: string;
}

export const changeUserPin = functions
	.region('asia-south1')
	.https.onCall(async (data: ChangeUserPinData, context) => {
		/*
			This function changes the calling user's pin

			Invariants:
			1. User should be authenticated
			2. Old pin must match with the one in db
		*/

		functions.logger.info('Args:', data);

		fourDigitPinValidated(data.pin);
		fourDigitPinValidated(data.oldPin);
		const { usersRef, userSnapshot } = await checkUserAuthAndDoc(context);

		const newPin = data.pin;
		const oldPin = data.oldPin;

		if (userSnapshot.data()!.pin !== oldPin) {
			throwError('invalid-argument', 'Old pin doesnt match');
		}

		/*
			Handle Success
		*/

		return usersRef.update({
			pin: newPin,
		});
	});

interface SendForgotPasswordEmailData {
	rollNumber: string;
}

export const sendForgotPasswordEmail = functions
	.region('asia-south1')
	.https.onCall(async (data: SendForgotPasswordEmailData, context) => {
		/*
			This function generates an otp and sends forgot password email to the users
		*/

		functions.logger.info('Args:', data);

		rollNumberValidated(data.rollNumber);
		const randomPin = generateRandom4DigitPin();

		/*
			Success
		*/

		// Save otp in firestore
		await db.collection('forgot_password_otps').doc(data.rollNumber).set({
			otp: randomPin,
		});

		// Send email to the user
		const studentEmail = data.rollNumber + '@lums.edu.pk';
		const subject = 'CardPay | Forgot Password';
		const text = `Your 4-digit pin is: ${randomPin}`;
		const htmlBody = `Your 4-digit pin is: <b>${randomPin}</b>`;
		return sendEmail(studentEmail, subject, text, htmlBody);
	});

interface verifyForgotPasswordOtpData {
	rollNumber: string;
	otp: string;
	password: string;
}

export const verifyForgotPasswordOtp = functions
	.region('asia-south1')
	.https.onCall(async (data: verifyForgotPasswordOtpData, _) => {
		/*
			This function verifies the calling user's email

			Invariants:
			1. User doesn't need to be authenticated
		*/

		functions.logger.info('Args:', data);

		rollNumberValidated(data.rollNumber);
		fourDigitPinValidated(data.otp);
		passwordValidated(data.password);

		const userOtp = data.otp;

		// Get the sender details from Firestore
		const userQueryRef = db
			.collection('users')
			.where('rollNumber', '==', data.rollNumber);
		const senderSnapshot = await userQueryRef.get();
		if (senderSnapshot.empty) {
			throwError('not-found', 'User does not exists in Firestore');
		}
		if (senderSnapshot.size != 1) {
			throwError(
				'invalid-argument',
				'User roll number with multiple documents exist in firestore!'
			);
		}

		const doc = await db
			.collection('forgot_password_otps')
			.doc(data.rollNumber)
			.get();

		if (!doc.exists) {
			throwError(
				'not-found',
				'Users forgot password OTP doesnt exist in db'
			);
		}
		const originalOtp = doc.data()!.otp;

		if (originalOtp !== userOtp) {
			throwError('failed-precondition', 'Incorrect OTP');
		}

		const senderUid = senderSnapshot.docs[0].id;

		/*
			Success
		*/

		return admin.auth().updateUser(senderUid, {
			password: data.password,
		});
	});
