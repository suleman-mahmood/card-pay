import 'package:auto_route/auto_route.dart';
import 'package:frontend_futter/src/presentation/views/splash_view.dart';
import 'package:frontend_futter/src/presentation/views/intro_view.dart';
import 'package:frontend_futter/src/presentation/views/signup_view.dart';
import 'package:frontend_futter/src/presentation/views/register_organisation_view.dart';
import 'package:frontend_futter/src/presentation/views/register_rollnumber_view.dart';
import 'package:frontend_futter/src/presentation/views/login_view.dart';

part 'app_router.gr.dart';

@AutoRouterConfig(replaceInRouteName: 'View,Route')
class AppRouter extends _$AppRouter {
  @override
  List<AutoRoute> get routes => [
        AutoRoute(page: SplashRoute.page, initial: true),
        CustomRoute(
          page: IntroRoute.page,
          transitionsBuilder: TransitionsBuilders.slideLeft,
        ),
        CustomRoute(
          page: SignupRoute.page,
          transitionsBuilder: TransitionsBuilders.slideLeft,
        ),
        CustomRoute(
          page: RegisterRoute.page,
          transitionsBuilder: TransitionsBuilders.slideLeft,
        ),
        CustomRoute(
          page: RegisterrollRoute.page,
          transitionsBuilder: TransitionsBuilders.slideLeft,
        ),
        CustomRoute(
          page: LoginRoute.page,
          transitionsBuilder: TransitionsBuilders.slideLeft,
        ),
      ];
}
