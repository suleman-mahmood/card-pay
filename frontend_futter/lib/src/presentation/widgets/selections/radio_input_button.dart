import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:cardpay/src/config/themes/colors.dart';

class RadioButton extends HookWidget {
  final bool filled;

  const RadioButton({super.key, required this.filled});

  @override
  Widget build(BuildContext context) {
    const borderWidth = 1.0;

    return Padding(
      padding: EdgeInsets.all(5),
      child: _buildRadioButton(borderWidth, context),
    );
  }

  Container _buildRadioButton(double borderWidth, BuildContext context) {
    return Container(
      width: 25,
      height: 25,
      decoration: BoxDecoration(
        shape: BoxShape.circle,
        color: filled ? AppColors.secondaryColor : Colors.transparent,
        border: Border.all(
          color: AppColors.secondaryColor,
          width: borderWidth,
        ),
      ),
    );
  }
}
