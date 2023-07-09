import 'package:auto_route/auto_route.dart';
import 'package:frontend_futter/src/presentation/views/splash_view.dart';
import 'package:frontend_futter/src/presentation/views/intro_view.dart';
import 'package:frontend_futter/src/presentation/views/signup_view.dart';
import 'package:frontend_futter/src/presentation/views/register_organisation_view.dart';
import 'package:frontend_futter/src/presentation/views/login_view.dart';
import 'package:frontend_futter/src/presentation/views/pin_view.dart';
import 'package:frontend_futter/src/presentation/views/dashboard_view.dart';
import 'package:frontend_futter/src/presentation/views/deposite_view.dart';
import 'package:frontend_futter/src/presentation/views/transfer_view.dart';
import 'package:frontend_futter/src/presentation/views/request_view.dart';
import 'package:frontend_futter/src/presentation/views/send_view.dart';
import 'package:frontend_futter/src/presentation/views/history_transaction_view.dart';
import 'package:frontend_futter/src/presentation/views/request_amount_view.dart';
import 'package:frontend_futter/src/presentation/views/filtered_history_view.dart';
import 'package:frontend_futter/src/presentation/views/confirmation_view.dart';

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
          page: LoginRoute.page,
          transitionsBuilder: TransitionsBuilders.slideLeft,
        ),
        CustomRoute(
          page: AuthRoute.page,
          transitionsBuilder: TransitionsBuilders.slideLeft,
        ),
        CustomRoute(
          page: DashboardRoute.page,
          transitionsBuilder: TransitionsBuilders.slideLeft,
        ),
        CustomRoute(
          page: DepositRoute.page,
          transitionsBuilder: TransitionsBuilders.slideLeft,
        ),
        CustomRoute(
          page: TransferRoute.page,
          transitionsBuilder: TransitionsBuilders.slideLeft,
        ),
        CustomRoute(
          page: RequestRoute.page,
          transitionsBuilder: TransitionsBuilders.slideLeft,
        ),
        CustomRoute(
          page: SendRoute.page,
          transitionsBuilder: TransitionsBuilders.slideLeft,
        ),
        CustomRoute(
          page: HistroyRoute.page,
          transitionsBuilder: TransitionsBuilders.slideLeft,
        ),
        CustomRoute(
          page: RequestAmountRoute.page,
          transitionsBuilder: TransitionsBuilders.slideLeft,
        ),
        CustomRoute(
          page: FilterHistoryRoute.page,
          transitionsBuilder: TransitionsBuilders.slideLeft,
        ),
        CustomRoute(
          page: ConfirmationRoute.page,
          transitionsBuilder: TransitionsBuilders.slideLeft,
        )
      ];
}
