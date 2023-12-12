import 'package:cardpay/src/config/router/app_router.dart';
import 'package:cardpay/src/config/router/route_observer.dart';
import 'package:cardpay/src/domain/repositories/api_repository.dart';
import 'package:cardpay/src/domain/repositories/database_repository.dart';
import 'package:cardpay/src/locator.dart';
import 'package:cardpay/src/presentation/cubits/local/local_balance_cubit.dart';
import 'package:cardpay/src/presentation/cubits/local/local_recent_transactions_cubit.dart';
import 'package:cardpay/src/presentation/cubits/remote/balance_cubit.dart';
import 'package:cardpay/src/presentation/cubits/remote/checkpoints_cubit.dart';
import 'package:cardpay/src/presentation/cubits/remote/closed_loop_cubit.dart';
import 'package:cardpay/src/presentation/cubits/remote/deposit_cubit.dart';
import 'package:cardpay/src/presentation/cubits/remote/fcm_token_cubit.dart';
import 'package:cardpay/src/presentation/cubits/remote/frequent_users_cubit.dart';
import 'package:cardpay/src/presentation/cubits/remote/live_events_cubit.dart';
import 'package:cardpay/src/presentation/cubits/remote/login_cubit.dart';
import 'package:cardpay/src/presentation/cubits/remote/pin_cubit.dart';
import 'package:cardpay/src/presentation/cubits/remote/recent_transactions_cubit.dart';
import 'package:cardpay/src/presentation/cubits/remote/register_event_cubit.dart';
import 'package:cardpay/src/presentation/cubits/remote/registered_events_cubit.dart';
import 'package:cardpay/src/presentation/cubits/remote/signup_cubit.dart';
import 'package:cardpay/src/presentation/cubits/remote/transfer_cubit.dart';
import 'package:cardpay/src/presentation/cubits/remote/user_cubit.dart';
import 'package:cardpay/src/presentation/cubits/remote/full_name_cubit.dart';

import 'package:cardpay/src/presentation/cubits/remote/versions_cubit.dart';
import 'package:cardpay/src/presentation/views/intro/splash_view.dart';
import 'package:flutter/material.dart';
import 'package:cardpay/src/config/themes/app_themes.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:shared_preferences/shared_preferences.dart';

Future<void> main() async {
  runApp(MainApp());
}

class MainApp extends StatelessWidget {
  MainApp({super.key});

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<void>(
      future: initializeDependencies(),
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.done) {
          return MultiBlocProvider(
            providers: [
              BlocProvider(
                create: (context) => UserCubit(locator<ApiRepository>()),
              ),
              BlocProvider(
                create: (context) => ClosedLoopCubit(locator<ApiRepository>()),
              ),
              BlocProvider(
                create: (context) => VersionsCubit(locator<ApiRepository>()),
              ),
              BlocProvider(
                create: (context) => CheckpointsCubit(locator<ApiRepository>()),
              ),
              BlocProvider(
                create: (context) => LoginCubit(locator<SharedPreferences>()),
              ),
              BlocProvider(
                create: (context) => SignupCubit(
                  locator<ApiRepository>(),
                  locator<SharedPreferences>(),
                ),
              ),
              BlocProvider(
                create: (context) => TransferCubit(locator<ApiRepository>()),
              ),
              BlocProvider(
                create: (context) => DepositCubit(locator<ApiRepository>()),
              ),
              BlocProvider(
                create: (context) => BalanceCubit(locator<ApiRepository>()),
              ),
              BlocProvider(
                  create: (context) =>
                      RecentTransactionsCubit(locator<ApiRepository>())),
              BlocProvider(
                create: (context) => PinCubit(locator<ApiRepository>()),
              ),
              BlocProvider(
                create: (context) => FullNameCubit(locator<ApiRepository>()),
              ),
              BlocProvider(
                create: (context) => FrequentUsersCubit(
                  locator<ApiRepository>(),
                ),
              ),
              BlocProvider(
                create: (context) => FcmTokenCubit(locator<ApiRepository>()),
              ),
              // Events
              BlocProvider(
                create: (context) => LiveEventsCubit(locator<ApiRepository>()),
              ),
              BlocProvider(
                create: (context) =>
                    RegisteredEventsCubit(locator<ApiRepository>()),
              ),
              BlocProvider(
                create: (context) =>
                    RegisterEventCubit(locator<ApiRepository>()),
              ),
              // Local
              BlocProvider(
                create: (context) =>
                    LocalBalanceCubit(locator<DatabaseRepository>()),
              ),
              BlocProvider(
                create: (context) =>
                    LocalRecentTransactionsCubit(locator<DatabaseRepository>()),
              ),
            ],
            child: MaterialApp.router(
              routerConfig: locator<AppRouter>().config(
                navigatorObservers: () => [MyObserver()],
              ),
              theme: AppTheme.light,
            ),
          );
        }
        return const SplashView();
      },
    );
  }
}
