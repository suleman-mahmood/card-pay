import * as functions from 'firebase-functions';
import { db } from './initialize';

interface checkUserAuthAndDocReturnInterface {
	uid: string;
	usersRef: FirebaseFirestore.DocumentReference<FirebaseFirestore.DocumentData>;
	userSnapshot: FirebaseFirestore.DocumentSnapshot<FirebaseFirestore.DocumentData>;
}

// TODO: Convert this into a decorator
export const checkUserAuthAndDoc = async (
	context: functions.https.CallableContext
): Promise<checkUserAuthAndDocReturnInterface> => {
	if (!context.auth) {
		throw new functions.https.HttpsError(
			'unauthenticated',
			'User is not authenticated'
		);
	}

	// Get the user's uid
	const uid: string = context.auth.uid;

	// Get the user details from Firestore
	const usersRef = db.collection('users').doc(uid);
	const userSnapshot = await usersRef.get();

	if (!userSnapshot.exists) {
		throw new functions.https.HttpsError(
			'not-found',
			'User does not exist in Firestore'
		);
	}

	return {
		uid,
		usersRef,
		userSnapshot,
	};
};
