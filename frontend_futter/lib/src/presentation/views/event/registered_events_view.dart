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
                      height: ScreenUtil.screenHeight(context) * 0.7,
                      width: ScreenUtil.screenWidth(context),
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Spacer(),
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
                          Spacer(),
                          Container(
                            width: ScreenUtil.screenWidth(context) * 0.7,
                            height: 50,
                            decoration: BoxDecoration(
                              gradient: LinearGradient(
                                colors: [
                                  Color.fromRGBO(67, 157, 254, 1),
                                  Color.fromRGBO(90, 39, 200, 1),
                                ],
                              ),
                              borderRadius: BorderRadius.circular(15),
                            ),
                            child: Builder(
                              builder: (BuildContext context) {
                                return ElevatedButton(
                                  style: ElevatedButton.styleFrom(
                                    primary: Colors.transparent,
                                    onPrimary: Colors.white,
                                    shadowColor: Colors.transparent,
                                    elevation: 0,
                                    shape: RoundedRectangleBorder(
                                      borderRadius: BorderRadius.circular(15),
                                    ),
                                  ),
                                  onPressed: () {
                                    DefaultTabController.of(context)
                                        .animateTo(0);
                                  },
                                  child: Row(
                                    children: [
                                      const Spacer(),
                                      Text("Explore Events",
                                          style: TextStyle(
                                            fontWeight: FontWeight.bold,
                                            fontSize: 20,
                                          )),
                                      const Spacer(),
                                      Container(
                                        decoration: BoxDecoration(
                                          color: Colors.white.withOpacity(0.05),
                                          borderRadius:
                                              BorderRadius.circular(10),
                                        ),
                                        padding: const EdgeInsets.all(5),
                                        child: Icon(
                                          Icons.arrow_forward_ios,
                                          size: 20,
                                        ),
                                      ),
                                    ],
                                  ),
                                );
                              },
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
