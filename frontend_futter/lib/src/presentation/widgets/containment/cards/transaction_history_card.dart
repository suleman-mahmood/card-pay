import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:cardpay/src/config/themes/colors.dart';

class TransactionContainer extends HookWidget {
  final IconData icon;
  final String firstText;
  final String secondText;
  final Color firstTextColor;
  final Color secondTextColor;
  final Color iconColor;
  final bool display;

  const TransactionContainer({
    super.key,
    required this.icon,
    required this.firstText,
    required this.secondText,
    this.firstTextColor = AppColors.blackColor,
    this.secondTextColor = AppColors.redColor,
    this.iconColor = AppColors.primaryColor,
    this.display = false,
  });

  @override
  Widget build(BuildContext context) {
    return Align(
      alignment: Alignment.center,
      child: Container(
        margin: EdgeInsets.all(4),
        padding: EdgeInsets.symmetric(vertical: 3, horizontal: 5),
        decoration: BoxDecoration(
          color: AppColors.secondaryColor,
          borderRadius: BorderRadius.circular(10),
          boxShadow: [
            BoxShadow(
              color: AppColors.greyColor.withOpacity(0.2),
              spreadRadius: 2,
              blurRadius: 5,
              offset: Offset(0, 4),
            ),
          ],
        ),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.center,
          mainAxisSize: MainAxisSize.min,
          children: [
            buildIcon(context),
            buildFirstText(context),
            const Spacer(),
            buildSecondText(context),
          ],
        ),
      ),
    );
  }

  Icon buildIcon(BuildContext context) {
    return Icon(
      icon,
      color: iconColor,
    );
  }

  Widget buildFirstText(BuildContext context) {
    return Padding(
      padding: EdgeInsets.all(10),
      child: Column(
        children: [
          Text(firstText, style: AppTypography.bodyText),
          if (display) Text('send', style: AppTypography.subHeadingBold),
        ],
      ),
    );
  }

  Padding buildSecondText(BuildContext context) {
    return Padding(
      padding: EdgeInsets.all(10),
      child: Text(
        secondText,
        style: AppTypography.bodyText.copyWith(color: secondTextColor),
      ),
    );
  }
}
