import 'package:auto_route/auto_route.dart';
import 'package:cardpay/src/config/router/app_router.dart';
import 'package:firebase_auth/firebase_auth.dart';

class SplashGuard extends AutoRouteGuard {
  @override
  void onNavigation(NavigationResolver resolver, StackRouter router) {
    resolver.next(true);

    if (FirebaseAuth.instance.currentUser != null) {
      // Race conditions and stuff
      Future.delayed(
        const Duration(seconds: 1),
        () => resolver.redirect(DashboardLayoutRoute()),
      );
    } else {
      // Race conditions and stuff
      Future.delayed(
        const Duration(seconds: 1),
        () => resolver.redirect(const IntroRoute()),
      );
    }
  }
}
