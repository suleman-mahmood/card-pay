import * as functions from 'firebase-functions';
import { checkUserAuthAndDoc } from './helpers';
import { db } from './initialize';
import { transactionMain } from './makeTransaction';
import { UserDoc } from './types';
import { throwError } from './utils';
import {
	amountValidated,
	fourDigitPinValidated,
	rollNumberValidated,
} from './validations';

interface transferData {
	amount: string;
	recipientRollNumber: string;
	pin: string;
}

export const transfer = functions
	.region('asia-south1')
	.https.onCall(async (data: transferData, context) => {
		/*
			This function transfers the amount from the caller's id
			to the recipient's roll number in the argument
		*/

		functions.logger.info('Args:', data);

		amountValidated(data.amount);
		rollNumberValidated(data.recipientRollNumber);
		fourDigitPinValidated(data.pin);

		const { uid, userSnapshot } = await checkUserAuthAndDoc(context);
		const sendersUid = uid;
		const senderSnapshot = userSnapshot;
		const senderModel = senderSnapshot.data() as UserDoc;

		const recipientRollNumber = data.recipientRollNumber;

		if (senderModel.pin !== data.pin) {
			throwError(
				'invalid-argument',
				'Incorrect pin! User pin does not match'
			);
		}

		// Self transfer is invalid
		if (senderModel.rollNumber === recipientRollNumber) {
			throwError(
				'failed-precondition',
				'You cannot send money to yourself'
			);
		}

		// Get the recipient details from Firestore
		const recipientsQueryRef = db
			.collection('users')
			.where('rollNumber', '==', recipientRollNumber);
		const recipientSnapshot = await recipientsQueryRef.get();
		if (recipientSnapshot.empty) {
			throwError('not-found', 'Recipient does not exist in Firestore');
		}
		if (recipientSnapshot.docs.length > 1) {
			throwError(
				'internal',
				'Multiple recipients with the same roll number exists in Firestore'
			);
		}
		const recipientUid = recipientSnapshot.docs[0].id;

		/*
			Handle transaction success!
		*/

		return transactionMain(sendersUid, recipientUid, data.amount);
	});
