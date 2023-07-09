import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:frontend_futter/src/config/screen_utills/screen_util.dart';
import 'package:frontend_futter/src/config/themes/colors.dart';

class BalanceCard extends HookWidget {
  final String balance;
  final String topRightImage;
  final String bottomLeftImage;

  BalanceCard({
    required this.balance,
    required this.topRightImage,
    required this.bottomLeftImage,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      width: double.infinity,
      decoration: BoxDecoration(
        color: AppColors.purpleColor,
        borderRadius: BorderRadius.circular(10),
      ),
      child: Stack(
        children: [
          _cardContent(context),
          _topRightImage(context),
          _bottomLeftImage(context),
        ],
      ),
    );
  }

  Padding _cardContent(BuildContext context) {
    return Padding(
      padding: EdgeInsets.all(ScreenUtil.blockSizeVertical(context) * 4),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  _balanceTitle(context),
                  _balanceAmount(context),
                ],
              ),
            ],
          ),
        ],
      ),
    );
  }

  Text _balanceTitle(BuildContext context) {
    return Text(
      "Total Balance",
      style: AppTypography.headingFont.copyWith(
        color: AppColors.secondaryColor,
        fontSize: ScreenUtil.textMultiplier(context) * 1.9,
      ),
    );
  }

  Text _balanceAmount(BuildContext context) {
    return Text(
      balance,
      style: AppTypography.mainHeading.copyWith(
        color: AppColors.secondaryColor,
        fontSize: ScreenUtil.textMultiplier(context) * 3.5,
      ),
    );
  }

  Positioned _topRightImage(BuildContext context) {
    return Positioned(
      top: 0,
      right: 0,
      child: Image.asset(
        topRightImage,
        width: ScreenUtil.widthMultiplier(context) * 18,
        height: ScreenUtil.heightMultiplier(context) * 9,
      ),
    );
  }

  Positioned _bottomLeftImage(BuildContext context) {
    return Positioned(
      bottom: 0,
      left: 0,
      child: Image.asset(
        bottomLeftImage,
        width: ScreenUtil.widthMultiplier(context) * 13,
        height: ScreenUtil.heightMultiplier(context) * 4.5,
      ),
    );
  }
}
