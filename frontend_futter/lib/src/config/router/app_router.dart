import 'package:auto_route/auto_route.dart';
import 'package:cardpay/src/presentation/views/feature_service/faqs_view.dart';
import 'package:cardpay/src/presentation/views/feature_service/help_view.dart';
import 'package:cardpay/src/presentation/views/transaction_service/payment_dashboard_view.dart';
import 'package:cardpay/src/presentation/views/transaction_service/qr_view.dart';
import 'package:cardpay/src/presentation/views/feature_service/profile_view.dart';
import 'package:cardpay/src/presentation/views/splash_view.dart';
import 'package:cardpay/src/presentation/views/intro_view.dart';
import 'package:cardpay/src/presentation/views/authentification_service/signup_view.dart';
import 'package:cardpay/src/presentation/views/authentification_service/register_organisation_view.dart';
import 'package:cardpay/src/presentation/views/authentification_service/login_view.dart';
import 'package:cardpay/src/presentation/views/authentification_service/pin_view.dart';
import 'package:cardpay/src/presentation/views/dashboard_view.dart';
import 'package:cardpay/src/presentation/views/transaction_service/deposite_view.dart';
import 'package:cardpay/src/presentation/views/transaction_service/transfer_view.dart';
import 'package:cardpay/src/presentation/views/transaction_service/request_view.dart';
import 'package:cardpay/src/presentation/views/transaction_service/send_view.dart';
import 'package:cardpay/src/presentation/views/transaction_service/history_transaction_view.dart';
import 'package:cardpay/src/presentation/views/transaction_service/request_amount_view.dart';
import 'package:cardpay/src/presentation/views/transaction_service/filtered_history_view.dart';
import 'package:cardpay/src/presentation/views/transaction_service/confirmation_view.dart';
import 'package:cardpay/src/presentation/views/feature_service/edit_profile_view.dart';

import 'package:flutter/material.dart';

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
          page: RegisterOrganizationRoute.page,
          transitionsBuilder: TransitionsBuilders.slideLeft,
        ),
        CustomRoute(
          page: LoginRoute.page,
          transitionsBuilder: TransitionsBuilders.slideLeft,
        ),
        CustomRoute(
          page: PinRoute.page,
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
          page: TransactionHistoryRoute.page,
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
        ),
        CustomRoute(
          page: PaymentDashboardRoute.page,
          transitionsBuilder: TransitionsBuilders.slideLeft,
        ),
        CustomRoute(
          page: FaqsRoute.page,
          transitionsBuilder: TransitionsBuilders.slideLeft,
        ),
        CustomRoute(
          page: HelpRoute.page,
          transitionsBuilder: TransitionsBuilders.slideLeft,
        ),
        CustomRoute(
          page: ProfileRoute.page,
          transitionsBuilder: TransitionsBuilders.slideLeft,
        ),
        CustomRoute(
          page: QrRoute.page,
          transitionsBuilder: TransitionsBuilders.slideLeft,
        ),
        CustomRoute(
          page: EditProfileRoute.page,
          transitionsBuilder: TransitionsBuilders.slideLeft,
        ),
      ];
}
