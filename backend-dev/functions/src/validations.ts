import * as functions from 'firebase-functions';
import { admin } from './initialize';
import { throwError } from './utils';

export const userAuthenticated = (context: functions.https.CallableContext) => {
	if (!context.auth) {
		throwError('unauthenticated', 'User is not authenticated');
	}
};

export const fullNameWithTwoOrMoreWords = (fullName: string) => {
	if (fullName.split(' ').length < 2) {
		throwError('invalid-argument', 'Enter first and last name');
	}
};

export const passwordValidated = (password: string) => {
	if (password.length < 6) {
		throwError(
			'invalid-argument',
			'Password must be of at least 6 characters'
		);
	}
};

export const emailValidated = (email: string) => {
	if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(email) === false) {
		throwError('invalid-argument', 'Email format is incorrect');
	}
};

export const uidValidated = async (uid: string) => {
	try {
		await admin.auth().getUser(uid);
	} catch (e) {
		throwError('invalid-argument', `UID is not related to any user: ${e}`);
	}
};

export const amountValidated = (amount: string) => {
	let amountNumber = 0;
	try {
		amountNumber = parseInt(amount);
	} catch (e) {
		throwError(
			'invalid-argument',
			'Amount cannot be converted to a number'
		);
	}
	if (amountNumber <= 0) {
		throwError('invalid-argument', 'Amount must be greater than 0');
	}
};

export const phoneNumberValidated = (phoneNumber: string) => {
	if (phoneNumber.length !== 10) {
		throwError('invalid-argument', 'Phone number must be 10 digits long');
	}
	if (/^[0-9]+$/.test(phoneNumber) === false) {
		throwError('invalid-argument', 'Phone number must contain digits only');
	}
};

export const rollNumberValidated = (rollNumber: string) => {
	if (rollNumber.length !== 8) {
		throwError(
			'invalid-argument',
			'Sender roll number must be 8 digits long'
		);
	}
	if (/^[0-9]+$/.test(rollNumber) === false) {
		throwError(
			'invalid-argument',
			'Sender roll number must contain digits only'
		);
	}
};

export const fourDigitPinValidated = (pin: string) => {
	if (pin.length !== 4) {
		throwError(
			'invalid-argument',
			'User pin must be exactly 4 digits long'
		);
	}
	if (/^[0-9]{4}$/.test(pin) === false) {
		throwError('invalid-argument', 'User pin must contain digits only');
	}
};
