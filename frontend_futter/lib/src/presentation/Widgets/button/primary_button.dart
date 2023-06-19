import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:frontend_futter/src/config/themes/colors.dart';

class CustomButton extends HookWidget {
  final String text;
  final VoidCallback onPressed;
  final double width;
  final double height;

  const CustomButton({
    required this.text,
    required this.onPressed,
    this.width = 272,
    this.height = 48,
  });

  EdgeInsets calculateMargin(BuildContext context) {
    return EdgeInsets.only(
      top: 0.03 * MediaQuery.of(context).size.height,
      left: 0.05 * MediaQuery.of(context).size.width,
    );
  }

  @override
  Widget build(BuildContext context) {
    final margin = useMemoized(() => calculateMargin(context));

    return Container(
      width: width,
      height: height,
      margin: margin,
      child: ElevatedButton(
        onPressed: onPressed,
        style: ButtonStyle(
          backgroundColor: MaterialStateProperty.all<Color>(
            AppColors.primaryColor,
          ),
          shape: MaterialStateProperty.all<RoundedRectangleBorder>(
            RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(10),
            ),
          ),
        ),
        child: Container(
          alignment: Alignment.center,
          padding: EdgeInsets.symmetric(vertical: 8, horizontal: 16),
          child: Text(
            text,
            style: AppTypography.headingFont.copyWith(
              color: AppColors.secondaryColor,
            ),
          ),
        ),
      ),
    );
  }
}
