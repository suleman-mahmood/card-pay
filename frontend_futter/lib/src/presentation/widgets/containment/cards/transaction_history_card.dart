import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:cardpay/src/config/screen_utills/screen_util.dart';
import 'package:cardpay/src/config/themes/colors.dart';

class TransactionContainer extends HookWidget {
  final IconData icon;
  final String firstText;
  final String secondText;
  final Color firstTextColor;
  final Color secondTextColor;
  final Color iconColor;

  const TransactionContainer({
    super.key,
    required this.icon,
    required this.firstText,
    required this.secondText,
    this.firstTextColor = AppColors.blackColor,
    this.secondTextColor = AppColors.redColor,
    this.iconColor = AppColors.primaryColor,
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
              blurRadius: 10,
              offset: Offset(0, ScreenUtil.heightMultiplier(context)),
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

  Padding buildFirstText(BuildContext context) {
    return Padding(
      padding: EdgeInsets.only(
          left: ScreenUtil.widthMultiplier(context), // 3% of screen width
          top: ScreenUtil.heightMultiplier(context), // 1% of screen height
          bottom: ScreenUtil.heightMultiplier(context) // 1% of screen height
          ),
      child: Text(firstText, style: AppTypography.bodyText),
    );
  }

  Padding buildSecondText(BuildContext context) {
    return Padding(
      padding: EdgeInsets.only(
          top: ScreenUtil.heightMultiplier(context),
          bottom: ScreenUtil.heightMultiplier(context)),
      child: Text(
        secondText,
        style: AppTypography.bodyText.copyWith(color: secondTextColor),
      ),
    );
  }
}
