import 'package:cardpay/services/auth.dart';
import 'package:cardpay/services/models.dart' as model;
import 'package:cardpay/services/utils.dart';
import 'package:cardpay/services/validation.dart';
import 'package:cardpay/shared/shared.dart';
import 'package:cloud_functions/cloud_functions.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class SignUpScreen extends StatelessWidget {
  model.RollNumber rollNumber = model.RollNumber();
  String password = '';
  String confirmPassword = '';
  String fullName = '';

  final _signInFormKey = GlobalKey<FormState>();

  SignUpScreen({Key? key}) : super(key: key);

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
    Navigator.pushNamed(context, '/student-verification');
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return MultiProvider(
      providers: [
        ChangeNotifierProvider<model.ErrorModel>(
          create: (_) => model.ErrorModel(),
        ),
      ],
      builder: (context, child) {
        if (context.watch<model.Loading>().getLoading) {
          return const ScreenTransitionLoaderCustomWidget();
        }

        return Form(
          key: _signInFormKey,
          child: AuthLayoutCustomWidget(
            invertColors: true,
            children: [
              // Main heading
              MainHeadingTypographyCustomWidget(
                content: "Create your account",
                invertColors: true,
              ),

              SizedBox(height: 10),

              // Sub heading
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: const [
                  CaptionTypographyCustomWidget(
                    content: "Do you already have an account?",
                    invertColors: true,
                  ),
                  Padding(
                    padding: EdgeInsets.only(left: 10),
                    child: LinkTypographyCustomWidget(
                      content: "Sign In Now",
                      redirectTo: "/login",
                      invertColors: true,
                    ),
                  ),
                ],
              ),

              SizedBox(height: 20),

              // Full Name input
              PlaceholderInputCustomWidget(
                labelText: "Full Name",
                hintText: "Atif Raheem",
                onChanged: (v) => fullName = v,
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

              SizedBox(height: 20),

              // Roll number input
              PlaceholderInputCustomWidget(
                labelText: "Roll Number",
                hintText: "23100011",
                onChanged: (v) => rollNumber.setRollNumber = v,
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

              SizedBox(height: 20),

              // Password input
              PlaceholderInputCustomWidget(
                labelText: "Password",
                hintText: "********",
                obscureText: true,
                onChanged: (v) => password = v,
                validator: (passwordValue) {
                  if (passwordValue == null) {
                    return "Please enter Password";
                  }
                  if (!passwordValue.isValidPassword) {
                    return "Minimum eight characters,\nat least one letter and one number";
                  }
                  return null;
                },
              ),

              SizedBox(height: 20),

              // Confirm password input
              PlaceholderInputCustomWidget(
                labelText: "Confirm Password",
                hintText: "********",
                obscureText: true,
                onChanged: (v) => confirmPassword = v,
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

              const ErrorTypographyCustomWidget(),

              SizedBox(height: 20),

              // Remember me
              Row(
                children: [
                  // TODO: Add remember option here as well
                  Opacity(
                    opacity: 0,
                    child: Placeholder(
                      color: Colors.blue[800]!,
                      fallbackWidth: 120,
                      fallbackHeight: 20,
                    ),
                  ),
                ],
              ),

              SizedBox(height: 20),

              // Sign in button
              TextButtonCustomWidget(
                content: "Sign Up",
                invertColors: true,
                onPressed: () => _submit(context),
              ),

              // Spacer(),
              SizedBox(height: 100),

              // TOC checkbox
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Checkbox(
                      value: false,
                      onChanged: (_) => {},
                      fillColor: MaterialStateProperty.all(Colors.white)),
                  Expanded(
                    // child: BodyS
                    child: SmallBodyTypographyCustomWidget(
                      content:
                          'By creating your account you agree with  our Terms and Conditions',
                      invertColors: true,
                    ),
                  ),
                ],
              ),
            ],
          ),
        );
      },
    );
  }
}
