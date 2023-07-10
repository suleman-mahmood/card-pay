import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:auto_route/auto_route.dart';
import 'package:frontend_futter/src/config/router/app_router.dart';
import 'package:frontend_futter/src/config/themes/colors.dart';

@RoutePage()
class SplashView extends HookWidget {
  const SplashView({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () => _navigateToIntroRoute(context),
      child: _buildBackground(),
    );
  }

  Widget _buildBackground() {
    return Container(
      decoration: BoxDecoration(
        gradient: LinearGradient(
          colors: AppColors.animationHomeGradient.colors,
          begin: Alignment.topCenter,
          end: Alignment.bottomCenter,
          stops: AppColors.animationHomeGradient.stops,
        ),
      ),
      child: Center(
        child: Image.asset(
          'assets/images/logo.png',
        ),
      ),
    );
  }

  void _navigateToIntroRoute(BuildContext context) {
    context.router.push(const IntroRoute());
  }
}
