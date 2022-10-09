import * as functions from "firebase-functions";
import {admin, db} from "./initialize";

type Role = "student" | "unknown";

interface CreateUserData {
  fullName: string;
  rollNumber: string;
  pin: string;
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

  /*
  Checks
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
        "already-exists", "User document already exists in Firestore"
    );
  }

  // Get the sender details from Firestore
  const userQueryRef = db.collection("users")
      .where("rollNumber", "==", data.rollNumber);
  const senderSnapshot = await userQueryRef.get();
  if (!senderSnapshot.empty) {
    throw new functions.https.HttpsError(
        "already-exists",
        "User with the roll number already exists in Firestore",
    );
  }

  /*
  Handle Success
  */

  await admin.auth().updateUser(uid, {
    displayName: data.fullName,
  });

  return ref.set({
    id: uid,
    fullName: data.fullName.trim(),
    personalEmail: "",
    email: data.rollNumber + "@lums.edu.pk",
    pendingDeposits: false,
    pin: data.pin,
    phoneNumber: "",
    rollNumber: data.rollNumber,
    verified: false,
    role: role,
    balance: 0,
    transactions: [],
  });
});
