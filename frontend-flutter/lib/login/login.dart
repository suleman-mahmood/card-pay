import 'package:cardpay/services/auth.dart';
import 'package:cardpay/services/exceptions.dart';
import 'package:cardpay/services/models.dart' as model;
import 'package:cardpay/services/utils.dart';
import 'package:cardpay/services/validation.dart';
import 'package:cardpay/shared/shared.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:local_auth/local_auth.dart';
import 'package:provider/provider.dart';
import 'package:shared_preferences/shared_preferences.dart';

class LoginScreen extends StatelessWidget {
  model.RollNumber rollNumber = model.RollNumber();
  String password = '';

  LoginScreen({Key? key}) : super(key: key);
  final _signInFormKey = GlobalKey<FormState>();

  Future<void> _submit(BuildContext context, bool shouldValidate) async {
    if (shouldValidate && !_signInFormKey.currentState!.validate()) {
      return;
    }

    context.read<model.Loading>().showLoading();

    try {
      await AuthService().signIn(rollNumber, password);
    } on EmailUnverified catch (e) {
      // Handle navigation to student verification page
      printWarning(e.cause);
      context.read<model.ErrorModel>().errorResolved();
      context.read<model.Loading>().hideLoading();
      Navigator.pushNamed(context, '/student-verification');
      return;
    } on UserIsNull catch (e) {
      printError(e.cause);
      context.read<model.ErrorModel>().errorOcurred("User null", e.cause);
      context.read<model.Loading>().hideLoading();
      return;
    } on FirebaseAuthException catch (e) {
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
    Navigator.pushNamed(context, '/dashboard');
  }

  Future<bool> authenticateWithBiometrics() async {
    final LocalAuthentication auth = LocalAuthentication();
    bool didAuthenticate = false;

    try {
      didAuthenticate = await auth.authenticate(
        localizedReason: 'Please authenticate to show account balance',
        options: const AuthenticationOptions(biometricOnly: true),
      );
    } on PlatformException catch (e) {
      printError("Exception in biometric authentication");
      printError(e.code);
      printError(e.details);
      printError(e.message ?? "");
      return false;
    }

    // Handle after biometric authentication flow
    if (!didAuthenticate) {
      printError("Biometric was un-successful");
      return false;
    }

    // Handle successful biometric authentication
    printInGreen("Biometric was successful");

    // Get email and password from local storage
    final prefs = await SharedPreferences.getInstance();
    final rollNumberLocal = await prefs.getString("rollNumber") ?? "";
    final passwordLocal = await prefs.getString("password") ?? "";

    // Set variables to local storage values
    rollNumber.setRollNumber = rollNumberLocal;
    password = passwordLocal;

    return true;
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

        return FutureBuilder<bool>(
          future: authenticateWithBiometrics(),
          builder: (context, snapshot) {
            if (snapshot.hasData && snapshot.data == true) {
              // The biometric was successful, fake a submit
              _submit(context, false);
            }
            return Form(
              key: _signInFormKey,
              child: AuthLayoutCustomWidget(
                children: [
                  // Main heading
                  MainHeadingTypographyCustomWidget(
                      content: "Sign in your account"),

                  SizedBox(height: 10),

                  // Sub heading
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      CaptionTypographyCustomWidget(
                          content: "Don't have an account yet?"),
                      Padding(
                        padding: const EdgeInsets.only(left: 10),
                        child: LinkTypographyCustomWidget(
                            content: "Sign Up Now", redirectTo: "/signup"),
                      ),
                    ],
                  ),

                  SizedBox(height: 30),

                  // Roll number input
                  PlaceholderInputCustomWidget(
                    labelText: "Roll Number",
                    hintText: "23100011",
                    invertColors: true,
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

                  SizedBox(height: 30),

                  // Password input
                  PlaceholderInputCustomWidget(
                    labelText: "Password",
                    hintText: "******",
                    obscureText: true,
                    invertColors: true,
                    onChanged: (v) => password = v,
                  ),

                  const ErrorTypographyCustomWidget(),

                  SizedBox(height: 20),

                  // Remember me and forgot password row
                  Row(
                    children: const [
                      // TODO: Add Remeber me widget here
                      Opacity(
                        opacity: 0,
                        child: Placeholder(
                          color: Colors.blue,
                          fallbackWidth: 120,
                          fallbackHeight: 20,
                        ),
                      ),
                      Spacer(),
                      LinkTypographyCustomWidget(
                          content: "Forgot password?",
                          redirectTo: "/forgot-password"),
                    ],
                  ),

                  SizedBox(height: 20),

                  // Sign in button
                  TextButtonCustomWidget(
                    content: "Sign In",
                    onPressed: () => _submit(context, true),
                  ),

                  // Spacer(),
                  SizedBox(height: 100),

                  // Row fingerprint and face id
                  Row(
                    children: [
                      BigIconButtonCustomWidget(
                        icon: Icons.fingerprint,
                        onPressed: () => {},
                      ),
                      Spacer(),
                      BigIconButtonCustomWidget(
                        icon: Icons.face_unlock_outlined,
                        onPressed: () => {},
                      ),
                    ],
                  )
                ],
              ),
            );
          },
        );
      },
    );
  }
}
