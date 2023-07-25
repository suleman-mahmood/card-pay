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
            height: 70,
            decoration: BoxDecoration(
              color: AppColors.lightGreyColor,
              borderRadius: BorderRadius.circular(8),
            ),
          )
        ],
      ),
    );
  }
}
