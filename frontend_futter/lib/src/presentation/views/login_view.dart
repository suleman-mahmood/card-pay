import 'package:cardpay/src/presentation/widgets/boxes/height_box.dart';
import 'package:flutter/material.dart';
import 'package:auto_route/auto_route.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:cardpay/src/config/themes/colors.dart';
import 'package:cardpay/src/config/router/app_router.dart';
import 'package:cardpay/src/presentation/widgets/actions/button/primary_button.dart';
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
    final formKey = useMemoized(() => GlobalKey<FormState>());

    return AuthLayout(
      child: SingleChildScrollView(
        physics: const AlwaysScrollableScrollPhysics(),
        child: Form(
          key: formKey,
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              HeightBox(slab: 4),
              Align(
                alignment: Alignment.centerLeft,
                child: const Text(
                  AppStrings.logIn,
                  style: AppTypography.introHeading,
                ),
              ),
              HeightBox(slab: 4),
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
              Align(
                alignment: Alignment.centerRight,
                child: Text(AppStrings.forgot,
                    style: AppTypography.subHeadingBold),
              ),
              HeightBox(slab: 3),
              PrimaryButton(
                text: AppStrings.logIn,
                onPressed: () {
                  if (formKey.currentState!.validate()) {
                    handleLoginButtonPressed(context);
                  }
                },
              ),
            ],
          ),
        ),
      ),
    );
  }
}
