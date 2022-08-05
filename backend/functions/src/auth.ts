import * as functions from "firebase-functions";
import {admin, db} from "./initialize";

type Role = "student" | "unknown";

interface CreateUserData {
  fullName: string;
  rollNumber: string;
  role: Role;
}

export const createUser = functions.https.onCall(async (
    data: CreateUserData,
    context
) => {
  /*
    This function creates a new user in Firestore if it isn't already present.
    param: data = {
      fullName: string,
      rollNumber: string,
      role: string,
    }
   */

  if (!context.auth) {
    throw new functions.https.HttpsError(
        "unauthenticated", "User is not authenticated"
    );
  }

  const uid: string = context.auth.uid;
  const role: Role = data.role === "student" ? "student" : "unknown";
  const ref = db.collection("users").doc(uid);

  const snapshot = await ref.get();
  const docAlreadyExists: boolean = snapshot.exists;

  if (docAlreadyExists) {
    throw new functions.https.HttpsError(
        "already-exists", "User already exists in Firestore"
    );
  }

  await admin.auth().updateUser(uid, {
    displayName: data.fullName,
  });

  return ref.set({
    id: uid,
    fullName: data.fullName,
    personalEmail: "",
    email: data.rollNumber + "@lums.edu.pk",
    phoneNumber: "",
    rollNumber: data.rollNumber,
    verified: false,
    role: role,
    balance: 0,
    transactions: [],
  });
});
