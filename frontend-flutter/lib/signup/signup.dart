// ignore_for_file: non_constant_identifier_names

import 'package:cardpay/services/auth.dart';
import 'package:cardpay/services/models.dart' as model;
import 'package:cardpay/services/utils.dart';
import 'package:cardpay/services/validation.dart';
import 'package:cardpay/shared/error.dart' as err;
import 'package:cardpay/shared/loading.dart';
import 'package:cloud_functions/cloud_functions.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class SignUpScreen extends StatelessWidget {
  model.RollNumber rollNumber = model.RollNumber();
  String password = '';
  String confirmPassword = '';
  String fullName = '';

  SignUpScreen({Key? key}) : super(key: key);
  final _signInFormKey = GlobalKey<FormState>();

  void _submit(BuildContext context) async {
    if (!_signInFormKey.currentState!.validate()) {
      // No need to throw any error as each textfield will take care
      // of its own validation error
      return;
    }

    context.read<model.Loading>().showLoading();

    try {
      await AuthService().signUp(fullName, rollNumber, password);
    } on FirebaseAuthException catch (e) {
      final String errorMessage;

      if (codeToMessage.containsKey(e.code)) {
        errorMessage = codeToMessage[e.code];
      } else {
        errorMessage = "Unknown exception thrown: ${e.code}";
      }

      context.read<model.ErrorModel>().errorOcurred(
            e.code,
            errorMessage,
          );
      printError(errorMessage);
      context.read<model.Loading>().hideLoading();
      return;
    } on FirebaseFunctionsException catch (e) {
      final String errorMessage;

      if (codeToMessage.containsKey(e.code)) {
        errorMessage = codeToMessage[e.code];
      } else {
        errorMessage = "Unknown exception thrown: ${e.code}";
      }

      printError(errorMessage);
      context.read<model.ErrorModel>().errorOcurred(
            e.code,
            errorMessage,
          );
      context.read<model.Loading>().hideLoading();
      return;
    }

    // Handle success
    context.read<model.ErrorModel>().errorResolved();
    context.read<model.Loading>().hideLoading();
    printWarning(
      "$fullName has rollnumber: ${rollNumber.getRollNumber} with pass: $password",
    );
    Navigator.pushNamed(context, '/dashboard');
  }

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider<model.ErrorModel>(
          create: (_) => model.ErrorModel(),
        ),
      ],
      builder: (context, child) {
        if (context.watch<model.Loading>().getLoading) {
          return const LoadingWidget();
        }

        return Scaffold(
          body: Center(
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
                    'Lorem ipsum dolor sit amet, consectetur adipiscing elit',
                    style: Theme.of(context).textTheme.bodyText2,
                    textAlign: TextAlign.center,
                  ),
                ),
                Form(
                  key: _signInFormKey,
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
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
                          onChanged: (nameValue) => fullName = nameValue,
                          decoration: const InputDecoration(
                            labelText: 'Full Name',
                            border: InputBorder.none,
                          ),
                          validator: (nameValue) {
                            if (nameValue == null) {
                              return "Please enter your name";
                            }
                            if (!nameValue.isValidName) {
                              return "Please enter your first name and last name";
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
                          autovalidateMode: AutovalidateMode.onUserInteraction,
                          onChanged: (rollNumberValue) =>
                              rollNumber.setRollNumber = rollNumberValue,
                          decoration: const InputDecoration(
                            labelText: 'LUMS Roll number',
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
                          onChanged: (passwordValue) =>
                              password = passwordValue,
                          decoration: const InputDecoration(
                            labelText: 'Password',
                            border: InputBorder.none,
                          ),
                          validator: (passwordValue) {
                            if (passwordValue == null) {
                              return "Please enter Password";
                            }
                            if (!passwordValue.isValidPassword) {
                              return "Weak Password";
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
                          onChanged: (confirmPasswordValue) =>
                              confirmPassword = confirmPasswordValue,
                          decoration: const InputDecoration(
                            labelText: 'Confirm Password',
                            border: InputBorder.none,
                          ),
                          validator: (confirmPasswordValue) {
                            if (confirmPasswordValue == null) {
                              return "Please re-enter Password";
                            }
                            if (confirmPasswordValue != password) {
                              return "The passwords don't match";
                            }
                            return null;
                          },
                        ),
                      ),
                      const err.ErrorWidget(),
                      Container(
                        margin: EdgeInsets.only(top: 15),
                        child: Row(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Checkbox(value: false, onChanged: (e) => true),
                            Container(
                              width: 200,
                              child: Text(
                                'By creating your account you agree with  our Terms and Conditions',
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
                            'Sign Up',
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),
        );
      },
    );
  }
}
