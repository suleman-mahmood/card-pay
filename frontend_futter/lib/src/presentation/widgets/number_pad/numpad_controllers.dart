import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:cardpay/src/config/themes/colors.dart';

class NumberButton extends HookWidget {
  final String digit;
  final TextEditingController controller;
  final Color? buttonColor;

  const NumberButton({
    super.key,
    required this.digit,
    required this.controller,
    this.buttonColor,
  }) : super();

  @override
  Widget build(BuildContext context) {
    return Container(
      child: InkWell(
        onTap: () {
          controller.text += digit;
        },
        child: digit == 'X'
            ? _buildXButton()
            : _buildDigitButton(context, buttonColor),
      ),
    );
  }

  Widget _buildXButton() {
    return _InkWellButton(
      child: const Icon(Icons.close),
    );
  }

  Widget _buildDigitButton(BuildContext context, Color? color) {
    return _InkWellButton(
      child: Text(
        digit,
        style: AppTypography.mainHeadingGrey
            .copyWith(color: color ?? AppColors.secondaryColor),
      ),
    );
  }
}

class _InkWellButton extends HookWidget {
  final Widget child;

  const _InkWellButton({
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
