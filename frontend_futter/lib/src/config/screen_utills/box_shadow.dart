import 'package:flutter/material.dart';
import 'package:cardpay/src/config/themes/colors.dart';

const double _borderRadiusValue = 30.0;

class CustomBoxDecoration {
  static BoxDecoration getDecoration() {
    return BoxDecoration(
      color: AppColors.secondaryColor,
      borderRadius: const BorderRadius.only(
        topLeft: Radius.circular(_borderRadiusValue),
        topRight: Radius.circular(_borderRadiusValue),
      ),
      boxShadow: const [
        // BoxShadow(
        //   color: AppColors.greyColor,
        //   blurRadius: 10.0,
        //   spreadRadius: 5.0,
        //   offset: Offset(
        //     3.0,
        //     3.0,
        //   ),
        // )
      ],
    );
  }
}
