import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:frontend_futter/src/config/themes/colors.dart';

class RadioButton extends HookWidget {
  final bool filled;

  const RadioButton({required this.filled});

  @override
  Widget build(BuildContext context) {
    return Container(
      child: Padding(
        padding: const EdgeInsets.all(2.0),
        child: Container(
          width: 14,
          height: 14,
          decoration: BoxDecoration(
            shape: BoxShape.circle,
            color: filled ? AppColors.secondaryColor : Colors.transparent,
            border: Border.all(
              color: AppColors.secondaryColor,
              width: 1.0,
            ),
          ),
        ),
      ),
    );
  }
}
