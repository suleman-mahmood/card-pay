import 'package:auto_route/auto_route.dart';
import 'package:cardpay/src/config/router/auth_guard.dart';
import 'package:cardpay/src/config/router/splash_guard.dart';
import 'package:cardpay/src/domain/models/event.dart';
import 'package:cardpay/src/presentation/views/event/event_attendance_qr_view.dart';
import 'package:cardpay/src/presentation/views/event/event_details_view.dart';
import 'package:cardpay/src/presentation/views/event/event_selector_view.dart';
import 'package:cardpay/src/presentation/views/event/live_events_detailed_view.dart';
import 'package:cardpay/src/presentation/views/event/live_events_view.dart';
import 'package:cardpay/src/presentation/views/event/registered_events_view.dart';
import 'package:cardpay/src/presentation/views/faqs_view.dart';
import 'package:cardpay/src/presentation/views/dashboard_layout_view.dart';
import 'package:cardpay/src/presentation/views/intro/intro_view.dart';
import 'package:cardpay/src/presentation/views/intro/splash_view.dart';
import 'package:cardpay/src/presentation/views/intro/splash_view_animated.dart';
import 'package:cardpay/src/presentation/views/payment/deposit_amount_view.dart';
import 'package:cardpay/src/presentation/views/payment/qr_amount_view.dart';
import 'package:cardpay/src/presentation/views/payment/qr_view.dart';
import 'package:cardpay/src/presentation/views/payment/request_amount_view.dart';
import 'package:cardpay/src/presentation/views/payment/request_sender_view.dart';
import 'package:cardpay/src/presentation/views/payment/transfer_amount_view.dart';
import 'package:cardpay/src/presentation/views/payment/transfer_recipient_view.dart';
import 'package:cardpay/src/presentation/views/profile/edit_profile_view.dart';
import 'package:cardpay/src/presentation/views/profile/profile_view.dart';
import 'package:cardpay/src/presentation/views/auth/signup_view.dart';
import 'package:cardpay/src/presentation/views/auth/closed_loop_view.dart';
import 'package:cardpay/src/presentation/views/auth/login_view.dart';
import 'package:cardpay/src/presentation/views/auth/pin_view.dart';
import 'package:cardpay/src/presentation/views/payment/payment_dashboard_view.dart';
import 'package:cardpay/src/presentation/views/payment/transactions_view.dart';
import 'package:cardpay/src/presentation/views/payment/detailed_transactions_view.dart';
import 'package:cardpay/src/presentation/views/payment/receipt_view.dart';

import 'package:flutter/material.dart';

part 'app_router.gr.dart';

@AutoRouterConfig(replaceInRouteName: 'View,Route')
class AppRouter extends _$AppRouter {
  @override
  List<AutoRoute> get routes => [
        CustomRoute(
          initial: true,
          page: SplashRoute.page,
          transitionsBuilder: TransitionsBuilders.slideLeft,
          guards: [SplashGuard()],
        ),
        CustomRoute(
          page: IntroRoute.page,
          transitionsBuilder: TransitionsBuilders.slideLeft,
          guards: [AuthGuard()],
        ),
        CustomRoute(
          page: SignupRoute.page,
          transitionsBuilder: TransitionsBuilders.slideLeft,
        ),
        CustomRoute(
          page: ClosedLoopRoute.page,
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
          page: DashboardLayoutRoute.page,
          transitionsBuilder: TransitionsBuilders.slideLeft,
          guards: [AuthGuard()],
        ),
        CustomRoute(
          page: DepositAmountRoute.page,
          transitionsBuilder: TransitionsBuilders.slideLeft,
        ),
        CustomRoute(
          page: TransferRecipientRoute.page,
          transitionsBuilder: TransitionsBuilders.slideLeft,
        ),
        CustomRoute(
          page: QrAmountRoute.page,
          transitionsBuilder: TransitionsBuilders.slideLeft,
        ),
        CustomRoute(
          page: TransferAmountRoute.page,
          transitionsBuilder: TransitionsBuilders.slideLeft,
        ),
        CustomRoute(
          page: TransactionsRoute.page,
          transitionsBuilder: TransitionsBuilders.slideLeft,
        ),
        CustomRoute(
          page: RequestAmountRoute.page,
          transitionsBuilder: TransitionsBuilders.slideLeft,
        ),
        CustomRoute(
          page: RequestSenderRoute.page,
          transitionsBuilder: TransitionsBuilders.slideLeft,
        ),
        CustomRoute(
          page: DetailedTransactionsRoute.page,
          transitionsBuilder: TransitionsBuilders.slideLeft,
        ),
        CustomRoute(
          page: ReceiptRoute.page,
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
        // Event views
        CustomRoute(
          page: EventSelectorRoute.page,
          transitionsBuilder: TransitionsBuilders.slideLeft,
        ),
        CustomRoute(
          page: LiveEventsRoute.page,
          transitionsBuilder: TransitionsBuilders.slideLeft,
        ),
        CustomRoute(
          page: LiveEventsDetailedRoute.page,
          transitionsBuilder: TransitionsBuilders.slideLeft,
        ),
        CustomRoute(
          page: EventDetailsRoute.page,
          transitionsBuilder: TransitionsBuilders.slideLeft,
        ),
        CustomRoute(
          page: RegisteredEventsRoute.page,
          transitionsBuilder: TransitionsBuilders.slideLeft,
        ),
        CustomRoute(
          page: EventAttendanceQrRoute.page,
          transitionsBuilder: TransitionsBuilders.slideLeft,
        ),
      ];
}
