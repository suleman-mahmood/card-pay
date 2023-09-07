import 'package:cardpay/src/presentation/widgets/boxes/all_padding.dart';
import 'package:cardpay/src/utils/constants/payment_string.dart';
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

    Widget _cardContent() {
      return PaddingAll(
        slab: 2,
        child: Column(
          children: [
            Row(
              children: [
                Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(PaymentStrings.totalBalance,
                        style: AppTypography.subHeading),
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
        child: ClipRRect(
          borderRadius: BorderRadius.only(
            topRight: Radius.circular(10.0), // Adjust the radius as needed
          ),
          child: Image.asset(
            topRightImage,
          ),
        ),
      );
    }

    Positioned _bottomLeftImage() {
      return Positioned(
        bottom: 0,
        left: 0,
        child: ClipRRect(
          borderRadius: BorderRadius.only(
            bottomLeft: Radius.circular(10.0), // Adjust the radius as needed
          ),
          child: Image.asset(
            bottomLeftImage,
          ),
        ),
      );
    }

    return Card(
      color: AppColors.purpleColor,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(10),
      ),
      child: ConstrainedBox(
        constraints: BoxConstraints(
          minHeight: deviceHeight * 0.19,
        ),
        child: Stack(
          children: [
            _cardContent(),
            _topRightImage(),
            _bottomLeftImage(),
          ],
        ),
      ),
    );
  }
}
