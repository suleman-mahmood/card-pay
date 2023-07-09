import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:frontend_futter/src/config/themes/colors.dart';

class BackspaceButton extends HookWidget {
  final TextEditingController controller;
  final Color color;
  final double widthFactor;
  final double heightFactor;
  final double iconFactor;

  const BackspaceButton({
    required this.controller,
    this.color = AppColors.secondaryColor,
    this.widthFactor = 0.15,
    this.heightFactor = 0.1,
    this.iconFactor = 0.04,
  });

  @override
  Widget build(BuildContext context) {
    final screenHeight = MediaQuery.of(context).size.height;
    final screenWidth = MediaQuery.of(context).size.width;

    return GestureDetector(
      onTap: () {
        final text = controller.text;
        if (text.isNotEmpty) {
          controller.text = text.substring(0, text.length - 1);
        }
      },
      child: Container(
        width: screenWidth * widthFactor,
        height: screenHeight * heightFactor,
        alignment: Alignment.center,
        child: Icon(
          Icons.backspace,
          color: color,
          size: screenHeight * iconFactor,
        ),
      ),
    );
  }
}
