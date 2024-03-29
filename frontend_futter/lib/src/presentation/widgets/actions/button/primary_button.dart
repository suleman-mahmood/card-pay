import 'package:flutter/material.dart';
import 'package:cardpay/src/config/themes/colors.dart';
import 'package:flutter_hooks/flutter_hooks.dart';

class PrimaryButton extends HookWidget {
  final String text;
  final VoidCallback onPressed;
  final Color color;
  final Color textColor;

  const PrimaryButton({
    super.key,
    required this.text,
    required this.onPressed,
    this.color = AppColors.primaryColor,
    this.textColor = AppColors.secondaryColor,
  });

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: MediaQuery.of(context).size.width * 5 / 7,
      height: MediaQuery.of(context).size.width * 13 / 100,
      child: ElevatedButton(
        onPressed: onPressed,
        style: ButtonStyle(
          backgroundColor: MaterialStateProperty.all<Color>(color),
          shape: MaterialStateProperty.all<RoundedRectangleBorder>(
            RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(10),
            ),
          ),
        ),
        child: Text(
          text,
          style: AppTypography.headingFont.copyWith(
            color: textColor,
          ),
        ),
      ),
    );
  }
}
