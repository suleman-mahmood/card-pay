import 'package:cardpay/shared/layouts/auth.dart';
import 'package:cardpay/shared/typography/main_heading.dart';
import 'package:flutter/material.dart';

class ForgotPasswordScreen extends StatelessWidget {
  const ForgotPasswordScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return const AuthLayoutWidget(
      children: [
        MainHeadingWidget(
          content: "Forgot password feature coming soon.\n Stay tuned!!!",
        ),
      ],
    );
  }
}
