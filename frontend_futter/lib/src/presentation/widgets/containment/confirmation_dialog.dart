import 'package:flutter/material.dart';
import 'package:frontend_futter/src/config/themes/colors.dart';
import 'package:frontend_futter/src/config/screen_utills/screen_util.dart';

class ConfirmationContainer extends StatelessWidget {
  final String title1;
  final String title2;
  final String text1;
  final String text2;

  ConfirmationContainer({
    required this.title1,
    required this.text1,
    required this.title2,
    required this.text2,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: EdgeInsets.all(ScreenUtil.blockSizeHorizontal(context) *
          10), // using blockSizeHorizontal for responsive padding
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.all(
          Radius.circular(ScreenUtil.blockSizeHorizontal(context) *
              3), // using blockSizeHorizontal for responsive radius
        ),
        boxShadow: [
          BoxShadow(
            color: Colors.grey.withOpacity(0.5),
            spreadRadius: ScreenUtil.blockSizeHorizontal(context) *
                1, // using blockSizeHorizontal for responsive spread radius
            blurRadius: ScreenUtil.blockSizeHorizontal(context) *
                2, // using blockSizeHorizontal for responsive blur radius
            offset: Offset(
                0,
                ScreenUtil.blockSizeVertical(context) *
                    1), // using blockSizeVertical for responsive offset
          ),
        ],
      ),
      child: Column(children: [
        Text(
          title1,
          style: AppTypography.inputFont.copyWith(
              color: AppColors.greyColor,
              fontSize: ScreenUtil.textMultiplier(context) *
                  2 // using textMultiplier for responsive font size
              ),
        ),
        Text(
          text1,
          style: AppTypography.mainHeading.copyWith(
              fontSize: ScreenUtil.textMultiplier(context) *
                  3 // using textMultiplier for responsive font size
              ),
        ),
        Text(
          title2,
          style: AppTypography.inputFont.copyWith(
              color: AppColors.greyColor,
              fontSize: ScreenUtil.textMultiplier(context) *
                  2 // using textMultiplier for responsive font size
              ),
        ),
        Text(
          text2,
          style: AppTypography.mainHeading.copyWith(
              fontSize: ScreenUtil.textMultiplier(context) *
                  3 // using textMultiplier for responsive font size
              ),
        )
      ]),
    );
  }
}
