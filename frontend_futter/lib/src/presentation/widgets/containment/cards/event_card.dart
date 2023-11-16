import 'package:cardpay/src/config/themes/colors.dart';
import 'package:flutter/material.dart';
import 'package:intl/intl.dart';

class EventCard extends StatelessWidget {
  final String imageUrl;
  final String text;
  final String? subText;
  final IconData? iconEnd;
  final IconData? secondLastIcon;
  final Color suffixIconColor;
  final Function()? onEndIconTap;
  final Function()? onSecondLastIconTap;
  final bool selected;
  final DateTime eventStartTimestamp;
  final String venue;
  final int amount;

  final Color iconColor;
  final Color textColor;
  final Color backgroundColor;
  final Color subTextColor;

  const EventCard({
    Key? key,
    required this.imageUrl,
    required this.text,
    this.iconEnd,
    this.secondLastIcon,
    this.onSecondLastIconTap,
    this.subText,
    this.onEndIconTap,
    this.selected = false,
    this.iconColor = AppColors.greyColor,
    this.textColor = AppColors.greyColor,
    this.backgroundColor = AppColors.secondaryColor,
    this.subTextColor = AppColors.greyColor,
    this.suffixIconColor = AppColors.greyColor,
    required this.eventStartTimestamp,
    required this.venue,
    required this.amount,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final Color finalBackgroundColor = selected ? Colors.blue : backgroundColor;
    final Color finalTextColor = selected ? Colors.white : textColor;
    return Container(
      width: MediaQuery.of(context).size.width,
      height: 100,
      padding: EdgeInsets.fromLTRB(4, 6, 4, 8),
      margin: EdgeInsets.symmetric(horizontal: 10, vertical: 8),
      decoration: BoxDecoration(
        color: finalBackgroundColor,
        borderRadius: BorderRadius.circular(16),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.05),
            blurRadius: 2,
            offset: Offset(0, 2),
          ),
        ],
      ),
      child: InkWell(
        onTap:  onSecondLastIconTap,
        child: Row(
          mainAxisAlignment: MainAxisAlignment.start,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            imageUrl == ""
                ? Container(
                    width: 80,
                    height: double.infinity,
                    decoration: BoxDecoration(
                      color: AppColors.primaryColor,
                      borderRadius: BorderRadius.circular(16),
                    ),
                    child: Center(
                      child: Text(
                        text.split(" ")[0].substring(0, 1).toUpperCase() +
                            (text.split(" ").length > 1
                                ? text
                                    .split(" ")[1]
                                    .substring(0, 1)
                                    .toUpperCase()
                                : ""),
                        style: TextStyle(
                          color: Colors.white,
                          fontSize: 24,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ))
                : Container(
                    width: 80,
                    height: double.infinity,
                    decoration: BoxDecoration(
                      color: Colors.white,
                      borderRadius: BorderRadius.circular(12),
                      image: DecorationImage(
                        image: NetworkImage(imageUrl),
                        fit: BoxFit.cover,
                      ),
                    ),
                  ),
            SizedBox(width: 8),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    DateFormat('EEE, MMM dd - hh:mm a')
                        .format(eventStartTimestamp),
                    style: AppTypography.mainHeading.copyWith(
                      fontSize: 14,
                      color: AppColors.blueColor,
                    ),
                  ),
                  SizedBox(height: 2),
                  Text(
                    text,
                    overflow: TextOverflow.ellipsis,
                    style: AppTypography.mainHeading.copyWith(
                      fontSize: 18,
                      color: finalTextColor,
                    ),
                  ),
                  const Spacer(),
                  Text(
                    'Rs. $amount',
                    style: TextStyle(
                        color:
                            selected ? AppColors.secondaryColor : subTextColor),
                  )
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
