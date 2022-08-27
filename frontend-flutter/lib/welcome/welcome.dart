import 'package:cardpay/dashboard/dashboard.dart';
import 'package:cardpay/services/auth.dart';
import 'package:cardpay/shared/shared.dart';
import 'package:cardpay/student_verification/student_verification.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';

class WelcomeScreen extends StatelessWidget {
  const WelcomeScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return StreamBuilder<User?>(
      stream: AuthService().userStream,
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          return const Scaffold(
            body: Center(
              child: Text('loading'),
            ),
          );
        } else if (snapshot.hasError) {
          return const Scaffold(
            body: Center(
              child: Text('error'),
            ),
          );
        } else if (snapshot.hasData) {
          // Check if the user has verified his email
          if (!snapshot.data!.emailVerified) {
            return const StudentVerificationScreen();
          }
          // There is data if the user is logged in so goto dashboard
          return const DashboardScreen();
        } else {
          return const WelcomeWidget();
        }
      },
    );
  }
}

class WelcomeWidget extends StatelessWidget {
  const WelcomeWidget({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return AuthLayoutCustomWidget(
      children: [
        MainHeadingTypographyCustomWidget(content: "Welcome to CardPay"),
        SizedBox(height: 15),
        SubHeadingTypographyCustomWidget(
            content: "Revolutionize your campus experience"),
        SizedBox(height: 15),
        TextButtonCustomWidget(
          content: "Continue!",
          onPressed: () => Navigator.pushNamed(context, '/login'),
        ),
      ],
    );
  }
}
