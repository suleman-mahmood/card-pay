import * as functions from 'firebase-functions';
import { db } from './initialize';
import { throwError } from './utils';
import { userAuthenticated } from './validations';

interface checkUserAuthAndDocReturnInterface {
	uid: string;
	usersRef: FirebaseFirestore.DocumentReference<FirebaseFirestore.DocumentData>;
	userSnapshot: FirebaseFirestore.DocumentSnapshot<FirebaseFirestore.DocumentData>;
}

// TODO: Convert this into a decorator
export const checkUserAuthAndDoc = async (
	context: functions.https.CallableContext
): Promise<checkUserAuthAndDocReturnInterface> => {
	userAuthenticated(context);

	// Get the user's uid
	const uid: string = context.auth!.uid;

	// Get the user details from Firestore
	const usersRef = db.collection('users').doc(uid);
	const userSnapshot = await usersRef.get();

	if (!userSnapshot.exists) {
		throwError('not-found', 'User does not exist in Firestore');
	}

	return {
		uid,
		usersRef,
		userSnapshot,
	};
};

export const noDocumentWithRollNumber = async (rollNumber: string) => {
	const userQueryRef = db
		.collection('users')
		.where('rollNumber', '==', rollNumber);
	const senderSnapshot = await userQueryRef.get();
	if (!senderSnapshot.empty) {
		throwError(
			'already-exists',
			'User with the roll number already exists in Firestore'
		);
	}
};
