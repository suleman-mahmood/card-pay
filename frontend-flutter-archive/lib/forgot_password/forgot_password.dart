import 'package:cardpay/shared/shared.dart';
import 'package:flutter/material.dart';

class ForgotPasswordScreen extends StatelessWidget {
  const ForgotPasswordScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return const AuthLayoutCustomWidget(
      children: [
        MainHeadingTypographyCustomWidget(
          content: "Forgot password feature coming soon.\n Stay tuned!!!",
        ),
      ],
    );
  }
}
