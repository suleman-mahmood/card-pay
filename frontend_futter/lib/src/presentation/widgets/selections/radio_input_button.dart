import 'package:cardpay/src/presentation/widgets/boxes/horizontal_padding.dart';
import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:cardpay/src/config/themes/colors.dart';

class RadioButton extends HookWidget {
  final bool filled;

  const RadioButton({super.key, required this.filled});

  @override
  Widget build(BuildContext context) {
    const borderWidth = 1.0;

    return PaddingHorizontal(
      slab: 1,
      child: _buildRadioButton(borderWidth, context),
    );
  }

  Container _buildRadioButton(double borderWidth, BuildContext context) {
    return Container(
      width: 16,
      height: 16,
      decoration: BoxDecoration(
        shape: BoxShape.circle,
        color: filled ? AppColors.secondaryColor : AppColors.greyColor,
      ),
    );
  }
}
