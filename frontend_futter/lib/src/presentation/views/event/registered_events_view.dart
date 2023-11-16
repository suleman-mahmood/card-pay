import 'package:auto_route/auto_route.dart';
import 'package:cardpay/src/config/router/app_router.dart';
import 'package:cardpay/src/config/screen_utills/screen_util.dart';
import 'package:cardpay/src/config/themes/colors.dart';
import 'package:cardpay/src/presentation/cubits/remote/register_event_cubit.dart';
import 'package:cardpay/src/presentation/cubits/remote/registered_events_cubit.dart';
import 'package:cardpay/src/presentation/widgets/boxes/verticle_padding.dart';
import 'package:cardpay/src/presentation/widgets/containment/cards/event_card.dart';
import 'package:cardpay/src/presentation/widgets/layout/basic_view_layout.dart';
import 'package:cardpay/src/utils/utils.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:flutter_svg/flutter_svg.dart';
import 'package:cardpay/src/presentation/widgets/boxes/height_box.dart';
import 'package:intl/intl.dart';
import 'package:skeleton_loader/skeleton_loader.dart';

@RoutePage()
class RegisteredEventsView extends HookWidget {
  const RegisteredEventsView({super.key});

  @override
  Widget build(BuildContext context) {
    return BlocBuilder<RegisteredEventsCubit, RegisteredEventsState>(
        builder: (_, state) {
      switch (state.runtimeType) {
        case RegisteredEventsSuccess:
          return state.events.isEmpty
              ? RefreshIndicator(
                  backgroundColor: AppColors.secondaryColor,
                  onRefresh: () => context
                      .read<RegisteredEventsCubit>()
                      .getRegisteredEvents(),
                  child: SingleChildScrollView(
                    physics: const AlwaysScrollableScrollPhysics(),
                    child: SizedBox(
                      height: ScreenUtil.screenHeight(context) * 0.6,
                      width: ScreenUtil.screenWidth(context),
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          SvgPicture.asset(
                            "assets/icon/noEventCalender.svg",
                          ),
                          const HeightBox(slab: 2),
                          Text(
                            "No Registered Events!",
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
              : SizedBox(
                  child: RefreshIndicator(
                    backgroundColor: AppColors.secondaryColor,
                    onRefresh: () async {
                      context
                          .read<RegisteredEventsCubit>()
                          .getRegisteredEvents();
                    },
                    child: ListView.builder(
                      itemCount: state.events.length,
                      itemBuilder: (_, index) {
                        return EventCard(
                          imageUrl: state.events[index].imageUrl,
                          iconColor: AppColors.primaryColor,
                          textColor: AppColors.blackColor,
                          text: state.events[index].name,
                          subText: croppedDescription(
                            state.events[index].description,
                          ),
                          eventStartTimestamp:
                              state.events[index].eventStartTimestamp,
                          secondLastIcon: Icons.info_outline,
                          venue: state.events[index].venue,
                          amount: state.events[index].registrationFee,
                          iconEnd: Icons.qr_code,
                          onSecondLastIconTap: () {
                            context.router.push(
                              EventAttendanceQrRoute(
                                  event: state.events[index]),
                            );
                          },
                          onEndIconTap: () {
                            context.router.push(
                              EventAttendanceQrRoute(
                                  event: state.events[index]),
                            );
                          },
                        );
                      },
                    ),
                  ),
                );

        /* Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    HeightBox(slab: 2),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Text(
                          "Your Events",
                          style: TextStyle(
                            color: AppColors.blackColor,
                            fontSize: 22,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        TextButton(onPressed: () {}, child: Text("See All")),
                      ],
                    ),
                    SizedBox(
                      height: ScreenUtil.screenHeight(context) * 0.4,
                      child: ListView.builder(
                        scrollDirection: Axis.horizontal,
                        itemCount: state.events.length,
                        itemBuilder: (_, index) {
                          return InkWell(
                            onTap: () {
                              context.router.push(
                                EventAttendanceQrRoute(
                                    event: state.events[index]),
                              );
                            },
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
                                    color:
                                        AppColors.blackColor.withOpacity(0.55),
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
                                          color:
                                              AppColors.blackColor.withOpacity(
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
                                              state.events[index].organizerName,
                                              maxLines: 1,
                                              overflow: TextOverflow.ellipsis,
                                              style: TextStyle(
                                                color: AppColors.secondaryColor
                                                    .withOpacity(0.7),
                                                fontSize: 18,
                                                fontWeight: FontWeight.w500,
                                              ),
                                            ),
                                            Text(
                                              state.events[index].name,
                                              style: TextStyle(
                                                color: AppColors.secondaryColor,
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
                ); */
        case RegisterEventFailed:
          return const Center(child: CircularProgressIndicator());
        case RegisterEventLoading:
          return SkeletonLoader(
            builder: Container(
              height: ScreenUtil.screenHeight(context) * 0.6,
              width: ScreenUtil.screenWidth(context),
              decoration: BoxDecoration(
                color: AppColors.secondaryColor,
                borderRadius: BorderRadius.circular(15),
                border: Border.all(
                  color: AppColors.blackColor.withOpacity(0.55),
                ),
              ),
            ),
          );
        default:
          return RefreshIndicator(
            backgroundColor: AppColors.secondaryColor,
            onRefresh: () =>
                context.read<RegisteredEventsCubit>().getRegisteredEvents(),
            child: SingleChildScrollView(
              physics: const AlwaysScrollableScrollPhysics(),
              child: SizedBox(
                height: ScreenUtil.screenHeight(context) * 0.6,
                width: ScreenUtil.screenWidth(context),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    SvgPicture.asset(
                      "assets/icon/noEventCalender.svg",
                    ),
                    const HeightBox(slab: 2),
                    Text(
                      "No Registered Events!",
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
    });
  }
}
