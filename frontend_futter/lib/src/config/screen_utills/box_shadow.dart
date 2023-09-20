import 'package:flutter/material.dart';
import 'package:cardpay/src/config/themes/colors.dart';

const double _borderRadiusValue = 30.0;

class CustomBoxDecoration {
  static BoxDecoration getDecoration() {
    return const BoxDecoration(
      color: AppColors.secondaryColor,
      borderRadius: BorderRadius.only(
        topLeft: Radius.circular(_borderRadiusValue),
        topRight: Radius.circular(_borderRadiusValue),
      ),
    );
  }
}
