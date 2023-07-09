import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:frontend_futter/src/config/themes/colors.dart';

class RadioButton extends HookWidget {
  final bool filled;

  const RadioButton({required this.filled});

  @override
  Widget build(BuildContext context) {
    final screenWidth = MediaQuery.of(context).size.width;
    final screenHeight = MediaQuery.of(context).size.height;
    final borderWidth = 1.0;

    return Padding(
      padding: EdgeInsets.all(screenWidth * 0.003),
      child: _buildRadioButton(screenWidth, screenHeight, borderWidth, context),
    );
  }

  Container _buildRadioButton(double screenWidth, double screenHeight,
      double borderWidth, BuildContext context) {
    return Container(
      width: screenWidth * 0.055,
      height: screenHeight * 0.055,
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
