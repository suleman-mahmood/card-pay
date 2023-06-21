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
    final screenHeight = MediaQuery.of(context).size.height;
    final screenWidth = MediaQuery.of(context).size.width;

    if (digit == 'X') {
      return Padding(
        padding: EdgeInsets.all(10.0),
        child: InkWell(
          onTap: () {
            controller.text += digit;
          },
          child: Container(
            width: screenWidth * 0.15,
            height: screenHeight * 0.1,
            alignment: Alignment.center,
            child: Icon(Icons.close),
          ),
        ),
      );
    }

    return Padding(
      padding: EdgeInsets.all(10.0),
      child: InkWell(
        onTap: () {
          controller.text += digit;
        },
        child: Container(
          width: screenWidth * 0.15,
          height: screenHeight * 0.1,
          alignment: Alignment.center,
          child: Text(
            digit,
            style: TextStyle(
              color: AppColors.secondaryColor,
              fontSize: screenHeight * 0.04,
            ),
          ),
        ),
      ),
    );
  }
}
