import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:auto_route/auto_route.dart';
import 'package:frontend_futter/src/config/router/app_router.dart';
import 'package:frontend_futter/src/presentation/Widgets/button/primary_button.dart';
import 'package:frontend_futter/src/config/themes/colors.dart';
import 'package:frontend_futter/src/presentation/Widgets/layout/auth_layout.dart';

@RoutePage()
class IntroView extends HookWidget {
  @override
  Widget build(BuildContext context) {
    final screenHeight = MediaQuery.of(context).size.height;
    final screenWidth = MediaQuery.of(context).size.width;

    return AuthLayout(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Image.asset('assets/images/transection.png'),
          Column(
            children: [
              Text(
                'Revolutions Your',
                style: AppTypography.mainHeading.copyWith(
                  fontSize: screenWidth * 0.1,
                ),
              ),
              Text(
                'Transactions',
                style: AppTypography.mainHeading.copyWith(
                  fontSize: screenWidth * 0.1,
                ),
              ),
            ],
          ),
          SizedBox(height: screenHeight * 0.005),
          CustomButton(
            text: 'Get Started',
            onPressed: () {
              context.router.push(SignupRoute());
            },
          ),
          SizedBox(height: screenHeight * 0.02),
          GestureDetector(
            onTap: () {
              context.router.push(LoginRoute());
            },
            child: RichText(
              text: TextSpan(
                text: 'Already have an account? ',
                style: TextStyle(
                  color: AppColors.blackColor,
                  fontSize: screenWidth * 0.04,
                ),
                children: [
                  TextSpan(
                    text: 'Log In',
                    style: TextStyle(
                      color: AppColors.primaryColor,
                      fontWeight: FontWeight.bold,
                      fontSize: screenWidth * 0.04,
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}
