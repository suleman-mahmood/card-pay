import 'package:auto_route/auto_route.dart';
import 'package:cardpay/src/config/router/app_router.dart';
import 'package:cardpay/src/config/screen_utills/screen_util.dart';
import 'package:cardpay/src/config/themes/colors.dart';
import 'package:cardpay/src/domain/models/event.dart';
import 'package:cardpay/src/presentation/cubits/remote/register_event_cubit.dart';
import 'package:cardpay/src/presentation/widgets/actions/button/primary_button.dart';
import 'package:cardpay/src/presentation/widgets/boxes/height_box.dart';
import 'package:cardpay/src/presentation/widgets/layout/basic_view_layout.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:intl/intl.dart';

@RoutePage()
class EventDetailsView extends StatelessWidget {
  final bool showRegistrationButton;
  final Event event;

  const EventDetailsView({
    super.key,
    required this.showRegistrationButton,
    required this.event,
  });

  @override
  Widget build(BuildContext context) {
    final registerEventCubit = BlocProvider.of<RegisterEventCubit>(context);

    void handleEventRegistration() {
      registerEventCubit.registerEvent(event.id);
    }

    void _showDialog() {
      showDialog(
        context: context,
        builder: (BuildContext context) => AlertDialog(
          alignment: Alignment.center,
          backgroundColor: Colors.white,
          title: Column(
            children: [
              Stack(
                alignment: Alignment.center,
                children: [
                  CircleAvatar(
                    radius: 30,
                    backgroundColor: AppColors.lightBlueColor,
                  ),
                  /*  CircleAvatar(
                    radius: 28,
                    backgroundColor: AppColors.secondaryColor,
                  ), */
                  const Icon(
                    Icons.question_mark_rounded,
                    color: AppColors.secondaryColor,
                    size: 50,
                  ),
                ],
              ),
              const HeightBox(slab: 2),
              const Text('Confirm registration',
                  textAlign: TextAlign.center,
                  style: TextStyle(
                    color: Colors.black,
                    fontSize: 22,
                    fontWeight: FontWeight.w600,
                  )),
            ],
          ),
          content: BlocBuilder<RegisterEventCubit, RegisterEventState>(
            builder: (_, state) {
              switch (state.runtimeType) {
                case RegisterEventInitial:
                  return Column(
                    mainAxisSize: MainAxisSize.min,
                    mainAxisAlignment: MainAxisAlignment.center,
                    crossAxisAlignment: CrossAxisAlignment.center,
                    children: [
                      const HeightBox(slab: 2),
                      Text(
                        'You are about to register for ${event.name}',
                        textAlign: TextAlign.center,
                      ),
                      const HeightBox(slab: 2),
                      Text(
                        'Tap on Pay to Register\nRs.${event.registrationFee}',
                        textAlign: TextAlign.center,
                        style: AppTypography.bodyTextBold,
                      ),
                      const HeightBox(slab: 5),
                      ElevatedButton(
                        style: ElevatedButton.styleFrom(
                          padding: const EdgeInsets.symmetric(
                              horizontal: 80, vertical: 12),
                          primary: AppColors.lightBlueColor,
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(10),
                          ),
                          onPrimary: Colors.white,
                        ),
                        onPressed: handleEventRegistration,
                        child: const Text('Pay!',
                            style: TextStyle(
                                fontSize: 18, fontWeight: FontWeight.w600)),
                      ),
                      const HeightBox(slab: 1),
                      TextButton(
                        onPressed: () => context.router.pop(),
                        child: const Text('Cancel'),
                      ),
                    ],
                  );
                case RegisterEventLoading:
                  return const SizedBox(
                    width: 10,
                    height: 30,
                    child: Center(child: CircularProgressIndicator()),
                  );
                case RegisterEventFailed || RegisterEventUnknownFailure:
                  return Text(
                    state.errorMessage,
                    style: const TextStyle(color: Colors.red),
                    textAlign: TextAlign.center,
                  );
                default:
                  return const SizedBox.shrink();
              }
            },
          ),
        ),
      );
    }

