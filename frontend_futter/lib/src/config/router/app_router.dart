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
        AutoRoute(page: IntroRoute.page),
        AutoRoute(page: SignupRoute.page),
        AutoRoute(page: RegisterRoute.page),
        AutoRoute(page: RegisterrollRoute.page),
        AutoRoute(page: LoginRoute.page),
      ];
}
