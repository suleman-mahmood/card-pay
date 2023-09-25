import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:cardpay/src/config/themes/colors.dart';

class NumberButton extends HookWidget {
  final String digit;
  final TextEditingController controller;
  final Color? buttonColor;

  const NumberButton({
    Key? key,
    required this.digit,
    required this.controller,
    this.buttonColor,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () {
        controller.text += digit;
      },
      behavior: HitTestBehavior.translucent,
      child: Container(
        alignment: Alignment.center,
        child: digit == 'X'
            ? _buildXButton()
            : _buildDigitButton(context, buttonColor),
      ),
    );
  }

  Widget _buildXButton() {
    return _GestureDetectorButton(
      child: const Icon(Icons.close),
    );
  }

  Widget _buildDigitButton(BuildContext context, Color? color) {
    return _GestureDetectorButton(
      child: Text(
        digit,
        style: AppTypography.mainHeadingGrey
            .copyWith(color: color ?? AppColors.secondaryColor),
      ),
    );
  }
}

class _GestureDetectorButton extends HookWidget {
  final Widget child;

  const _GestureDetectorButton({
    required this.child,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      alignment: Alignment.center,
      child: child,
    );
  }
}
