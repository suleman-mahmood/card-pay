import 'package:cardpay/src/config/themes/colors.dart';
import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';

class CustomDivider extends HookWidget {
  final double? height;
  final double? thickness;
  final double? indent;
  final double? endIndent;
  final Color? color;

  const CustomDivider({
    Key? key,
    this.height,
    this.thickness,
    this.indent,
    this.endIndent,
    this.color,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
      child: Divider(
        height: height ?? 20,
        thickness: thickness ?? 5,
        indent: indent ?? 20,
        endIndent: endIndent ?? 20,
        color: color ?? AppColors.greyColor,
      ),
    );
  }
}
