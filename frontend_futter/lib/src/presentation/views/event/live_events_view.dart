import 'dart:math';
import 'package:auto_route/auto_route.dart';
import 'package:cardpay/src/config/router/app_router.dart';
import 'package:cardpay/src/config/screen_utills/screen_util.dart';
import 'package:cardpay/src/config/themes/colors.dart';
import 'package:cardpay/src/presentation/cubits/remote/live_events_cubit.dart';
import 'package:cardpay/src/presentation/cubits/remote/user_cubit.dart';
import 'package:cardpay/src/presentation/widgets/boxes/height_box.dart';
import 'package:cardpay/src/presentation/widgets/boxes/verticle_padding.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:flutter_svg/svg.dart';
import 'package:intl/intl.dart';
import 'package:skeleton_loader/skeleton_loader.dart';

@RoutePage()
class LiveEventsView extends HookWidget {
  const LiveEventsView({super.key});

  @override
  Widget build(BuildContext context) {
    final userCubit = BlocProvider.of<UserCubit>(context);
    final liveEventsCubit = BlocProvider.of<LiveEventsCubit>(context);
    return Column(
      children: [
        // a search button
        /* Container(
          decoration: BoxDecoration(
            color: AppColors.secondaryColor,
            borderRadius: BorderRadius.circular(15),
            border: Border.all(
              color: AppColors.blackColor.withOpacity(0.5),
            ),
          ),
          padding: const EdgeInsets.symmetric(horizontal: 10),
          margin: EdgeInsets.only(
            top: 10,
            bottom: 20,
          ),
          height: 50,
          width: ScreenUtil.screenWidth(context) * 0.85,
          child: Row(
            mainAxisAlignment: MainAxisAlignment.start,
            children: [
              Row(
                children: [
                  Icon(
                    Icons.search,
                    color: AppColors.blackColor.withOpacity(0.5),
                  ),
                  const SizedBox(width: 10),
                  Text(
                    "Search",
                    style: TextStyle(
                      color: AppColors.blackColor.withOpacity(0.7),
                      fontSize: 16,
                      fontWeight: FontWeight.w300,
                    ),
                  ),
                ],
              ),
            ],
          ),
        ), */
        BlocBuilder<LiveEventsCubit, LiveEventsState>(builder: (_, state) {
          switch (state.runtimeType) {
            case LiveEventsSuccess:
              return state.events.isEmpty
                  ? RefreshIndicator(
                      backgroundColor: AppColors.secondaryColor,
                      onRefresh: () async {
                        liveEventsCubit.getLiveEvents(
                          userCubit.state.user.closedLoops[0].closedLoopId,
                        );
                      },
                      child: SingleChildScrollView(
                        physics: AlwaysScrollableScrollPhysics(),
                        child: SizedBox(
                          height: ScreenUtil.screenHeight(context) * 0.6,
                          child: Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              SvgPicture.asset(
                                "assets/icon/noEventCalender.svg",
                              ),
                              const HeightBox(slab: 2),
                              Text(
                                "No Upcoming Events!",
                                style: TextStyle(
                                  color: AppColors.blackColor,
                                  fontSize: 22,
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                            ],
                          ),
                        ),
                      ),
                    )
                  : Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Padding(
                          padding: const EdgeInsets.all(8.0),
                          child: Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: [
                              Text(
                                "Popular Now",
                                style: TextStyle(
                                  color: AppColors.blackColor,
                                  fontSize: 22,
                                  fontWeight: FontWeight.bold,
                                ),
                              ),

                              // TODO: add a route for LiveEventsDetailRoute
                              TextButton(
                                  onPressed: () => context.router
                                      .push(LiveEventsDetailedRoute()),
                                  child: Text("See All")),
                            ],
                          ),
                        ),
                        SizedBox(
                          height: ScreenUtil.screenHeight(context) * 0.4,
                          child: ListView.builder(
                            scrollDirection: Axis.horizontal,
                            itemCount: state.events.length,
                            itemBuilder: (_, index) {
                              return InkWell(
                                onTap: () => context.router.push(
                                  EventDetailsRoute(
                                    showRegistrationButton: true,
                                    event: state.events[index],
                                  ),
                                ),
                                child: PaddingBoxVertical(
                                  slab: 1,
                                  child: Container(
                                    margin: const EdgeInsets.only(
                                        left: 10, right: 15, top: 20),
                                    clipBehavior: Clip.antiAlias,
                                    width: 300,
                                    decoration: BoxDecoration(
                                      color: AppColors.secondaryColor,
                                      borderRadius: BorderRadius.circular(15),
                                      border: Border.all(
                                        color: AppColors.secondaryColor,
                                      ),
                                    ),
                                    child: Stack(
                                      fit: StackFit.expand,
                                      children: [
                                        Image.network(
                                          state.events[index].imageUrl,
                                          fit: BoxFit.cover,
                                        ),
                                        // a blur box
                                        Positioned.fill(
                                          child: Container(
                                            decoration: BoxDecoration(
                                              color: AppColors.blackColor
                                                  .withOpacity(
                                                0.3,
                                              ),
                                            ),
                                          ),
                                        ),
                                        Positioned(
                                          top: 10,
                                          right: 10,
                                          child: Container(
                                            padding: const EdgeInsets.symmetric(
                                              horizontal: 15,
                                              vertical: 7.5,
                                            ),
                                            decoration: BoxDecoration(
                                              color: AppColors.secondaryColor
                                                  .withOpacity(
                                                0.75,
                                              ),
                                              borderRadius: BorderRadius.all(
                                                Radius.circular(15),
                                              ),
                                            ),
                                            child: Column(
                                              children: [
                                                Text(
                                                  // state.events[index].eventStartTimestamp.month as Jan/Feb/Mar etc not number of month
                                                  DateFormat('MMM').format(state
                                                      .events[index]
                                                      .eventStartTimestamp),
                                                  style: TextStyle(
                                                    color: AppColors.blackColor
                                                        .withOpacity(0.6),
                                                    fontSize: 16,
                                                    fontWeight: FontWeight.w300,
                                                  ),
                                                ),
                                                Text(
                                                  state.events[index]
                                                      .eventStartTimestamp.day
                                                      .toString(),
                                                  style: TextStyle(
                                                    color: AppColors.blackColor,
                                                    fontSize: 24,
                                                    fontWeight: FontWeight.w900,
                                                  ),
                                                ),
                                              ],
                                            ),
                                          ),
                                        ),
                                        Positioned(
                                          bottom: 10,
                                          left: 10,
                                          child: Padding(
                                            padding: const EdgeInsets.all(8.0),
                                            child: Column(
                                              mainAxisAlignment:
                                                  MainAxisAlignment.spaceEvenly,
                                              crossAxisAlignment:
                                                  CrossAxisAlignment.start,
                                              children: [
                                                Text(
                                                  state.events[index]
                                                      .organizerName,
                                                  maxLines: 1,
                                                  overflow:
                                                      TextOverflow.ellipsis,
                                                  style: TextStyle(
                                                    color: AppColors
                                                        .secondaryColor
                                                        .withOpacity(0.7),
                                                    fontSize: 18,
                                                    fontWeight: FontWeight.w500,
                                                  ),
                                                ),
                                                Text(
                                                  state.events[index].name,
                                                  style: TextStyle(
                                                    color: AppColors
                                                        .secondaryColor,
                                                    fontSize: 30,
                                                    fontWeight: FontWeight.w900,
                                                  ),
                                                ),
                                              ],
                                            ),
                                          ),
                                        ),
                                      ],
                                    ),
                                  ),
                                ),
                              );
                            },
                          ),
                        ),
                      ],
                    );
            case LiveEventsLoading:
              return SkeletonLoader(
                builder: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Padding(
                      padding: const EdgeInsets.all(8.0),
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          Text(
                            "Popular Now",
                            style: TextStyle(
                              color: AppColors.blackColor,
                              fontSize: 22,
                              fontWeight: FontWeight.bold,
                            ),
                          ),

                          // TODO: add a route for LiveEventsDetailRoute
                          TextButton(
                              onPressed: () => context.router
                                  .push(LiveEventsDetailedRoute()),
                              child: Text("See All")),
                        ],
                      ),
                    ),
                    Row(
                      children: [
                        const SizedBox(width: 10),
                        Container(
                          height: ScreenUtil.screenHeight(context) * 0.3,
                          width: ScreenUtil.screenWidth(context) * 0.7,
                          decoration: BoxDecoration(
                            color: AppColors.secondaryColor,
                            borderRadius: BorderRadius.circular(15),
                          ),
                        ),
                        const SizedBox(width: 10),
                        Container(
                          height: ScreenUtil.screenHeight(context) * 0.3,
                          width: ScreenUtil.screenWidth(context) * 0.7,
                          decoration: BoxDecoration(
                            color: AppColors.secondaryColor,
                            borderRadius: BorderRadius.circular(15),
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
              );
            case LiveEventsFailed:
              return SkeletonLoader(
                builder: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Padding(
                      padding: const EdgeInsets.all(8.0),
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          Text(
                            "Popular Now",
                            style: TextStyle(
                              color: AppColors.blackColor,
                              fontSize: 22,
                              fontWeight: FontWeight.bold,
                            ),
                          ),

                          // TODO: add a route for LiveEventsDetailRoute
                          TextButton(
                              onPressed: () => context.router
                                  .push(LiveEventsDetailedRoute()),
                              child: Text("See All")),
                        ],
                      ),
                    ),
                    Row(
                      children: [
                        const SizedBox(width: 10),
                        Container(
                          height: ScreenUtil.screenHeight(context) * 0.3,
                          width: ScreenUtil.screenWidth(context) * 0.7,
                          decoration: BoxDecoration(
                            color: AppColors.secondaryColor,
                            borderRadius: BorderRadius.circular(15),
                          ),
                        ),
                        const SizedBox(width: 10),
                        Container(
                          height: ScreenUtil.screenHeight(context) * 0.3,
                          width: ScreenUtil.screenWidth(context) * 0.7,
                          decoration: BoxDecoration(
                            color: AppColors.secondaryColor,
                            borderRadius: BorderRadius.circular(15),
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
              );
            default:
              return RefreshIndicator(
                backgroundColor: AppColors.secondaryColor,
                onRefresh: () async {
                  context.read<LiveEventsCubit>().getLiveEvents(
                        userCubit.state.user.closedLoops[0].closedLoopId,
                      );
                },
                child: SingleChildScrollView(
                  physics: AlwaysScrollableScrollPhysics(),
                  child: SizedBox(
                    height: ScreenUtil.screenHeight(context) * 0.6,
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        SvgPicture.asset(
                          "assets/icon/noEventCalender.svg",
                        ),
                        const HeightBox(slab: 2),
                        Text(
                          "No Upcoming Events!",
                          style: TextStyle(
                            color: AppColors.blackColor,
                            fontSize: 22,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              );
          }
        }),
      ],
    );
  }
}
