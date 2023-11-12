import 'dart:math';

import 'package:auto_route/auto_route.dart';
import 'package:cardpay/src/config/router/app_router.dart';
import 'package:cardpay/src/config/screen_utills/screen_util.dart';
import 'package:cardpay/src/config/themes/colors.dart';
import 'package:cardpay/src/presentation/cubits/remote/live_events_cubit.dart';
import 'package:cardpay/src/presentation/widgets/boxes/verticle_padding.dart';
import 'package:cardpay/src/presentation/widgets/layout/basic_view_layout.dart';
import 'package:cardpay/src/presentation/widgets/navigations/drawer_navigation.dart';
import 'package:cardpay/src/utils/utils.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_hooks/flutter_hooks.dart';

@RoutePage()
class LiveEventsView extends HookWidget {
  const LiveEventsView({super.key});

  @override
  Widget build(BuildContext context) {
    return BasicViewLayout(
      centered: false,
      headerTitle: "Live Events",
      backgroundColor: AppColors.teal,
      children: [
        BlocBuilder<LiveEventsCubit, LiveEventsState>(builder: (_, state) {
          switch (state.runtimeType) {
            case LiveEventsSuccess:
              return SizedBox(
                height: ScreenUtil.screenHeight(context) * 0.8,
                child: ListView.builder(
                  itemCount: state.events.length,
                  itemBuilder: (_, index) {
                    return PaddingBoxVertical(
                      slab: 1,
                      child: CustomListTile(
                        iconColor: AppColors.primaryColor,
                        textColor: AppColors.blackColor,
                        icon: Icons.info,
                        text: state.events[index].name,
                        subText: croppedDescription(
                          state.events[index].description,
                        ),
                        iconEnd: Icons.arrow_forward_ios,
                        onTap: () => context.router.push(
                          EventDetailsRoute(
                            showRegistrationButton: true,
                            event: state.events[index],
                          ),
                        ),
                      ),
                    );
                  },
                ),
              );
            case LiveEventsFailed:
              return const Center(child: CircularProgressIndicator());
            default:
              return const SizedBox.shrink();
          }
        }),
      ],
    );
  }
}
