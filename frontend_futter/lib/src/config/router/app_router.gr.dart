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
    FaqsRoute.name: (routeData) {
      return AutoRoutePage<dynamic>(
        routeData: routeData,
        child: const FaqsView(),
      );
    },
    ConfirmationRoute.name: (routeData) {
      return AutoRoutePage<dynamic>(
        routeData: routeData,
        child: const ConfirmationView(),
      );
    },
    HistroyRoute.name: (routeData) {
      return AutoRoutePage<dynamic>(
        routeData: routeData,
        child: const HistroyView(),
      );
    },
    AuthRoute.name: (routeData) {
      return AutoRoutePage<dynamic>(
        routeData: routeData,
        child: const AuthView(),
      );
    },
    RegisterRoute.name: (routeData) {
      return AutoRoutePage<dynamic>(
        routeData: routeData,
        child: const RegisterView(),
      );
    },
    QrRoute.name: (routeData) {
      return AutoRoutePage<dynamic>(
        routeData: routeData,
        child: const QrView(),
      );
    },
    HelpRoute.name: (routeData) {
      return AutoRoutePage<dynamic>(
        routeData: routeData,
        child: const HelpView(),
      );
    },
    TransferRoute.name: (routeData) {
      return AutoRoutePage<dynamic>(
        routeData: routeData,
        child: const TransferView(),
      );
    },
    DepositRoute.name: (routeData) {
      return AutoRoutePage<dynamic>(
        routeData: routeData,
        child: const DepositView(),
      );
    },
    SplashRoute.name: (routeData) {
      return AutoRoutePage<dynamic>(
        routeData: routeData,
        child: const SplashView(),
      );
    },
    SignupRoute.name: (routeData) {
      return AutoRoutePage<dynamic>(
        routeData: routeData,
        child: const SignupView(),
      );
    },
    PaymentDashboardRoute.name: (routeData) {
      final args = routeData.argsAs<PaymentDashboardRouteArgs>(
          orElse: () => const PaymentDashboardRouteArgs());
      return AutoRoutePage<dynamic>(
        routeData: routeData,
        child: PaymentDashboardView(
          key: args.key,
          showBottomBar: args.showBottomBar,
          backgroundColor: args.backgroundColor,
          useHorizontalPadding: args.useHorizontalPadding,
        ),
      );
    },
    FilterHistoryRoute.name: (routeData) {
      return AutoRoutePage<dynamic>(
        routeData: routeData,
        child: const FilterHistoryView(),
      );
    },
    DashboardRoute.name: (routeData) {
      final args = routeData.argsAs<DashboardRouteArgs>(
          orElse: () => const DashboardRouteArgs());
      return AutoRoutePage<dynamic>(
        routeData: routeData,
        child: DashboardView(
          key: args.key,
          scaffoldKey: args.scaffoldKey,
        ),
      );
    },
    RequestRoute.name: (routeData) {
      return AutoRoutePage<dynamic>(
        routeData: routeData,
        child: const RequestView(),
      );
    },
    RequestAmountRoute.name: (routeData) {
      final args = routeData.argsAs<RequestAmountRouteArgs>();
      return AutoRoutePage<dynamic>(
        routeData: routeData,
        child: RequestAmountView(
          key: args.key,
          uniqueIdentifier: args.uniqueIdentifier,
        ),
      );
    },
    IntroRoute.name: (routeData) {
      return AutoRoutePage<dynamic>(
        routeData: routeData,
        child: const IntroView(),
      );
    },
    LoginRoute.name: (routeData) {
      return AutoRoutePage<dynamic>(
        routeData: routeData,
        child: const LoginView(),
      );
    },
    SendRoute.name: (routeData) {
      final args =
          routeData.argsAs<SendRouteArgs>(orElse: () => const SendRouteArgs());
      return AutoRoutePage<dynamic>(
        routeData: routeData,
        child: SendView(
          key: args.key,
          uniqueIdentifier: args.uniqueIdentifier,
        ),
      );
    },
    ProfileRoute.name: (routeData) {
      final args = routeData.argsAs<ProfileRouteArgs>(
          orElse: () => const ProfileRouteArgs());
      return AutoRoutePage<dynamic>(
        routeData: routeData,
        child: ProfileView(key: args.key),
      );
    },
  };
}

/// generated route for
/// [FaqsView]
class FaqsRoute extends PageRouteInfo<void> {
  const FaqsRoute({List<PageRouteInfo>? children})
      : super(
          FaqsRoute.name,
          initialChildren: children,
        );

  static const String name = 'FaqsRoute';

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
/// [QrView]
class QrRoute extends PageRouteInfo<void> {
  const QrRoute({List<PageRouteInfo>? children})
      : super(
          QrRoute.name,
          initialChildren: children,
        );

  static const String name = 'QrRoute';

  static const PageInfo<void> page = PageInfo<void>(name);
}

/// generated route for
/// [HelpView]
class HelpRoute extends PageRouteInfo<void> {
  const HelpRoute({List<PageRouteInfo>? children})
      : super(
          HelpRoute.name,
          initialChildren: children,
        );

