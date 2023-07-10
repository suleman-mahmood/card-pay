import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:frontend_futter/src/config/screen_utills/screen_util.dart';
import 'package:frontend_futter/src/config/themes/colors.dart';

class TransactionContainer extends HookWidget {
  final IconData icon;
  final String firstText;
  final String secondText;
  final Color firstTextColor;
  final Color secondTextColor;
  final Color iconColor;

  const TransactionContainer({super.key, 
    required this.icon,
    required this.firstText,
    required this.secondText,
    this.firstTextColor = AppColors.blackColor,
    this.secondTextColor = AppColors.redColor,
    this.iconColor = AppColors.primaryColor,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Align(
      alignment: Alignment.center,
      child: Container(
        margin: EdgeInsets.all(
            ScreenUtil.widthMultiplier(context) * 1), // 2% of screen width
        padding: EdgeInsets.symmetric(
            vertical: ScreenUtil.heightMultiplier(context) *
                0.9, // 1% of screen height
            horizontal:
                ScreenUtil.widthMultiplier(context) * 3 // 3% of screen width
            ),
        decoration: BoxDecoration(
          color: AppColors.secondaryColor,
          borderRadius: BorderRadius.circular(10),
          boxShadow: [
            BoxShadow(
              color: AppColors.greyColor.withOpacity(0.4),
              spreadRadius: ScreenUtil.widthMultiplier(context) *
                  0.7, // 1% of screen width
              blurRadius: ScreenUtil.widthMultiplier(context) *
                  1.5, // 2% of screen width
              offset: Offset(0,
                  ScreenUtil.heightMultiplier(context)), // 1% of screen height
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
      size: ScreenUtil.imageSizeMultiplier(context) * 4, // 7% of screen width
    );
  }

  Padding buildFirstText(BuildContext context) {
    return Padding(
      padding: EdgeInsets.only(
          left: ScreenUtil.widthMultiplier(context) * 1.5, // 3% of screen width
          top:
              ScreenUtil.heightMultiplier(context) * 0.8, // 1% of screen height
          bottom: ScreenUtil.heightMultiplier(context) // 1% of screen height
          ),
      child: Text(
        firstText,
        overflow: TextOverflow.ellipsis,
        textAlign: TextAlign.left,
        style: Theme.of(context).textTheme.bodyLarge?.copyWith(
              color: firstTextColor,
              fontSize: ScreenUtil.textMultiplier(context) *
                  1.9, // 2.2% of screen height
              fontWeight: FontWeight.w600,
            ),
      ),
    );
  }

  Padding buildSecondText(BuildContext context) {
    return Padding(
      padding: EdgeInsets.only(
          top: ScreenUtil.heightMultiplier(context), // 1% of screen height
          bottom: ScreenUtil.heightMultiplier(context) // 1% of screen height
          ),
      child: Text(
        secondText,
        overflow: TextOverflow.ellipsis,
        textAlign: TextAlign.left,
        style: Theme.of(context).textTheme.bodyLarge?.copyWith(
              color: secondTextColor,
              fontSize: ScreenUtil.textMultiplier(context) *
                  2.2, // 2.2% of screen height
              fontWeight: FontWeight.w600,
            ),
      ),
    );
  }
}
