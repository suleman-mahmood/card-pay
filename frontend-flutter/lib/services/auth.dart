import 'package:cardpay/services/functions.dart';
import 'package:cardpay/services/models.dart';
import 'package:cardpay/services/utils.dart';
import 'package:firebase_auth/firebase_auth.dart';

class AuthService {
  final userStream = FirebaseAuth.instance.authStateChanges();
  final user = FirebaseAuth.instance.currentUser;

  Future<bool> signUp(
      String fullName, String rollNumber, String password) async {
    try {
      await FirebaseAuth.instance.createUserWithEmailAndPassword(
        email: "$rollNumber@lums.edu.pk",
        password: password,
      );
      // TODO: handle exception properly
      if (!await FunctionsSevice().createUser(
        CreateUserArguments(
          fullName: fullName,
          rollNumber: rollNumber,
          role: StudentRole.student,
        ),
      )) return false;
      return true;
    } on FirebaseAuthException catch (e) {
      // Handle error

      switch (e.code) {
        case "email-already-in-use":
          printError("Roll number is already registered");
          break;
        // case "weak-password":
        //   printError("Weak Password");
        //   break;
        default:
          print("Exception thrown:${e.code}");
      }
      return false;
    }
  }

  Future<bool> signIn(String email, String password) async {
    try {
      await FirebaseAuth.instance.signInWithEmailAndPassword(
        email: email,
        password: password,
      );
      return true;
    } on FirebaseAuthException catch (e) {
      // Handle error
      print(e.code);
      return false;
    }
  }

  Future<void> signOut() async {
    await FirebaseAuth.instance.signOut();
  }
}
