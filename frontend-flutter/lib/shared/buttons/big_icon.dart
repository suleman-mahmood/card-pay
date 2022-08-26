import 'package:flutter/material.dart';

class BigIconButtonCustomWidget extends StatelessWidget {
  // Configurations
  final double borderWidth = 5;
  final double paddingHorizontal = 10;
  final double paddingVertical = 10;
  final double buttonSize = 75;
  final double buttonBorderRadius = 30;
  final Color borderColor = Colors.blue[800]!;

  final IconData icon;
  final VoidCallback onPressed;

  BigIconButtonCustomWidget({
    Key? key,
    required this.icon,
    required this.onPressed,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return OutlinedButton(
      style: ButtonStyle(
        shape: MaterialStateProperty.all(
          RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(buttonBorderRadius),
          ),
        ),
        side: MaterialStateProperty.all(
          BorderSide(
            color: borderColor,
            width: borderWidth,
          ),
        ),
      ),
      onPressed: onPressed,
      child: Padding(
        padding: EdgeInsets.symmetric(
          horizontal: paddingHorizontal,
          vertical: paddingVertical,
        ),
        child: SizedBox.square(
          dimension: buttonSize,
          child: Icon(
            icon,
            size: buttonSize,
          ),
        ),
      ),
    );
  }
}
