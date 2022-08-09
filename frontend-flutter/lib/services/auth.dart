import 'package:cardpay/services/functions.dart';
import 'package:cardpay/services/models.dart';
import 'package:cardpay/services/utils.dart';
import 'package:firebase_auth/firebase_auth.dart';

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
    await FunctionsSevice().createUser(
      CreateUserArguments(
        fullName: fullName,
        rollNumber: rollNumber.getRollNumber,
        role: StudentRole.student,
      ),
    );
  }

  Future<void> signIn(RollNumber rollNumber, String password) async {
    printWarning(rollNumber.getEmail);
    await FirebaseAuth.instance.signInWithEmailAndPassword(
      email: rollNumber.getEmail,
      password: password,
    );
  }

  Future<void> signOut() async {
    await FirebaseAuth.instance.signOut();
  }
}
