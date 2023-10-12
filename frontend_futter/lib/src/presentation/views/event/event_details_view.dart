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
          backgroundColor: Colors.white,
          title: const Text('Confirm registration'),
          content: BlocBuilder<RegisterEventCubit, RegisterEventState>(
            builder: (_, state) {
              switch (state.runtimeType) {
                case RegisterEventInitial:
                  return Text('Amount ${event.registrationFee}');
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
          actions: <Widget>[
            TextButton(
              onPressed: handleEventRegistration,
              child: const Text('Pay!'),
            ),
            TextButton(
              onPressed: () => context.router.pop(),
              child: const Text('Cancel'),
            ),
          ],
        ),
      );
    }

    return BasicViewLayout(
      centered: false,
      headerTitle: "Event Details",
      backgroundColor: AppColors.teal,
      children: [
        AspectRatio(
          aspectRatio: 16 / 9,
          child: Container(
            decoration: BoxDecoration(
              borderRadius: const BorderRadius.all(Radius.circular(15)),
              image: DecorationImage(
                fit: BoxFit.fitWidth,
                alignment: FractionalOffset.center,
                image: NetworkImage(event.imageUrl),
              ),
            ),
          ),
        ),
        const HeightBox(slab: 2),
        Align(
          child: Text(
            event.name,
            style: AppTypography.mainHeadingWhite,
          ),
        ),
        const HeightBox(slab: 1),
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            SizedBox(
              width: ScreenUtil.screenWidth(context) * (3 / 7),
              child: Card(
                child: ListTile(
                  title: const Text("Date"),
                  titleTextStyle: AppTypography.subHeadingBold,
                  subtitleTextStyle: AppTypography.bodyText,
                  subtitle: Text(event.eventStartTimestamp.toString()),
                  trailing: const Icon(
                    Icons.punch_clock_outlined,
                  ),
                ),
              ),
            ),
            SizedBox(
              width: ScreenUtil.screenWidth(context) * (3 / 7),
              child: Card(
                child: ListTile(
                  title: const Text("Time"),
                  titleTextStyle: AppTypography.subHeadingBold,
                  subtitleTextStyle: AppTypography.bodyText,
                  subtitle: Text(event.eventStartTimestamp.toString()),
                  trailing: const Icon(
                    Icons.punch_clock_outlined,
                  ),
                ),
              ),
            ),
          ],
        ),
        const HeightBox(slab: 1),
        Card(
          child: ListTile(
            title: const Text("Venue"),
            titleTextStyle: AppTypography.subHeadingBold,
            subtitle: Text(event.venue),
            subtitleTextStyle: AppTypography.bodyText,
            trailing: const Icon(
              Icons.punch_clock_outlined,
            ),
          ),
        ),
        const HeightBox(slab: 1),
        Text(
          "Additional information",
          style: AppTypography.subHeadingBold,
        ),
        Text(
          event.description,
          style: AppTypography.bodyText,
        ),
        const HeightBox(slab: 1),
        Text(
          "Organizer",
          style: AppTypography.subHeadingBold,
        ),
        Text(
          event.organizerName,
          style: AppTypography.bodyText,
        ),
        const HeightBox(slab: 2),
        Visibility(
          visible: showRegistrationButton,
          child: Align(
            alignment: Alignment.center,
            child: PrimaryButton(
              color: AppColors.blackColor,
              text: 'Register Now!',
              onPressed: () {
                registerEventCubit.initialize();
                _showDialog();
              },
            ),
          ),
        ),
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
    );
  }
}
