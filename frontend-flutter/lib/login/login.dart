import 'package:cardpay/services/auth.dart';
import 'package:cardpay/services/models.dart' as model;
import 'package:cardpay/services/utils.dart';
import 'package:cardpay/services/validation.dart';
import 'package:cardpay/shared/error.dart' as err;
import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import "package:provider/src/provider.dart";

class LoginScreen extends StatelessWidget {
  model.RollNumber rollNumber = model.RollNumber();
  String password = '';

  LoginScreen({Key? key}) : super(key: key);
  final _signInFormKey = GlobalKey<FormState>();

  void _submit(BuildContext context) async {
    context.read<model.ErrorModel>().errorResolved();

    if (!_signInFormKey.currentState!.validate()) {
      return;
    }

    try {
      final userDetails = await AuthService().signIn(rollNumber, password);
      // print(userDetails);
      if (!userDetails.user!.emailVerified) {
        // printError("User not Verified hence going to Std Verification");
        Navigator.pushNamed(context, '/student-verification');
        return;
      }
    } on FirebaseAuthException catch (e) {
      if (codeToMessage.containsKey(e.code)) {
        context
            .read<model.ErrorModel>()
            .errorOcurred(e.code, codeToMessage[e.code]);
        printError(codeToMessage[e.code]);
      } else {
        context.read<model.ErrorModel>().errorOcurred(
              e.code,
              "Unknown exception thrown: ${e.code}",
            );
        printError("Unknown exception thrown: ${e.code}");
      }
      return;
    }
    // ignore: use_build_context_synchronously
    Navigator.pushNamed(context, '/dashboard');
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Form(
          key: _signInFormKey,
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text(
                'Welcome',
                style: Theme.of(context).textTheme.headline5,
              ),
              Container(
                width: 250,
                child: Text(
                  'Sign in to continue',
                  style: Theme.of(context).textTheme.bodyText2,
                  textAlign: TextAlign.center,
                ),
              ),
              Container(
                width: 250,
                margin: const EdgeInsets.only(top: 15),
                padding: const EdgeInsets.only(left: 20),
                decoration: BoxDecoration(
                  borderRadius: const BorderRadius.all(
                    Radius.circular(10),
                  ),
                  color: Colors.orange[700],
                ),
                child: TextFormField(
                  autovalidateMode: AutovalidateMode.onUserInteraction,
                  onChanged: (rollNumberValue) =>
                      rollNumber.setRollNumber = rollNumberValue,
                  decoration: const InputDecoration(
                    labelText: 'University Roll Number',
                    border: InputBorder.none,
                  ),
                  validator: (rollNumberValue) {
                    if (rollNumberValue == null) {
                      return "Please enter Roll Number";
                    }
                    if (!rollNumberValue.isValidRollNumber) {
                      return "Invalid ID";
                    }
                    return null;
                  },
                ),
              ),
              Container(
                width: 250,
                margin: const EdgeInsets.only(top: 15),
                padding: const EdgeInsets.only(left: 20),
                decoration: BoxDecoration(
                  borderRadius: const BorderRadius.all(
                    Radius.circular(10),
                  ),
                  color: Colors.orange[700],
                ),
                child: TextFormField(
                  obscureText: true,
                  autovalidateMode: AutovalidateMode.onUserInteraction,
                  onChanged: (passwordValue) => password = passwordValue,
                  decoration: const InputDecoration(
                    labelText: 'Password',
                    border: InputBorder.none,
                  ),
                ),
              ),
              const err.ErrorWidget(),
              Container(
                width: 250,
                padding: const EdgeInsets.only(top: 15),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.end,
                  children: [
                    GestureDetector(
                      onTap: () =>
                          Navigator.pushNamed(context, '/forgot-password'),
                      child: Text(
                        'Forgot Password?',
                        style: Theme.of(context).textTheme.bodyText2,
                      ),
                    ),
                  ],
                ),
              ),
              Container(
                width: 250,
                margin: const EdgeInsets.only(top: 10),
                child: MaterialButton(
                  color: Colors.orange[800],
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(10),
                  ),
                  onPressed: () => _submit(context),
                  child: const Text(
                    'Sign In',
                  ),
                ),
              ),
              Container(
                width: 250,
                margin: const EdgeInsets.only(top: 10),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    const Text(
                      "Don't have an account? ",
                    ),
                    GestureDetector(
                      onTap: () => Navigator.pushNamed(context, '/signup'),
                      child: const Text(
                        "Sign Up",
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
