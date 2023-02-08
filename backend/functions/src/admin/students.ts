import * as functions from 'firebase-functions';
import { db } from '../initialize';
import { adminCheck } from './utils';

interface getStudentData {
	rollNumber: string;
}
export const getStudent = functions
	.region('asia-south1')
	.https.onCall(async (data: getStudentData, context) => {
		adminCheck(context);

		/* Success */

		const ref = db
			.collection('users')
			.where('rollNumber', '==', data.rollNumber);
		const querySnapshot = await ref.get();

		if (querySnapshot.size !== 1) {
			throw new functions.https.HttpsError(
				'failed-precondition',
				'None or multiple documents exist for the roll number provided'
			);
		}
		return querySnapshot.docs[0].data();
	});