    return Stack(
      children: [
        Scaffold(
          backgroundColor: AppColors.secondaryColor,
          body: SingleChildScrollView(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.start,
              children: [
                Stack(
                  clipBehavior: Clip.none,
                  children: [
                    Container(
                      height: ScreenUtil.screenHeight(context) * 0.5,
                      decoration: BoxDecoration(
                        borderRadius:
                            const BorderRadius.all(Radius.circular(15)),
                        image: DecorationImage(
                          fit: BoxFit.cover,
                          image: NetworkImage(event.imageUrl),
                        ),
                      ),
                    ),
                    /* Positioned(
                      top: 40,
                      left: 20,
                      child: GestureDetector(
                        onTap: () => context.router.pop(),
                        child: Container(
                          width: 40,
                          height: 40,
                          decoration: BoxDecoration(
                            color: AppColors.blackColor.withOpacity(0.5),
                            borderRadius:
                                const BorderRadius.all(Radius.circular(15)),
                          ),
                          child: const Icon(
                            Icons.arrow_back_rounded,
                            color: Colors.white,
                          ),
                        ),
                      ),
                    ), */
                    Positioned(
                      bottom: -ScreenUtil.screenHeight(context) * 0.075,
                      left: 20,
                      right: 20,
                      child: Container(
                        width: ScreenUtil.screenWidth(context) * 0.7,
                        decoration: BoxDecoration(
                          color: AppColors.secondaryColor,
                          borderRadius:
                              const BorderRadius.all(Radius.circular(15)),
                          boxShadow: [
                            BoxShadow(
                              color: AppColors.blackColor.withOpacity(0.1),
                              blurRadius: 10,
                              offset: const Offset(0, 5),
                            ),
                          ],
                        ),
                        padding: const EdgeInsets.only(
                            top: 8, bottom: 8, right: 14.0, left: 16.0),
                        child: Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          crossAxisAlignment: CrossAxisAlignment.start,
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            Text(
                              softWrap: true,
                              maxLines: 2,
                              overflow: TextOverflow.ellipsis,
                              event.name,
                              style: AppTypography.headingFont.copyWith(
                                color: AppColors.blackColor,
                                fontSize: 20,
                                fontWeight: FontWeight.w900,
                              ),
                            ),
                            const SizedBox(
                              height: 2,
                            ),
                            Text(
                              DateFormat('MMM dd, yyyy')
                                  .format(event.eventStartTimestamp),
                              style: AppTypography.bodyText.copyWith(
                                color: AppColors.greyColor,
                                fontSize: 14,
                              ),
                            ),
                            Text(
                              '${DateFormat('hh:mm a').format(event.eventStartTimestamp)}, ${event.venue}',
                              style: AppTypography.bodyText.copyWith(
                                color: AppColors.greyColor,
                                fontSize: 12,
                              ),
                            ),
                            SizedBox(
                              height: 10,
                            ),
                            Text(
                              'Rs. ${event.registrationFee}',
                              style: AppTypography.bodyText.copyWith(
                                color: AppColors.lightBlueColor,
                                fontSize: 16,
                                fontWeight: FontWeight.w900,
                              ),
                            ),
                          ],
                        ),
                      ),
                    )
                  ],
                ),
                Container(
                  padding:
                      const EdgeInsets.symmetric(horizontal: 20, vertical: 16),
                  margin: EdgeInsets.only(
                      top: ScreenUtil.screenHeight(context) * 0.08),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'Event by',
                        style: AppTypography.bodyTextBold,
                      ),
                      const HeightBox(slab: 1),
                      Row(
                        mainAxisAlignment: MainAxisAlignment.start,
                        children: [
                          CircleAvatar(
                            radius: 21,
                            backgroundColor: AppColors.purpleColor,
                            child: Center(
                              child: Text(
                                // first and last name innitials, if only one name then first 2 letters
                                event.organizerName.split(' ').length > 1
                                    ? '${event.organizerName.split(' ')[0][0]}${event.organizerName.split(' ')[1][0]}'
                                    : '${event.organizerName.split(' ')[0][0]}${event.organizerName.split(' ')[0][1]}',
                                style: AppTypography.bodyText.copyWith(
                                  color: Colors.white,
                                  fontSize: 15,
                                  fontWeight: FontWeight.w900,
                                ),
                              ),
                            ),
                          ),
                          const SizedBox(
                            width: 10,
                          ),
                          Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                event.organizerName,
                                textAlign: TextAlign.center,
                                style: AppTypography.bodyText.copyWith(
                                  color: AppColors.blackColor.withOpacity(0.6),
                                  fontWeight: FontWeight.w900,
                                  fontSize: 14,
                                ),
                              ),
                              Text(
                                "Posted on ${DateFormat('dd MMM, yyyy').format(event.eventStartTimestamp)}",
                                textAlign: TextAlign.center,
                                style: AppTypography.bodyText.copyWith(
                                  color: AppColors.greyColor,
                                  fontSize: 12,
                                ),
                              ),
                            ],
                          ),
                        ],
                      ),
                      const HeightBox(slab: 2),
                      Text(
                        "About",
                        style: AppTypography.bodyTextBold,
                      ),
                      Text(
                        event.description,
                        style: AppTypography.bodyText.copyWith(
                          color: AppColors.greyColor,
                          fontSize: 14,
                        ),
                      ),
                      const HeightBox(slab: 3),
                      BlocListener<RegisterEventCubit, RegisterEventState>(
                        listener: (_, state) {
                          switch (state.runtimeType) {
                            case RegisterEventSuccess:
                              context.router.push(
                                ReceiptRoute(
                                  amount: event.registrationFee,
                                  recipientName: event.organizerName,
                                ),
                              );
                          }
                        },
                        child: const SizedBox.shrink(),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),
          bottomNavigationBar: Visibility(
            visible: showRegistrationButton,
            child: Container(
              margin: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
              child: PrimaryButton(
                color: AppColors.lightBlueColor,
                text: 'Register Now!',
                onPressed: () {
                  registerEventCubit.initialize();
                  _showDialog();
                },
              ),
            ),
          ),
        ),
        Positioned(
          top: 40,
          left: 20,
          child: GestureDetector(
            onTap: () => context.router.pop(),
            child: Container(
              width: 40,
              height: 40,
              decoration: BoxDecoration(
                color: AppColors.blackColor.withOpacity(0.5),
                borderRadius: const BorderRadius.all(Radius.circular(15)),
              ),
              child: const Icon(
                Icons.arrow_back_rounded,
                color: Colors.white,
              ),
            ),
          ),
        ),
      ],
    );
  }
}
