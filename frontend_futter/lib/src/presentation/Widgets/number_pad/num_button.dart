import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:frontend_futter/src/config/themes/colors.dart';

class NumberButton extends HookWidget {
  final String digit;
  final TextEditingController controller;

  const NumberButton({
    required this.digit,
    required this.controller,
  });

  @override
  Widget build(BuildContext context) {
    if (digit == 'X') {
      return GestureDetector(
        onTap: () {
          controller.text += digit;
        },
        child: Container(
          width: 64,
          height: 64,
          alignment: Alignment.center,
          child: Icon(Icons.close),
        ),
      );
    }

    return GestureDetector(
      onTap: () {
        controller.text += digit;
      },
      child: Container(
        width: 64,
        height: 64,
        alignment: Alignment.center,
        child: Text(
          digit,
          style: TextStyle(
            color: AppColors.secondaryColor,
            fontSize: 24,
          ),
        ),
      ),
    );
  }
}
