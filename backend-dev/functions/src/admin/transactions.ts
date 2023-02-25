import * as functions from 'firebase-functions';
import { db } from '../initialize';
import { transactionMain } from '../makeTransaction';
import { throwError } from '../utils';
import { amountValidated, rollNumberValidated } from '../validations';
import { adminCheck, CARDPAY_ROLLNUMBER } from './utils';

interface topUpUserVirtualCashData {
	rollNumber: string; // vendor's roll number
	amount: string; // the amount to reconcile
}

export const topUpUserVirtualCash = functions
	.region('asia-south1')
	.https.onCall(async (data: topUpUserVirtualCashData, context) => {
		functions.logger.info('Args:', data);

		adminCheck(context);
		rollNumberValidated(data.rollNumber);
		amountValidated(data.amount);

		return topUpUserVirtualCashHelper(data);
	});

export const topUpUserVirtualCashHelper = async (
	data: topUpUserVirtualCashData
) => {
	amountValidated(data.amount);
	rollNumberValidated(data.rollNumber);

	const recipientRollNumber = data.rollNumber;
	const senderRollNumber = CARDPAY_ROLLNUMBER;

	// Get the recipient details from Firestore
	const recipientsQueryRef = db
		.collection('users')
		.where('rollNumber', '==', recipientRollNumber);
	const recipientSnapshot = await recipientsQueryRef.get();
	const recipientUid = recipientSnapshot.docs[0].id;

	// Get the sender details from Firestore
	const sendersQueryRef = db
		.collection('users')
		.where('rollNumber', '==', senderRollNumber);
	const senderSnapshot = await sendersQueryRef.get();
	const senderUid = senderSnapshot.docs[0].id;

	if (senderSnapshot.size !== 1) {
		throwError(
			'invalid-argument',
			'Multiple or no documents exists for sender'
		);
	}
	if (recipientSnapshot.size !== 1) {
		throwError(
			'invalid-argument',
			'Multiple or no documents exists for recipient'
		);
	}

	/*
		Handle transaction success!
	*/

	return transactionMain(senderUid, recipientUid, data.amount);
};
