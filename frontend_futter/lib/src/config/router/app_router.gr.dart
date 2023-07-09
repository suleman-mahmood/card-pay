// GENERATED CODE - DO NOT MODIFY BY HAND

// **************************************************************************
// AutoRouterGenerator
// **************************************************************************

// ignore_for_file: type=lint
// coverage:ignore-file

part of 'app_router.dart';

abstract class _$AppRouter extends RootStackRouter {
  // ignore: unused_element
  _$AppRouter({super.navigatorKey});

  @override
  final Map<String, PageFactory> pagesMap = {
    DashboardRoute.name: (routeData) {
      return AutoRoutePage<dynamic>(
        routeData: routeData,
        child: const DashboardView(),
      );
    },
    DepositRoute.name: (routeData) {
      return AutoRoutePage<dynamic>(
        routeData: routeData,
        child: const DepositView(),
      );
    },
    IntroRoute.name: (routeData) {
      return AutoRoutePage<dynamic>(
        routeData: routeData,
        child: IntroView(),
      );
    },
    LoginRoute.name: (routeData) {
      return AutoRoutePage<dynamic>(
        routeData: routeData,
        child: const LoginView(),
      );
    },
    AuthRoute.name: (routeData) {
      return AutoRoutePage<dynamic>(
        routeData: routeData,
        child: AuthView(),
      );
    },
    RegisterRoute.name: (routeData) {
      return AutoRoutePage<dynamic>(
        routeData: routeData,
        child: const RegisterView(),
      );
    },
    RequestAmountRoute.name: (routeData) {
      final args = routeData.argsAs<RequestAmountRouteArgs>();
      return AutoRoutePage<dynamic>(
        routeData: routeData,
        child: RequestAmountView(rollNumber: args.rollNumber),
      );
    },
    RequestRoute.name: (routeData) {
      return AutoRoutePage<dynamic>(
        routeData: routeData,
        child: const RequestView(),
      );
    },
    SendRoute.name: (routeData) {
      final args = routeData.argsAs<SendRouteArgs>();
      return AutoRoutePage<dynamic>(
        routeData: routeData,
        child: SendView(rollNumber: args.rollNumber),
      );
    },
    SignupRoute.name: (routeData) {
      return AutoRoutePage<dynamic>(
        routeData: routeData,
        child: const SignupView(),
      );
    },
    SplashRoute.name: (routeData) {
      return AutoRoutePage<dynamic>(
        routeData: routeData,
        child: const SplashView(),
      );
    },
    TransferRoute.name: (routeData) {
      return AutoRoutePage<dynamic>(
        routeData: routeData,
        child: const TransferView(),
      );
    },
    HistroyRoute.name: (routeData) {
      return AutoRoutePage<dynamic>(
        routeData: routeData,
        child: const HistroyView(),
      );
    },
    ConfirmationRoute.name: (routeData) {
      return AutoRoutePage<dynamic>(
        routeData: routeData,
        child: const ConfirmationView(),
      );
    },
    FilterHistoryRoute.name: (routeData) {
      return AutoRoutePage<dynamic>(
        routeData: routeData,
        child: const FilterHistoryView(),
      );
    },
  };
}

/// generated route for
/// [DashboardView]
class DashboardRoute extends PageRouteInfo<void> {
  const DashboardRoute({List<PageRouteInfo>? children})
      : super(
          DashboardRoute.name,
          initialChildren: children,
        );

  static const String name = 'DashboardRoute';

  static const PageInfo<void> page = PageInfo<void>(name);
}

/// generated route for
/// [DepositView]
class DepositRoute extends PageRouteInfo<void> {
  const DepositRoute({List<PageRouteInfo>? children})
      : super(
          DepositRoute.name,
          initialChildren: children,
        );

  static const String name = 'DepositRoute';

  static const PageInfo<void> page = PageInfo<void>(name);
}

/// generated route for
/// [IntroView]
class IntroRoute extends PageRouteInfo<void> {
  const IntroRoute({List<PageRouteInfo>? children})
      : super(
          IntroRoute.name,
          initialChildren: children,
        );

  static const String name = 'IntroRoute';

  static const PageInfo<void> page = PageInfo<void>(name);
}

/// generated route for
/// [LoginView]
class LoginRoute extends PageRouteInfo<void> {
  const LoginRoute({List<PageRouteInfo>? children})
      : super(
          LoginRoute.name,
          initialChildren: children,
        );

  static const String name = 'LoginRoute';

  static const PageInfo<void> page = PageInfo<void>(name);
}

