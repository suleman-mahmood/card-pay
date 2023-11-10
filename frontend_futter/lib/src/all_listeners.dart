import 'package:cardpay/src/config/router/app_router.dart';
import 'package:cardpay/src/locator.dart';
import 'package:cardpay/src/presentation/cubits/remote/balance_cubit.dart';
import 'package:cardpay/src/presentation/cubits/remote/checkpoints_cubit.dart';
import 'package:cardpay/src/presentation/cubits/remote/closed_loop_cubit.dart';
import 'package:cardpay/src/presentation/cubits/remote/fcm_token_cubit.dart';
import 'package:cardpay/src/presentation/cubits/remote/recent_transactions_cubit.dart';
import 'package:cardpay/src/presentation/cubits/remote/user_cubit.dart';
import 'package:cardpay/src/utils/pretty_logs.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

class AllListeners {
  bool didSetup = false;
  late final BuildContext context;
  late final FcmTokenCubit fcmTokemCubit;
  late final UserCubit userCubit;
  late final ClosedLoopCubit closedLoopCubit;
  late final BalanceCubit balanceCubit;
  late final RecentTransactionsCubit recentTransactionsCubit;
  late final CheckpointsCubit checkpointsCubit;

  authListener(BuildContext ctx) {
    if (didSetup) return;
    didSetup = true;

    context = ctx;
    fcmTokemCubit = BlocProvider.of<FcmTokenCubit>(context);
    userCubit = BlocProvider.of<UserCubit>(context);
    closedLoopCubit = BlocProvider.of<ClosedLoopCubit>(context);
    balanceCubit = BlocProvider.of<BalanceCubit>(context);
    recentTransactionsCubit = BlocProvider.of<RecentTransactionsCubit>(context);
    checkpointsCubit = BlocProvider.of<CheckpointsCubit>(context);

    FirebaseAuth.instance.authStateChanges().listen((User? user) {
      if (user == null) {
        if (locator<AppRouter>().topRoute.name != 'IntroRoute') {
          locator<AppRouter>().push(const IntroRoute());
        }
      } else {
        if (locator<AppRouter>().topRoute.name == 'SignupRoute') return;

        if (locator<AppRouter>().topRoute.name != 'DashboardLayoutRoute') {
          locator<AppRouter>().push(DashboardLayoutRoute());
        }

        fcmTokemCubit.setFcmTokem();
        userCubit.getUser();
        balanceCubit.getUserBalance();
        recentTransactionsCubit.getUserRecentTransactions();
        closedLoopCubit.getAllClosedLoops();
        checkpointsCubit.getCheckpoints();
      }
    });
  }
}
