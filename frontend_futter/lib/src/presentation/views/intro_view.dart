import 'package:cardpay/src/presentation/cubits/remote/versions_cubit.dart';
import 'package:flutter/material.dart';
import 'package:auto_route/auto_route.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:cardpay/src/config/router/app_router.dart';
import 'package:cardpay/src/config/themes/colors.dart';
import 'package:cardpay/src/presentation/widgets/boxes/height_box.dart';
import 'package:cardpay/src/presentation/widgets/boxes/width_between.dart';
import 'package:cardpay/src/presentation/widgets/layout/auth_layout.dart';
import 'package:cardpay/src/config/animations/app_animations.dart';
import 'package:cardpay/src/presentation//widgets/actions/button/primary_button.dart';
import 'package:cardpay/src/utils/constants/signUp_string.dart';

@RoutePage()
class IntroView extends HookWidget {
  const IntroView({super.key});

  @override
  Widget build(BuildContext context) {
    final versionCubit = BlocProvider.of<VersionsCubit>(context);

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
      showBackButton: false,
      child: SingleChildScrollView(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const HeightBox(slab: 3),
            SlideTransition(
              position: imageAnimationOffset,
              child: Image.asset('assets/images/transection.png'),
            ),
            Text(
              AppStrings.revolution,
              textAlign: TextAlign.center,
              style: AppTypography.introHeading,
            ),
            const HeightBox(slab: 3),
            FadeTransition(
              opacity: fadeAnimation,
              child: PrimaryButton(
                text: AppStrings.start,
                onPressed: () {
                  versionCubit.getVersions();
                  context.router.push(const SignupRoute());
                },
              ),
            ),
            const HeightBox(slab: 3),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Text(
                  AppStrings.alreadyHaveAccount,
                  style: AppTypography.bodyText,
                ),
                const WidthBetween(),
                GestureDetector(
                  onTap: () {
                    versionCubit.getVersions();
                    context.router.push(const LoginRoute());
                  },
                  child: Text(
                    AppStrings.logIn,
                    style: AppTypography.linkText,
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
