import 'package:flutter/material.dart';
import 'package:auto_route/auto_route.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:frontend_futter/src/config/router/app_router.dart';
import 'package:frontend_futter/src/config/themes/colors.dart';
import 'package:frontend_futter/src/presentation/widgets/boxes/height_box.dart';
import 'package:frontend_futter/src/presentation/widgets/boxes/width_between.dart';
import 'package:frontend_futter/src/presentation/widgets/layout/auth_layout.dart';
import 'package:frontend_futter/src/config/animations/app_animations.dart';
import 'package:frontend_futter/src/presentation//widgets/actions/button/primary_button.dart';
import 'package:frontend_futter/src/utils/constants/signUp_string.dart';

@RoutePage()
class IntroView extends HookWidget {
  const IntroView({super.key});

  @override
  Widget build(BuildContext context) {
    final fadeAnimation = useFadeAnimation(
      begin: 0.0,
      end: 1.0,
      duration: const Duration(milliseconds: 2000),
    );
    final imageAnimationOffset = useSlideAnimation(
      begin: const Offset(0.0, -1.0),
      end: Offset.zero,
      duration: const Duration(milliseconds: 2000),
    );

    return AuthLayout(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          SlideTransition(
            position: imageAnimationOffset,
            child: Image.asset('assets/images/transection.png'),
          ),
          const Text(
            AppStrings.revolution,
            textAlign: TextAlign.center,
            style: AppTypography.introHeading,
          ),
          const HeightBox(slab: 2),
          FadeTransition(
            opacity: fadeAnimation,
            child: PrimaryButton(
              text: AppStrings.start,
              onPressed: () {
                context.router.push(const SignupRoute());
              },
            ),
          ),
          const HeightBox(slab: 2),
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Text(
                AppStrings.alreadyHaveAccount,
                style: AppTypography.bodyText,
              ),
              const WidthBetween(),
              GestureDetector(
                onTap: () {
                  context.router.push(const LoginRoute());
                },
                child: const Text(
                  AppStrings.logIn,
                  style: AppTypography.linkText,
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}
