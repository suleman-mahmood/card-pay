import 'package:cardpay/src/config/themes/colors.dart';
import 'package:flutter/material.dart';

class CircleListItemLoading extends StatelessWidget {
  const CircleListItemLoading({Key? key});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 8),
      child: Container(
        width: 54,
        height: 54,
        decoration: const BoxDecoration(
            color: AppColors.lightGreyColor, shape: BoxShape.circle),
      ),
    );
  }
}
