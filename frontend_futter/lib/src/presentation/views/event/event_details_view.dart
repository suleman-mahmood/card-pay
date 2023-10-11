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
      context.router.push(
        ReceiptRoute(
          amount: event.registrationFee,
          recipientName: event.organizerName,
        ),
      );
    }

    void _showDialog() {
      showDialog(
        context: context,
        builder: (BuildContext context) => AlertDialog(
          backgroundColor: Colors.white,
          title: const Text('Confirm registration'),
          content: Text('Amount ${event.registrationFee}'),
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
                  subtitle: Text(event.eventStartTime.toString()),
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
                  subtitle: Text(event.eventStartTime.toString()),
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
          "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Amet luctus venenatis lectus magna fringilla. Arcu cursus vitae congue mauris rhoncus aenean vel.",
          style: AppTypography.bodyText,
        ),
        const HeightBox(slab: 1),
        Text(
          "Organizer",
          style: AppTypography.subHeadingBold,
        ),
        Text(
          "Some organizer",
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
              onPressed: () => _showDialog(),
            ),
          ),
        ),
      ],
    );
  }
}
