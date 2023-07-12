import 'package:cardpay/src/presentation/widgets/boxes/height_box.dart';
import 'package:flutter/material.dart';
import 'package:auto_route/auto_route.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:cardpay/src/config/screen_utills/screen_util.dart';
import 'package:cardpay/src/config/themes/colors.dart';
import 'package:cardpay/src/config/router/app_router.dart';
import 'package:cardpay/src/presentation/widgets/actions/button/primary_button.dart';
import 'package:cardpay/src/presentation/widgets/headings/main_heading.dart';
import 'package:cardpay/src/presentation/widgets/layout/auth_layout.dart';
import 'package:cardpay/src/presentation/widgets/text_inputs/input_field.dart';
import 'package:cardpay/src/utils/constants/signUp_string.dart';

@RoutePage()
class LoginView extends HookWidget {
  const LoginView({Key? key}) : super(key: key);

  void handleLoginButtonPressed(BuildContext context) {
    context.router.push(const DashboardRoute());
  }

  @override
  Widget build(BuildContext context) {
    return AuthLayout(
      child: SingleChildScrollView(
        physics: const AlwaysScrollableScrollPhysics(),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            SizedBox(height: ScreenUtil.heightMultiplier(context) * 22),
            const MainHeading(
              accountTitle: AppStrings.logIn,
            ),
            HeightBox(slab: 2),
            const CustomInputField(
              label: AppStrings.email,
              hint: AppStrings.enterEmail,
              obscureText: false,
            ),
            HeightBox(slab: 2),
            const CustomInputField(
              label: AppStrings.password,
              hint: AppStrings.enterPassword,
              obscureText: true,
            ),
            HeightBox(slab: 1),
            Text(AppStrings.forgot, style: AppTypography.linkText),
            HeightBox(slab: 3),
            PrimaryButton(
              text: AppStrings.logIn,
              onPressed: () => handleLoginButtonPressed(context),
            ),
          ],
        ),
      ),
    );
  }
}
