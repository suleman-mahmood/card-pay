import 'package:cardpay/services/exceptions.dart';
import 'package:cardpay/services/functions.dart';
import 'package:cardpay/services/models.dart';
import 'package:cardpay/services/utils.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:shared_preferences/shared_preferences.dart';

class AuthService {
  final userStream = FirebaseAuth.instance.authStateChanges();
  final user = FirebaseAuth.instance.currentUser;

  Future<void> signUp(
    String fullName,
    RollNumber rollNumber,
    String password,
  ) async {
    await FirebaseAuth.instance.createUserWithEmailAndPassword(
      email: rollNumber.getEmail,
      password: password,
    );
    await sendEmailVerification();
    await FunctionsSevice().createUser(
      CreateUserArguments(
        fullName: fullName,
        rollNumber: rollNumber.getRollNumber,
        role: StudentRole.student,
      ),
    );
    // Persist email and password to local storage
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString("rollNumber", rollNumber.getRollNumber);
    await prefs.setString("password", password);
  }

  Future<void> signIn(RollNumber rollNumber, String password) async {
    final userDetails = await FirebaseAuth.instance.signInWithEmailAndPassword(
      email: rollNumber.getEmail,
      password: password,
    );
    if (userDetails.user == null) {
      throw UserIsNull(
        "Can't find logged in user using firebase's authentication service",
      );
    }
    if (!userDetails.user!.emailVerified) {
      throw EmailUnverified("User has not verified his email");
    }
  }

  Future<void> signOut() async {
    await FirebaseAuth.instance.signOut();
  }

  Future<void> sendEmailVerification() async {
    await user?.sendEmailVerification();
  }
}
