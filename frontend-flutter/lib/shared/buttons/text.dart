import 'package:cardpay/shared/typography/main_heading.dart';
import 'package:cardpay/theme/colors.dart';
import 'package:flutter/material.dart';
import 'package:flutter/src/foundation/key.dart';
import 'package:flutter/src/widgets/framework.dart';

class TextButtonWidget extends StatelessWidget {
  // Configurations
  final double buttonBorderRadius = 20;
  final double paddingText = 10;
  final double fontSize = 20;

  final String content;
  final bool invertColors;
  final VoidCallback onPressed;

  const TextButtonWidget({
    Key? key,
    required this.content,
    required this.onPressed,
    this.invertColors = false,
  }) : super(key: key);

  Color showPrimaryColorDisplay() {
    return invertColors ? AppColors().PrimaryColor : AppColors().SecondaryColor;
  }

  Color showSecondaryColorDisplay() {
    return invertColors ? AppColors().SecondaryColor : AppColors().PrimaryColor;
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        ElevatedButton(
          style: ButtonStyle(
            shape: MaterialStateProperty.all(
              RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(buttonBorderRadius),
              ),
            ),
            padding: MaterialStateProperty.all(
              EdgeInsets.all(paddingText),
            ),
            backgroundColor: MaterialStateProperty.all(
              showSecondaryColorDisplay(),
            ),
          ),
          onPressed: onPressed,
          child: Text(
            content,
            style: TextStyle(
              fontSize: fontSize,
              color: showPrimaryColorDisplay(),
            ),
          ),
        ),
      ],
    );
  }
}
