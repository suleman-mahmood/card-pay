import 'package:cardpay/services/auth.dart';
import 'package:cardpay/services/models.dart' as model;
import 'package:cardpay/services/utils.dart';
import 'package:cardpay/services/validation.dart';
import 'package:cardpay/shared/buttons/big_icon.dart';
import 'package:cardpay/shared/buttons/text.dart';
import 'package:cardpay/shared/error.dart' as err;
import 'package:cardpay/shared/inputs/placeholder.dart';
import 'package:cardpay/shared/layouts/auth.dart';
import 'package:cardpay/shared/loading.dart';
import 'package:cardpay/shared/typography/caption.dart';
import 'package:cardpay/shared/typography/link.dart';
import 'package:cardpay/shared/typography/main_heading.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class LoginScreen extends StatelessWidget {
  model.RollNumber rollNumber = model.RollNumber();
  String password = '';

  LoginScreen({Key? key}) : super(key: key);
  final _signInFormKey = GlobalKey<FormState>();

  void _submit(BuildContext context) async {
    if (!_signInFormKey.currentState!.validate()) {
      return;
    }

    context.read<model.Loading>().showLoading();

    try {
      await AuthService().signIn(rollNumber, password);
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
            return const LoadingWidget();
          }

          return Form(
            key: _signInFormKey,
            child: AuthLayoutWidget(
              children: [
                // Main heading
                MainHeadingWidget(content: "Sign in your account"),

                SizedBox(height: 10),

                // Sub heading
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    CaptionWidget(content: "Don't have an account yet?"),
                    Padding(
                      padding: const EdgeInsets.only(left: 10),
                      child: LinkWidget(
                          content: "Sign Up Now", redirectTo: "/signup"),
                    ),
                  ],
                ),

                SizedBox(height: 30),

                // Roll number input
                PlaceholderInputWidget(
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
                PlaceholderInputWidget(
                  labelText: "Password",
                  hintText: "******",
                  obscureText: true,
                  invertColors: true,
                  onChanged: (v) => password = v,
                ),

                const err.ErrorWidget(),

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
                    LinkWidget(
                        content: "Forgot password?",
                        redirectTo: "/forgot-password"),
                  ],
                ),

                SizedBox(height: 20),

                // Sign in button
                TextButtonWidget(
                  content: "Sign In",
                  onPressed: () => _submit(context),
                ),

                // Spacer(),
                SizedBox(height: 100),

                // Row fingerprint and face id
                Row(
                  children: [
                    BigIconButtonWidget(
                      icon: Icons.fingerprint,
                      onPressed: () => {},
                    ),
                    Spacer(),
                    BigIconButtonWidget(
                      icon: Icons.face_unlock_outlined,
                      onPressed: () => {},
                    ),
                  ],
                )
              ],
            ),
          );
        });
  }
}

class LoginScreenOld extends StatelessWidget {
  model.RollNumber rollNumber = model.RollNumber();
  String password = '';

  LoginScreenOld({Key? key}) : super(key: key);
  final _signInFormKey = GlobalKey<FormState>();

  void _submit(BuildContext context) async {
    if (!_signInFormKey.currentState!.validate()) {
      return;
    }

    context.read<model.Loading>().showLoading();

    try {
      await AuthService().signIn(rollNumber, password);
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
                            onTap: () => Navigator.pushNamed(
                                context, '/forgot-password'),
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
                            onTap: () =>
                                Navigator.pushNamed(context, '/signup'),
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
        });
  }
}
