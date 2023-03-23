import * as functions from 'firebase-functions';
import { throwError } from '../utils';
import { userAuthenticated } from '../validations';

export const ADMIN_UIDS: Array<string> = [
	'xe2YEIpAr6XUbAu1SNfUY55Eutf1', // Suleman
	'2PfhS8wU3EMnu0fVNTa2piqQIla2', // Tayyab
	'CZi8ek4SxMORpuY92Rs2O0iRqmu2', // Shamsi
	'HYtUWuJUz0Mho4dN8Y4hvsfZFCs1', // Huzaifa
];

export const CARDPAY_ROLLNUMBER = '00000000';

export const adminCheck = (context: functions.https.CallableContext) => {
	userAuthenticated(context);

	// Get the user's uid
	const uid: string = context.auth!.uid;

	if (!ADMIN_UIDS.includes(uid)) {
		throwError(
			'unauthenticated',
			'Only authorized admins can call this request'
		);
	}
};
