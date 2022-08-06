import 'package:cardpay/services/functions.dart';
import 'package:cardpay/services/models.dart';
import 'package:cardpay/services/utils.dart';
import 'package:firebase_auth/firebase_auth.dart';

class AuthService {
  final userStream = FirebaseAuth.instance.authStateChanges();
  final user = FirebaseAuth.instance.currentUser;

  Future<bool> signUp(
      String email, String password, String fullName, String rollNumber) async {
    try {
      await FirebaseAuth.instance.createUserWithEmailAndPassword(
        email: "$email@lums.edu.pk",
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
      print('Found error');
      // print(e.code);

      switch (e.code) {
        case "email-already-in-use":
          printError("LUMS ID is Already in Use");
          break;
        case "weak-password":
          printError("Weak Password");
          break;
        default:
          print(e.code);
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
