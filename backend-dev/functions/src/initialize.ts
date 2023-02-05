import * as _admin from 'firebase-admin';

_admin.initializeApp();

export const db = _admin.firestore();
export const admin = _admin;
