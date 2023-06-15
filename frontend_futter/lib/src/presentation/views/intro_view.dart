import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:auto_route/auto_route.dart';
import 'package:frontend_futter/src/config/router/app_router.dart';
import 'package:frontend_futter/src/presentation/Widgets/button/primary_button.dart';
import 'package:frontend_futter/src/config/themes/colors.dart';

@RoutePage()
class IntroView extends HookWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Container(
          padding: EdgeInsets.symmetric(horizontal: 20),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Expanded(
                flex: 3,
                child: Image.asset('assets/images/transection.png'),
              ),
              const SizedBox(height: 10),
              Text(
                'Revolutionise ',
                style: AppColors().mainHeading.copyWith(
                      fontSize: 45,
                    ),
                textAlign: TextAlign.center,
              ),
              Text(
                'Your ',
                style: AppColors().mainHeading.copyWith(
                      fontSize: 45,
                    ),
                textAlign: TextAlign.center,
              ),
              Text(
                'Transactions ',
                style: AppColors().mainHeading.copyWith(
                      fontSize: 45,
                    ),
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 5),
              CustomButton(
                text: 'Get Started',
                onPressed: () {
                  context.router.push(SignupRoute());
                },
              ),
              Container(
                padding: EdgeInsets.only(bottom: 20), // Add padding here

                child: GestureDetector(
                  onTap: () {
                    context.router.push(LoginRoute());
                  },
                  child: RichText(
                    text: TextSpan(
                      text: 'Already have an account? ',
                      style: AppColors().inputFont.copyWith(
                            color: AppColors().blackColor,
                          ),
                      children: [
                        TextSpan(
                            text: 'Log In',
                            style: AppColors().inputFont.copyWith(
                                  color: AppColors().primaryColor,
                                )),
                      ],
                    ),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