/// generated route for
/// [AuthView]
class AuthRoute extends PageRouteInfo<void> {
  const AuthRoute({List<PageRouteInfo>? children})
      : super(
          AuthRoute.name,
          initialChildren: children,
        );

  static const String name = 'AuthRoute';

  static const PageInfo<void> page = PageInfo<void>(name);
}

/// generated route for
/// [RegisterView]
class RegisterRoute extends PageRouteInfo<void> {
  const RegisterRoute({List<PageRouteInfo>? children})
      : super(
          RegisterRoute.name,
          initialChildren: children,
        );

  static const String name = 'RegisterRoute';

  static const PageInfo<void> page = PageInfo<void>(name);
}

/// generated route for
/// [RequestAmountView]
class RequestAmountRoute extends PageRouteInfo<RequestAmountRouteArgs> {
  RequestAmountRoute({
    required String rollNumber,
    List<PageRouteInfo>? children,
  }) : super(
          RequestAmountRoute.name,
          args: RequestAmountRouteArgs(rollNumber: rollNumber),
          initialChildren: children,
        );

  static const String name = 'RequestAmountRoute';

  static const PageInfo<RequestAmountRouteArgs> page =
      PageInfo<RequestAmountRouteArgs>(name);
}

class RequestAmountRouteArgs {
  const RequestAmountRouteArgs({required this.rollNumber});

  final String rollNumber;

  @override
  String toString() {
    return 'RequestAmountRouteArgs{rollNumber: $rollNumber}';
  }
}

/// generated route for
/// [RequestView]
class RequestRoute extends PageRouteInfo<void> {
  const RequestRoute({List<PageRouteInfo>? children})
      : super(
          RequestRoute.name,
          initialChildren: children,
        );

  static const String name = 'RequestRoute';

  static const PageInfo<void> page = PageInfo<void>(name);
}

/// generated route for
/// [SendView]
class SendRoute extends PageRouteInfo<SendRouteArgs> {
  SendRoute({
    required String rollNumber,
    List<PageRouteInfo>? children,
  }) : super(
          SendRoute.name,
          args: SendRouteArgs(rollNumber: rollNumber),
          initialChildren: children,
        );

  static const String name = 'SendRoute';

  static const PageInfo<SendRouteArgs> page = PageInfo<SendRouteArgs>(name);
}

class SendRouteArgs {
  const SendRouteArgs({required this.rollNumber});

  final String rollNumber;

  @override
  String toString() {
    return 'SendRouteArgs{rollNumber: $rollNumber}';
  }
}

/// generated route for
/// [SignupView]
class SignupRoute extends PageRouteInfo<void> {
  const SignupRoute({List<PageRouteInfo>? children})
      : super(
          SignupRoute.name,
          initialChildren: children,
        );

  static const String name = 'SignupRoute';

  static const PageInfo<void> page = PageInfo<void>(name);
}

/// generated route for
/// [SplashView]
class SplashRoute extends PageRouteInfo<void> {
  const SplashRoute({List<PageRouteInfo>? children})
      : super(
          SplashRoute.name,
          initialChildren: children,
        );

  static const String name = 'SplashRoute';

  static const PageInfo<void> page = PageInfo<void>(name);
}

/// generated route for
/// [TransferView]
class TransferRoute extends PageRouteInfo<void> {
  const TransferRoute({List<PageRouteInfo>? children})
      : super(
          TransferRoute.name,
          initialChildren: children,
        );

  static const String name = 'TransferRoute';

  static const PageInfo<void> page = PageInfo<void>(name);
}

/// generated route for
/// [HistroyView]
class HistroyRoute extends PageRouteInfo<void> {
  const HistroyRoute({List<PageRouteInfo>? children})
      : super(
          HistroyRoute.name,
          initialChildren: children,
        );

  static const String name = 'HistroyRoute';

  static const PageInfo<void> page = PageInfo<void>(name);
}

/// generated route for
/// [ConfirmationView]
class ConfirmationRoute extends PageRouteInfo<void> {
  const ConfirmationRoute({List<PageRouteInfo>? children})
      : super(
          ConfirmationRoute.name,
          initialChildren: children,
        );

  static const String name = 'ConfirmationRoute';

  static const PageInfo<void> page = PageInfo<void>(name);
}

/// generated route for
/// [FilterHistoryView]
class FilterHistoryRoute extends PageRouteInfo<void> {
  const FilterHistoryRoute({List<PageRouteInfo>? children})
      : super(
          FilterHistoryRoute.name,
          initialChildren: children,
        );

  static const String name = 'FilterHistoryRoute';

  static const PageInfo<void> page = PageInfo<void>(name);
}
