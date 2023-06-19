import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:auto_route/auto_route.dart';
import 'package:frontend_futter/src/config/router/app_router.dart';
import 'package:frontend_futter/src/presentation/Widgets/button/primary_button.dart';
import 'package:frontend_futter/src/config/themes/colors.dart';
import 'package:frontend_futter/src/presentation/Widgets/layout/common_app_layout.dart';

@RoutePage()
class IntroView extends HookWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 20),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Expanded(
                flex: 3,
                child: FractionallySizedBox(
                  widthFactor: 0.6, // Adjust the width factor as needed
                  heightFactor: 0.6, // Adjust the height factor as needed
                  child: Image.asset('assets/images/transection.png'),
                ),
              ),
              Column(
                children: [
                  Text(
                    'Revolutions Your',
                    style: AppTypography.mainHeading.copyWith(
                      fontSize: 42,
                    ),
                  ),
                  Text(
                    'Transactions',
                    style: AppTypography.mainHeading.copyWith(
                      fontSize: 42,
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 5),
              CustomButton(
                text: 'Get Started',
                onPressed: () {
                  context.router.push(SignupRoute());
                },
              ),
              const SizedBox(height: 20),
              GestureDetector(
                onTap: () {
                  context.router.push(LoginRoute());
                },
                child: RichText(
                  text: TextSpan(
                    text: 'Already have an account? ',
                    style: TextStyle(
                      color: AppColors.blackColor,
                    ),
                    children: [
                      TextSpan(
                        text: 'Log In',
                        style: TextStyle(
                          color: AppColors.primaryColor,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ],
                  ),
                ),
              ),
              const SizedBox(height: 70), // Add bottom spacing
            ],
          ),
        ),
      ),
    );
  }
}
