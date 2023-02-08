import * as functions from 'firebase-functions';

export const ADMIN_UIDS: Array<string> = [
	'xe2YEIpAr6XUbAu1SNfUY55Eutf1', // Suleman
	'2PfhS8wU3EMnu0fVNTa2piqQIla2', // Tayyab
	'CZi8ek4SxMORpuY92Rs2O0iRqmu2', // Shamsi
	'cbRuwoSNsogJt5sQnJnSsQouneP2', // Suleman-dev
	'AgV1v1mCfLXx4D489HoEJFFefbu1', // Faraz-dev
];

export const CARDPAY_ROLLNUMBER = '00000000';

export const adminCheck = (context: functions.https.CallableContext) => {
	// Check is user is authenticated
	if (!context.auth) {
		throw new functions.https.HttpsError(
			'unauthenticated',
			'User is not authenticated'
		);
	}

	// Get the user's uid
	const uid: string = context.auth.uid;

	if (!ADMIN_UIDS.includes(uid)) {
		throw new functions.https.HttpsError(
			'unauthenticated',
			'Only authorized admins can call this request'
		);
	}
};
