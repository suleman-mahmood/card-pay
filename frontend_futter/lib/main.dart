import 'package:cardpay/src/domain/repositories/api_repository.dart';
import 'package:cardpay/src/locator.dart';
import 'package:cardpay/src/presentation/cubits/remote/checkpoints_cubit.dart';
import 'package:cardpay/src/presentation/cubits/remote/closed_loop_cubit.dart';
import 'package:cardpay/src/presentation/cubits/remote/login_cubit.dart';
import 'package:cardpay/src/presentation/cubits/remote/user_cubit.dart';
import 'package:flutter/material.dart';
import 'package:cardpay/src/config/router/app_router.dart';
import 'package:cardpay/src/config/themes/app_themes.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:upgrader/upgrader.dart';
import 'package:shared_preferences/shared_preferences.dart';

Future<void> main() async {
  await initializeDependencies();
  runApp(MainApp());
}

class MainApp extends StatelessWidget {
  MainApp({super.key});

  final _appRouter = AppRouter();

  @override
  Widget build(BuildContext context) {
    return UpgradeAlert(
      child: MultiBlocProvider(
        providers: [
          BlocProvider(
            create: (context) => UserCubit(
                locator<ApiRepository>(), locator<SharedPreferences>()),
          ),
          BlocProvider(
            create: (context) => ClosedLoopCubit(locator<ApiRepository>()),
          ),
          BlocProvider(
            create: (context) => CheckpointsCubit(locator<ApiRepository>()),
          ),
          BlocProvider(
            create: (context) => LoginCubit(locator<SharedPreferences>()),
          ),
        ],
        child: MaterialApp.router(
          routerConfig: _appRouter.config(),
          theme: AppTheme.light,
        ),
      ),
    );
  }
}
