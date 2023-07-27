import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:auto_route/auto_route.dart';
import 'package:cardpay/src/config/router/app_router.dart';
import 'package:cardpay/src/config/themes/colors.dart';

@RoutePage()
class SplashView extends HookWidget {
  const SplashView({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    void _navigateToIntroRoute(BuildContext context) {
      context.router.push(const IntroRoute());
    }

    useEffect(() {
      Future.delayed(const Duration(seconds: 1), () {
        _navigateToIntroRoute(context);
      });
    }, []);

    _buildBackground() {
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

    return _buildBackground();
  }
}
