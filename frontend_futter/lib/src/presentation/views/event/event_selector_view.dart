import 'package:auto_route/auto_route.dart';
import 'package:cardpay/src/config/router/app_router.dart';
import 'package:cardpay/src/config/themes/colors.dart';
import 'package:cardpay/src/presentation/cubits/remote/live_events_cubit.dart';
import 'package:cardpay/src/presentation/cubits/remote/registered_events_cubit.dart';
import 'package:cardpay/src/presentation/cubits/remote/user_cubit.dart';
import 'package:cardpay/src/presentation/views/event/live_events_view.dart';
import 'package:cardpay/src/presentation/views/event/registered_events_view.dart';
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

    if (userCubit.state.user.closedLoops.isNotEmpty)
      liveEventsCubit
          .getLiveEvents(userCubit.state.user.closedLoops[0].closedLoopId);
    registeredEventsCubit.getRegisteredEvents();

    return DefaultTabController(
      length: 2,
      child: BasicViewLayout(
        headerTitle: "Events",
        headerColor: AppColors.blackColor,
        backgroundColor: AppColors.secondaryColor,
        children: [
          Container(
            decoration: BoxDecoration(
              color: AppColors.blackColor.withOpacity(0.03),
              borderRadius: BorderRadius.circular(100),
            ),
            margin: const EdgeInsets.only(right: 20, left: 20),
            /* 
            padding: const EdgeInsets.all(0),
             */
            child: TabBar(
              indicatorWeight: 2,
              labelPadding: const EdgeInsets.only(right: 10, left: 10),
              indicatorPadding: const EdgeInsets.only(right: -10, left: -10),
              indicator: BoxDecoration(
                borderRadius: BorderRadius.circular(100),
                color: AppColors.secondaryColor,
                boxShadow: [
                  BoxShadow(
                    color: AppColors.blackColor.withOpacity(0.1),
                    blurRadius: 10,
                    offset: const Offset(0, 5),
                  ),
                ],
              ),
              padding: const EdgeInsets.only(bottom: 4, top: 4),
              splashFactory: InkSplash.splashFactory,
              splashBorderRadius: BorderRadius.circular(100),
              indicatorColor: Colors.transparent,
              labelStyle: const TextStyle(
                fontSize: 16,
                fontWeight: FontWeight.w500,
              ),
              unselectedLabelStyle: const TextStyle(
                fontSize: 16,
                fontWeight: FontWeight.w500,
              ),
              unselectedLabelColor: AppColors.blackColor.withOpacity(0.3),
              tabs: [
                Container(
                    padding: EdgeInsets.symmetric(horizontal: 25),
                    child: Tab(text: "Live Events")),
                Container(
                  padding: EdgeInsets.symmetric(horizontal: 18),
                  child: Tab(text: "My Bookings"),
                ),
              ],
            ),
          ),
          const HeightBox(slab: 1),
          SizedBox(
            height: MediaQuery.of(context).size.height * 0.7,
            width: MediaQuery.of(context).size.width,
            child: const TabBarView(
              children: [
                LiveEventsView(),
                RegisteredEventsView(),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
