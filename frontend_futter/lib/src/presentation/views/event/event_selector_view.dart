import 'package:auto_route/auto_route.dart';
import 'package:cardpay/src/config/router/app_router.dart';
import 'package:cardpay/src/config/themes/colors.dart';
import 'package:cardpay/src/presentation/cubits/remote/live_events_cubit.dart';
import 'package:cardpay/src/presentation/cubits/remote/registered_events_cubit.dart';
import 'package:cardpay/src/presentation/cubits/remote/user_cubit.dart';
import 'package:cardpay/src/presentation/widgets/actions/button/primary_button.dart';
import 'package:cardpay/src/presentation/widgets/boxes/height_box.dart';
import 'package:cardpay/src/presentation/widgets/layout/basic_view_layout.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_hooks/flutter_hooks.dart';

@RoutePage()
class EventSelectorView extends HookWidget {
  const EventSelectorView({super.key});

  @override
  Widget build(BuildContext context) {
    final liveEventsCubit = BlocProvider.of<LiveEventsCubit>(context);
    final registeredEventsCubit = BlocProvider.of<RegisteredEventsCubit>(
      context,
    );
    final userCubit = BlocProvider.of<UserCubit>(context);

    return BasicViewLayout(
      headerTitle: "Events",
      backgroundColor: AppColors.teal,
      children: [
        PrimaryButton(
          color: AppColors.blackColor,
          text: "Live Events",
          onPressed: () {
            liveEventsCubit.getLiveEvents(
              userCubit.state.user.closedLoops[0].closedLoopId,
            );
            context.router.push(const LiveEventsRoute());
          },
        ),
        const HeightBox(slab: 1),
        PrimaryButton(
          color: AppColors.blackColor,
          text: "My Bookings",
          onPressed: () {
            registeredEventsCubit.getRegisteredEvents();
            context.router.push(const RegisteredEventsRoute());
          },
        ),
      ],
    );
  }
}
