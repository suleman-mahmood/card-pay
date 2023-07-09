import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:frontend_futter/src/config/themes/colors.dart';

class NumberButton extends HookWidget {
  final String digit;
  final TextEditingController controller;
  final Color? buttonColor;

  const NumberButton({
    required this.digit,
    required this.controller,
    this.buttonColor,
  });

  @override
  Widget build(BuildContext context) {
    final screenWidth = MediaQuery.of(context).size.width;
    final screenHeight = MediaQuery.of(context).size.height;

    return Padding(
      padding: EdgeInsets.all(screenWidth * 0.01), // make padding responsive
      child: InkWell(
        onTap: () {
          controller.text += digit;
        },
        child: digit == 'X'
            ? _buildXButton(screenWidth, screenHeight)
            : _buildDigitButton(screenWidth, screenHeight, context),
      ),
    );
  }

  Widget _buildXButton(double screenWidth, double screenHeight) {
    return _InkWellButton(
      width: screenWidth * 0.15,
      height: screenHeight * 0.1,
      child: Icon(Icons.close),
    );
  }

  Widget _buildDigitButton(
      double screenWidth, double screenHeight, BuildContext context) {
    return _InkWellButton(
      width: screenWidth * 0.15,
      height: screenHeight * 0.1,
      child: Text(
        digit,
        style: TextStyle(
          color: buttonColor ?? AppColors.secondaryColor,
          fontSize: screenHeight * 0.05,
          fontFamily: 'popins',
        ),
      ),
    );
  }
}

class _InkWellButton extends StatelessWidget {
  final double width;
  final double height;
  final Widget child;

  const _InkWellButton({
    required this.width,
    required this.height,
    required this.child,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      width: width,
      height: height,
      alignment: Alignment.center,
      child: child,
    );
  }
}
