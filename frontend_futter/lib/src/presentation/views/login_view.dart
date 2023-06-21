import 'package:flutter/material.dart';
import 'package:auto_route/auto_route.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:frontend_futter/src/config/themes/colors.dart';
import 'package:frontend_futter/src/presentation/Widgets/headings/main_heading.dart';
import 'package:frontend_futter/src/presentation/Widgets/input_fields/input_field.dart';
import 'package:frontend_futter/src/presentation/Widgets/button/primary_button.dart';
import 'package:frontend_futter/src/config/router/app_router.dart';
import 'package:frontend_futter/src/presentation/Widgets/layout/auth_layout.dart';

@RoutePage()
class LoginView extends HookWidget {
  const LoginView({Key? key}) : super(key: key);

  void handleLoginButtonPressed(BuildContext context) {
    context.router.push(RegisterRoute());
  }

  @override
  Widget build(BuildContext context) {
    final screenHeight = MediaQuery.of(context).size.height;
    final screenWidth = MediaQuery.of(context).size.width;

    return AuthLayout(
      child: SingleChildScrollView(
        physics: AlwaysScrollableScrollPhysics(),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            SizedBox(height: screenHeight * 0.22),
            MainHeading(
              accountTitle: 'Login',
            ),
            SizedBox(height: screenHeight * 0.005),
            CustomInputField(
              label: 'Email Address',
              hint: 'Enter your email address',
              obscureText: false,
            ),
            SizedBox(height: screenHeight * 0.015),
            CustomInputField(
              label: 'PASSWORD',
              hint: 'Enter your password',
              obscureText: true,
            ),
            SizedBox(height: screenHeight * 0.005),
            Text(
              'Forgot Password?',
              style: AppTypography.headingFont.copyWith(
                fontSize: screenWidth * 0.04,
                color: AppColors.primaryColor,
              ),
            ),
            CustomButton(
              text: 'Login',
              onPressed: () => handleLoginButtonPressed(context),
            ),
          ],
        ),
      ),
    );
  }
}
