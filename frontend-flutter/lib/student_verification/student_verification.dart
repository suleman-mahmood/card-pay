import 'dart:async';
import 'package:cardpay/services/auth.dart';
import 'package:cardpay/shared/shared.dart';
import 'package:flutter/material.dart';

class StudentVerificationScreen extends StatefulWidget {
  const StudentVerificationScreen({Key? key}) : super(key: key);

  @override
  State<StudentVerificationScreen> createState() =>
      _StudentVerificationScreenState();
}

class _StudentVerificationScreenState extends State<StudentVerificationScreen> {
  int secondsRemaining = 300;
  bool enableResend = false;
  late Timer timer;

  @override
  initState() {
    super.initState();
    timer = Timer.periodic(Duration(seconds: 1), (_) {
      if (secondsRemaining != 0) {
        setState(() {
          secondsRemaining--;
        });
      } else {
        setState(() {
          enableResend = true;
        });
      }
    });
  }

  @override
  dispose() {
    timer.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return AuthLayoutCustomWidget(
      children: [
        MainHeadingTypographyCustomWidget(
          content: "A verification email has been sent to your outlook",
        ),
        SizedBox(height: 20),
        SubHeadingTypographyCustomWidget(
          content:
              "Click the link provided to complete registration and then Sign In again",
        ),
        SizedBox(height: 20),
        MediumBodyTypographyCustomWidget(
          content:
              "Note: Check your junk folder if you are having trouble finding the email",
        ),
        SizedBox(height: 20),
        TextButtonCustomWidget(
          content: "Proceed to login",
          onPressed: () async {
            await AuthService().signOut();
            Navigator.pushNamed(context, '/login');
          },
        ),
        SizedBox(height: 30),
        MediumBodyTypographyCustomWidget(
          content: "Didn't get verification email?",
        ),
        TextButtonCustomWidget(
          content: "Resend email verification",
          onPressed: () async {
            if (!enableResend) return;
            await AuthService().sendEmailVerification();
            setState(() {
              secondsRemaining = 300;
              enableResend = false;
            });
          },
        ),
        SmallBodyTypographyCustomWidget(
          content: "after $secondsRemaining seconds",
        ),
      ],
    );
  }
}
