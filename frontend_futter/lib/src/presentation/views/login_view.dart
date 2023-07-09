import 'package:flutter/material.dart';
import 'package:auto_route/auto_route.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:frontend_futter/src/config/screen_utills/screen_util.dart';
import 'package:frontend_futter/src/config/themes/colors.dart';
import 'package:frontend_futter/src/config/router/app_router.dart';
import 'package:frontend_futter/src/presentation/widgets/actions/button/primary_button.dart';
import 'package:frontend_futter/src/presentation/widgets/headings/main_heading.dart';
import 'package:frontend_futter/src/presentation/widgets/layout/auth_layout.dart';
import 'package:frontend_futter/src/presentation/widgets/text_inputs/input_field.dart';
import 'package:frontend_futter/src/utils/constants/signUp_string.dart';

@RoutePage()
class LoginView extends HookWidget {
  const LoginView({Key? key}) : super(key: key);

  void handleLoginButtonPressed(BuildContext context) {
    context.router.push(DashboardRoute());
  }

  @override
  Widget build(BuildContext context) {
    return AuthLayout(
      child: SingleChildScrollView(
        physics: AlwaysScrollableScrollPhysics(),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            SizedBox(
                height: ScreenUtil.heightMultiplier(context) *
                    22), // Leverage ScreenUtil
            MainHeading(
              accountTitle: AppStrings.logIn,
            ),
            SizedBox(
                height: ScreenUtil.heightMultiplier(context) *
                    0.5), // Leverage ScreenUtil
            CustomInputField(
              label: AppStrings.email,
              hint: AppStrings.enterEmail,
              obscureText: false,
            ),
            SizedBox(
                height: ScreenUtil.heightMultiplier(context) *
                    1.5), // Leverage ScreenUtil
            CustomInputField(
              label: AppStrings.password,
              hint: AppStrings.enterPassword,
              obscureText: true,
            ),
            SizedBox(
                height: ScreenUtil.heightMultiplier(context) *
                    0.5), // Leverage ScreenUtil
            Text(
              AppStrings.forgot,
              style: AppTypography.headingFont.copyWith(
                fontSize: ScreenUtil.textMultiplier(context) *
                    2, // Leverage ScreenUtil
                color: AppColors.primaryColor,
              ),
            ),
            CustomButton(
              text: AppStrings.logIn,
              onPressed: () => handleLoginButtonPressed(context),
            ),
          ],
        ),
      ),
    );
  }
}
