import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:cardpay/src/config/themes/colors.dart';

class BalanceCard extends HookWidget {
  final String balance;
  final String topRightImage;
  final String bottomLeftImage;

  const BalanceCard({
    super.key,
    required this.balance,
    required this.topRightImage,
    required this.bottomLeftImage,
  });

  @override
  Widget build(BuildContext context) {
    final deviceHeight = MediaQuery.of(context).size.height;

    Padding _cardContent() {
      return Padding(
        padding: EdgeInsets.all(15),
        child: Column(
          children: [
            Row(
              children: [
                Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text("Total Balance", style: AppTypography.subHeading),
                    Text(balance, style: AppTypography.mainHeadingWhite)
                  ],
                ),
              ],
            ),
          ],
        ),
      );
    }

    Positioned _topRightImage() {
      return Positioned(
        top: 0,
        right: 0,
        child: Image.asset(
          topRightImage,
        ),
      );
    }

    Positioned _bottomLeftImage() {
      return Positioned(
        bottom: 0,
        left: 0,
        child: Image.asset(
          bottomLeftImage,
        ),
      );
    }

    return Container(
      height: deviceHeight * 0.19,
      decoration: BoxDecoration(
        color: AppColors.purpleColor,
        borderRadius: BorderRadius.circular(10),
      ),
      child: Stack(
        children: [
          _cardContent(),
          _topRightImage(),
          _bottomLeftImage(),
        ],
      ),
    );
  }
}
