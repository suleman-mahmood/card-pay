import 'package:cardpay/src/config/screen_utills/box_decoration_all.dart';
import 'package:cardpay/src/config/themes/colors.dart';
import 'package:flutter/material.dart';

class ListItemLoading extends StatelessWidget {
  const ListItemLoading({Key? key});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Container(
            width: double.infinity,
            height: 24,
            decoration: CustomBoxDecorationAll.getDecoration(
                color: AppColors.lightGreyColor),
          ),
          const SizedBox(height: 16),
          Container(
            width: 250,
            height: 24,
            decoration: CustomBoxDecorationAll.getDecoration(
                color: AppColors.lightGreyColor),
          ),
        ],
      ),
    );
  }
}
