import 'package:auto_route/auto_route.dart';
import 'package:cardpay/src/config/router/app_router.dart';
import 'package:cardpay/src/config/themes/colors.dart';
import 'package:cardpay/src/domain/models/event.dart';
import 'package:cardpay/src/presentation/widgets/containment/cards/event_card.dart';
import 'package:cardpay/src/utils/utils.dart';
import 'package:flutter/material.dart';

import '../../widgets/boxes/verticle_padding.dart';

class EventSearchDelegate extends SearchDelegate<Event> {
  final List<Event> events;

  EventSearchDelegate(this.events);

  @override
  List<Widget> buildActions(BuildContext context) {
    return [
      IconButton(
        icon: Icon(Icons.clear),
        onPressed: () {
          query = '';
        },
      ),
    ];
  }

  @override
  Widget buildLeading(BuildContext context) {
    return IconButton(
      icon: Icon(Icons.arrow_back),
      onPressed: () {
        Navigator.of(context).pop();
      },
    );
  }

  @override
  Widget buildResults(BuildContext context) {
    List<Event> filteredEvents = events
        .where(
            (event) => event.name.toLowerCase().contains(query.toLowerCase()))
        .toList();

    return filteredEvents.isEmpty 
    ? PaddingBoxVertical(
      slab: 1,
      child: Center(
        child: Text(
          "No Events Found!",
          style: TextStyle(
            color: AppColors.blackColor.withOpacity(0.5),
            fontSize: 18,
          ),
        ),
      ),
    )
    : ListView.builder(
      itemCount: filteredEvents.length,
      itemBuilder: (context, index) {
        return PaddingBoxVertical(
          slab: 1,
          child: EventCard(
            imageUrl: events[index].imageUrl,
            iconColor: AppColors.primaryColor,
            textColor: AppColors.blackColor,
            text: events[index].name,
            subText: croppedDescription(
              events[index].description,
            ),
            eventStartTimestamp: events[index].eventStartTimestamp,
            secondLastIcon: Icons.info_outline,
            venue: events[index].venue,
            amount: events[index].registrationFee,
            iconEnd: Icons.qr_code,
            onSecondLastIconTap: () => context.router.push(
              EventDetailsRoute(
                showRegistrationButton: true,
                event: events[index],
              ),
            ),
            onEndIconTap: () {
              context.router.push(
                EventAttendanceQrRoute(event: events[index]),
              );
            },
          ),
        );
      },
    );
  }

  @override
  Widget buildSuggestions(BuildContext context) {
    List<Event> suggestionList = events
        .where(
            (event) => event.name.toLowerCase().contains(query.toLowerCase()))
        .toList();

    return suggestionList.isEmpty
    ? PaddingBoxVertical(
      slab: 1,
      child: Center(
        child: Text(
          "No Events Found!",
          style: TextStyle(
            color: AppColors.blackColor.withOpacity(0.5),
            fontSize: 18,
          ),
        ),
      ),
    )
    : ListView.builder(
      itemCount: suggestionList.length,
      itemBuilder: (context, index) {
        return PaddingBoxVertical(
          slab: 1,
          child: EventCard(
            imageUrl: events[index].imageUrl,
            iconColor: AppColors.primaryColor,
            textColor: AppColors.blackColor,
            text: events[index].name,
            subText: croppedDescription(
              events[index].description,
            ),
            eventStartTimestamp: events[index].eventStartTimestamp,
            secondLastIcon: Icons.info_outline,
            venue: events[index].venue,
            amount: events[index].registrationFee,
            iconEnd: Icons.qr_code,
            onSecondLastIconTap: () => context.router.push(
              EventDetailsRoute(
                showRegistrationButton: true,
                event: events[index],
              ),
            ),
            onEndIconTap: () {
              context.router.push(
                EventAttendanceQrRoute(event: events[index]),
              );
            },
          ),
        );
      },
    );
  }
}
