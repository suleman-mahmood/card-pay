import 'package:auto_route/auto_route.dart';
import 'package:cardpay/src/config/router/app_router.dart';
import 'package:cardpay/src/config/screen_utills/screen_util.dart';
import 'package:cardpay/src/config/themes/colors.dart';
import 'package:cardpay/src/presentation/cubits/remote/register_event_cubit.dart';
import 'package:cardpay/src/presentation/cubits/remote/registered_events_cubit.dart';
import 'package:cardpay/src/presentation/widgets/boxes/verticle_padding.dart';
import 'package:cardpay/src/presentation/widgets/containment/cards/event_card.dart';
import 'package:cardpay/src/presentation/widgets/layout/basic_view_layout.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_hooks/flutter_hooks.dart';

@RoutePage()
class RegisteredEventsView extends HookWidget {
  const RegisteredEventsView({super.key});

  @override
  Widget build(BuildContext context) {
    return BasicViewLayout(
      centered: false,
      headerTitle: "Registered Events",
      backgroundColor: AppColors.teal,
      children: [
        BlocBuilder<RegisteredEventsCubit, RegisteredEventsState>(
            builder: (_, state) {
          switch (state.runtimeType) {
            case RegisteredEventsSuccess:
              return SizedBox(
                height: ScreenUtil.screenHeight(context),
                child: ListView.builder(
                  itemCount: state.events.length,
                  itemBuilder: (_, index) {
                    return PaddingBoxVertical(
                      slab: 1,
                      child: EventCard(
                        iconColor: AppColors.primaryColor,
                        textColor: AppColors.blackColor,
                        icon: Icons.delete,
                        text: state.events[index].name,
                        subText: state.events[index].description,
                        secondLastIcon: Icons.info_outline,
                        iconEnd: Icons.qr_code,
                        onSecondLastIconTap: () => context.router.push(
                          EventDetailsRoute(
                            showRegistrationButton: false,
                            event: state.events[index],
                          ),
                        ),
                        onEndIconTap: () {
                          context.router.push(
                            EventAttendanceQrRoute(event: state.events[index]),
                          );
                        },
                      ),
                    );
                  },
                ),
              );
            case RegisterEventFailed:
              return const Center(child: CircularProgressIndicator());
            default:
              return const SizedBox.shrink();
          }
        }),
      ],
    );
  }
}
