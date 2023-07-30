import 'package:flutter/material.dart';
import 'package:cardpay/src/config/themes/colors.dart';

class CustomBoxDecorationAll {
  static BoxDecoration getDecoration({
    Color? color,
    double borderRadiusValue = 8.0,
    Color? shadowColor,
    double blurRadius = 3.0,
    double spreadRadius = 3.0,
    Offset? shadowOffset,
  }) {
    return BoxDecoration(
      color: color ?? AppColors.primaryColor,
      borderRadius: BorderRadius.all(Radius.circular(borderRadiusValue)),
      boxShadow: [
        BoxShadow(
          color: shadowColor ?? AppColors.lightGreyColor,
          blurRadius: blurRadius,
          spreadRadius: spreadRadius,
          offset: shadowOffset ?? Offset(1.0, 2.0),
        ),
      ],
    );
  }
}