  static const String name = 'HelpRoute';

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
/// [PaymentDashboardView]
class PaymentDashboardRoute extends PageRouteInfo<PaymentDashboardRouteArgs> {
  PaymentDashboardRoute({
    Key? key,
    bool showBottomBar = true,
    Color? backgroundColor,
    bool useHorizontalPadding = true,
    List<PageRouteInfo>? children,
  }) : super(
          PaymentDashboardRoute.name,
          args: PaymentDashboardRouteArgs(
            key: key,
            showBottomBar: showBottomBar,
            backgroundColor: backgroundColor,
            useHorizontalPadding: useHorizontalPadding,
          ),
          initialChildren: children,
        );

  static const String name = 'PaymentDashboardRoute';

  static const PageInfo<PaymentDashboardRouteArgs> page =
      PageInfo<PaymentDashboardRouteArgs>(name);
}

class PaymentDashboardRouteArgs {
  const PaymentDashboardRouteArgs({
    this.key,
    this.showBottomBar = true,
    this.backgroundColor,
    this.useHorizontalPadding = true,
  });

  final Key? key;

  final bool showBottomBar;

  final Color? backgroundColor;

  final bool useHorizontalPadding;

  @override
  String toString() {
    return 'PaymentDashboardRouteArgs{key: $key, showBottomBar: $showBottomBar, backgroundColor: $backgroundColor, useHorizontalPadding: $useHorizontalPadding}';
  }
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

/// generated route for
/// [DashboardView]
class DashboardRoute extends PageRouteInfo<DashboardRouteArgs> {
  DashboardRoute({
    Key? key,
    GlobalKey<ScaffoldState>? scaffoldKey,
    List<PageRouteInfo>? children,
  }) : super(
          DashboardRoute.name,
          args: DashboardRouteArgs(
            key: key,
            scaffoldKey: scaffoldKey,
          ),
          initialChildren: children,
        );

  static const String name = 'DashboardRoute';

  static const PageInfo<DashboardRouteArgs> page =
      PageInfo<DashboardRouteArgs>(name);
}

class DashboardRouteArgs {
  const DashboardRouteArgs({
    this.key,
    this.scaffoldKey,
  });

  final Key? key;

  final GlobalKey<ScaffoldState>? scaffoldKey;

  @override
  String toString() {
    return 'DashboardRouteArgs{key: $key, scaffoldKey: $scaffoldKey}';
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
/// [RequestAmountView]
class RequestAmountRoute extends PageRouteInfo<RequestAmountRouteArgs> {
  RequestAmountRoute({
    Key? key,
    required String uniqueIdentifier,
    List<PageRouteInfo>? children,
  }) : super(
          RequestAmountRoute.name,
          args: RequestAmountRouteArgs(
            key: key,
            uniqueIdentifier: uniqueIdentifier,
          ),
          initialChildren: children,
        );

  static const String name = 'RequestAmountRoute';

  static const PageInfo<RequestAmountRouteArgs> page =
      PageInfo<RequestAmountRouteArgs>(name);
}

class RequestAmountRouteArgs {
  const RequestAmountRouteArgs({
    this.key,
    required this.uniqueIdentifier,
  });

  final Key? key;

  final String uniqueIdentifier;

  @override
  String toString() {
    return 'RequestAmountRouteArgs{key: $key, uniqueIdentifier: $uniqueIdentifier}';
  }
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
/// [SendView]
class SendRoute extends PageRouteInfo<SendRouteArgs> {
  SendRoute({
    Key? key,
    String? uniqueIdentifier,
    List<PageRouteInfo>? children,
  }) : super(
          SendRoute.name,
          args: SendRouteArgs(
            key: key,
            uniqueIdentifier: uniqueIdentifier,
          ),
          initialChildren: children,
        );

  static const String name = 'SendRoute';

  static const PageInfo<SendRouteArgs> page = PageInfo<SendRouteArgs>(name);
}

class SendRouteArgs {
  const SendRouteArgs({
    this.key,
    this.uniqueIdentifier,
  });

  final Key? key;

  final String? uniqueIdentifier;

  @override
  String toString() {
    return 'SendRouteArgs{key: $key, uniqueIdentifier: $uniqueIdentifier}';
  }
}

/// generated route for
/// [ProfileView]
class ProfileRoute extends PageRouteInfo<ProfileRouteArgs> {
  ProfileRoute({
    Key? key,
    List<PageRouteInfo>? children,
  }) : super(
          ProfileRoute.name,
          args: ProfileRouteArgs(key: key),
          initialChildren: children,
        );

  static const String name = 'ProfileRoute';

  static const PageInfo<ProfileRouteArgs> page =
      PageInfo<ProfileRouteArgs>(name);
}

class ProfileRouteArgs {
  const ProfileRouteArgs({this.key});

  final Key? key;

  @override
  String toString() {
    return 'ProfileRouteArgs{key: $key}';
  }
}
