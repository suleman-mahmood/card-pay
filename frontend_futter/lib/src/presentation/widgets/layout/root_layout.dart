import 'package:auto_route/auto_route.dart';
import 'package:cardpay/src/all_listeners.dart';
import 'package:cardpay/src/config/router/app_router.dart';
import 'package:cardpay/src/locator.dart';
import 'package:cardpay/src/presentation/cubits/remote/checkpoints_cubit.dart';
import 'package:cardpay/src/presentation/cubits/remote/versions_cubit.dart';
import 'package:cardpay/src/presentation/widgets/boxes/update_modal.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_hooks/flutter_hooks.dart';

class RootLayout extends HookWidget {
  final Widget child;

  RootLayout({super.key, required this.child});

  @override
  Widget build(BuildContext context) {
    void navigateToNextScreen(CheckpointsState state) {
      PageRouteInfo route = const SignupRoute();

      if (state.checkPoints.verifiedPhoneOtp &&
          state.checkPoints.verifiedClosedLoop &&
          state.checkPoints.pinSetup) {
        route = DashboardLayoutRoute();
      } else if (state.checkPoints.verifiedPhoneOtp &&
          state.checkPoints.verifiedClosedLoop &&
          state.checkPoints.pinSetup == false) {
        route = const PinRoute();
      } else if (state.checkPoints.verifiedPhoneOtp &&
          state.checkPoints.verifiedClosedLoop == false) {
        route = const ClosedLoopRoute();
      }

      if (locator<AppRouter>().topRoute.name != 'DashboardLayoutRoute') {
        locator<AppRouter>().push(route);
      }
    }

    return Stack(
      children: [
        SizedBox(height: MediaQuery.of(context).size.height, child: child),
        BlocBuilder<VersionsCubit, VersionsState>(
          builder: (_, state) {
            switch (state.runtimeType) {
              case VersionsSuccess:
                if (state.forceUpdate) {
                  return const UpdateModal(showMaybeLaterButton: false);
                }
                if (state.normalUpdate) {
                  return const UpdateModal(showMaybeLaterButton: true);
                }
            }
            return const SizedBox.shrink();
          },
        ),
        BlocListener<VersionsCubit, VersionsState>(
          listener: (_, state) {
            switch (state.runtimeType) {
              case VersionsSuccess:
                locator<AllListeners>().authListener(context);
            }
          },
          child: const SizedBox.shrink(),
        ),
        BlocListener<CheckpointsCubit, CheckpointsState>(
          listener: (_, state) {
            switch (state.runtimeType) {
              case CheckpointsSuccess:
                navigateToNextScreen(state);
            }
          },
          child: const SizedBox.shrink(),
        ),
      ],
    );
  }
}
