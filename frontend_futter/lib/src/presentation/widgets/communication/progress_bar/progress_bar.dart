import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:cardpay/src/config/screen_utills/screen_util.dart';
import 'package:cardpay/src/config/themes/colors.dart';

class CustomProgressBar extends HookWidget {
  final double progress;
  final Color progressColor;
  final Color backgroundColor;

  const CustomProgressBar({
    super.key,
    required this.progress,
    this.progressColor = AppColors.primaryColor,
    this.backgroundColor = AppColors.greyColor,
  });

  @override
  Widget build(BuildContext context) {
    final height = ScreenUtil.blockSizeVertical(context) * 0.6;

    final valueColor =
        useMemoized(() => AlwaysStoppedAnimation<Color>(progressColor));

    return SizedBox(
      height: height,
      child: LinearProgressIndicator(
        value: progress,
        valueColor: valueColor,
        backgroundColor: backgroundColor,
      ),
    );
  }
}
