import 'package:cardpay/theme/colors.dart';
import 'package:flutter/material.dart';

class NumberButtonCustomWidget extends StatelessWidget {
  // Configurations
  final double buttonBorderRadius = 20;

  final int number;
  final bool invertColors;
  final VoidCallback onPressed;

  const NumberButtonCustomWidget({
    Key? key,
    required this.number,
    required this.onPressed,
    this.invertColors = false,
  }) : super(key: key);

  Color showPrimaryColorDisplay() {
    return invertColors ? AppColors().primaryColor : AppColors().secondaryColor;
  }

  Color showSecondaryColorDisplay() {
    return invertColors ? AppColors().secondaryColor : AppColors().primaryColor;
  }

  @override
  Widget build(BuildContext context) {
    return ElevatedButton(
      style: ButtonStyle(
        shape: MaterialStateProperty.all(
          RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(buttonBorderRadius),
            side: BorderSide(
              color: showPrimaryColorDisplay(),
              width: 2,
            ),
          ),
        ),
        backgroundColor: MaterialStateProperty.all(
          showSecondaryColorDisplay(),
        ),
      ),
      onPressed: onPressed,
      child: Text(
        number.toString(),
        style: TextStyle(color: showPrimaryColorDisplay()),
      ),
    );
  }
}
