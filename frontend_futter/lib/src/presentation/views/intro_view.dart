import 'package:flutter/material.dart';
import 'package:auto_route/auto_route.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:frontend_futter/src/config/router/app_router.dart';
import 'package:frontend_futter/src/config/screen_utills/screen_util.dart';
import 'package:frontend_futter/src/config/themes/colors.dart';
import 'package:frontend_futter/src/presentation/widgets/layout/auth_layout.dart';
import 'package:frontend_futter/src/config/animations/app_animations.dart';
import 'package:frontend_futter/src/presentation//widgets/actions/button/primary_button.dart';
import 'package:frontend_futter/src/utils/constants/signUp_string.dart';

@RoutePage()
class IntroView extends HookWidget {
  @override
  Widget build(BuildContext context) {
    final _fadeAnimation = useFadeAnimation(
      begin: 0.0,
      end: 1.0,
      duration: Duration(milliseconds: 2000),
    );
    final _imageAnimationOffset = useSlideAnimation(
      begin: Offset(0.0, -1.0),
      end: Offset.zero,
      duration: Duration(milliseconds: 2000),
    );

    return AuthLayout(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          SlideTransition(
            position: _imageAnimationOffset,
            child: Image.asset('assets/images/transection.png'),
          ),
          Column(
            children: [
              Text(
                AppStrings.revolution,
                style: AppTypography.mainHeading.copyWith(
                  fontSize: ScreenUtil.textMultiplier(context) *
                      4.3, // use ScreenUtil
                ),
              ),
              Text(
                AppStrings.transactions,
                style: AppTypography.mainHeading.copyWith(
                  fontSize: ScreenUtil.textMultiplier(context) *
                      4.3, // use ScreenUtil
                ),
              ),
            ],
          ),
          SizedBox(
              height:
                  ScreenUtil.heightMultiplier(context) * 0.5), // use ScreenUtil
          FadeTransition(
            opacity: _fadeAnimation,
            child: CustomButton(
              text: AppStrings.start,
              onPressed: () {
                context.router.push(SignupRoute());
              },
            ),
          ),
          SizedBox(
              height:
                  ScreenUtil.heightMultiplier(context) * 2), // use ScreenUtil
          GestureDetector(
            onTap: () {
              context.router.push(LoginRoute());
            },
            child: RichText(
              text: TextSpan(
                text: AppStrings.alreadyHaveAccount,
                style: TextStyle(
                  color: AppColors.blackColor,
                  fontSize:
                      ScreenUtil.textMultiplier(context) * 2, // use ScreenUtil
                ),
                children: [
                  TextSpan(
                    text: AppStrings.logIn,
                    style: TextStyle(
                      color: AppColors.primaryColor,
                      fontWeight: FontWeight.bold,
                      fontSize: ScreenUtil.textMultiplier(context) *
                          2, // use ScreenUtil
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
