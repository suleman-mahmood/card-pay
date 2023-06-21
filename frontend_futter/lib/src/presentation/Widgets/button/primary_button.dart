import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:frontend_futter/src/config/themes/colors.dart';

class CustomButton extends HookWidget {
  final String text;
  final VoidCallback onPressed;

  const CustomButton({
    required this.text,
    required this.onPressed,
  });

  EdgeInsets calculateMargin(BuildContext context) {
    final buttonWidth = MediaQuery.of(context).size.width;
    final buttonHeight = buttonWidth * 96 / 542;

    final marginVertical = buttonHeight * 0.03;
    final marginHorizontal = buttonWidth * 0.05;

    return EdgeInsets.fromLTRB(
        marginHorizontal, marginVertical, marginHorizontal, 0);
  }

  EdgeInsets calculatePadding(BuildContext context) {
    final buttonWidth = MediaQuery.of(context).size.width;
    final buttonHeight = buttonWidth * 96 / 542;

    final paddingVertical = buttonHeight * 0.07;
    final paddingHorizontal = buttonWidth * 0.13;

    return EdgeInsets.symmetric(
        vertical: paddingVertical, horizontal: paddingHorizontal);
  }

  @override
  Widget build(BuildContext context) {
    final margin = useMemoized(() => calculateMargin(context));
    final padding = useMemoized(() => calculatePadding(context));

    return Container(
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
        child: Padding(
          padding: padding,
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
