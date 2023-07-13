import 'package:cardpay/src/presentation/widgets/boxes/height_box.dart';
import 'package:flutter/material.dart';
import 'package:cardpay/src/config/themes/colors.dart';

class ConfirmationContainer extends StatelessWidget {
  final String title1;
  final String title2;
  final String text1;
  final String text2;

  const ConfirmationContainer({
    Key? key,
    required this.title1,
    required this.text1,
    required this.title2,
    required this.text2,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(
      builder: (context, constraints) {
        return Container(
          padding: const EdgeInsets.all(10),
          width: constraints.maxWidth,
          decoration: BoxDecoration(
            color: AppColors.secondaryColor,
            borderRadius: const BorderRadius.all(
              Radius.circular(30),
            ),
            boxShadow: [
              BoxShadow(
                color: AppColors.greyColor.withOpacity(0.25),
                blurRadius: 10.0,
                spreadRadius: 5.0,
                offset: Offset(
                  5.0,
                  5.0,
                ),
              ),
            ],
          ),
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 15.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('Details', style: AppTypography.subHeading),
                HeightBox(slab: 3),
                Text(title1, style: AppTypography.subHeading),
                Text(text1, style: AppTypography.mainHeading),
                Text(title2, style: AppTypography.subHeading),
                Text(text2, style: AppTypography.mainHeading),
              ],
            ),
          ),
        );
      },
    );
  }
}
