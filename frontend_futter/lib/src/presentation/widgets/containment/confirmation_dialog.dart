import 'package:cardpay/src/config/screen_utills/box_shadow.dart';
import 'package:flutter/material.dart';
import 'package:cardpay/src/config/themes/colors.dart';

class ConfirmationContainer extends StatelessWidget {
  final String title1;
  final String title2;
  final String text1;
  final String text2;
  const ConfirmationContainer({
    super.key,
    required this.title1,
    required this.text1,
    required this.title2,
    required this.text2,
  });
  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(10),
      height: 180,
      width: 320,
      decoration: CustomBoxDecoration.getDecoration(),
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Text(title1, style: AppTypography.subHeading),
        Text(text1, style: AppTypography.mainHeading),
        Text(title2, style: AppTypography.subHeading),
        Text(text2, style: AppTypography.mainHeading)
      ]),
    );
  }
}
