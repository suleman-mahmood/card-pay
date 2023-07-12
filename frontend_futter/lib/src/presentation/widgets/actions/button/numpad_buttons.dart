import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:cardpay/src/config/themes/colors.dart';
import 'package:cardpay/src/presentation/widgets/actions/button/backspace_button.dart';
import 'package:cardpay/src/presentation/widgets/number_pad/numpad_controllers.dart';

class NumPad extends HookWidget {
  final TextEditingController controller;
  final Color? buttonColor;

  const NumPad({
    super.key,
    required this.controller,
    this.buttonColor,
  });

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.only(top: 5),
      child: Column(
        children: [
          for (int row = 0; row < 3; row++)
            NumberPadRow(
              row: row,
              controller: controller,
              buttonColor: buttonColor,
              height: 80,
            ),
          NumberPadLastRow(
            controller: controller,
            buttonColor: buttonColor,
            height: 80,
          ),
        ],
      ),
    );
  }
}

class NumberPadRow extends HookWidget {
  final int row;
  final TextEditingController controller;
  final Color? buttonColor;
  final double height;

  const NumberPadRow({
    super.key,
    required this.row,
    required this.controller,
    this.buttonColor,
    required this.height,
  });

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      height: height,
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
        children: [
          for (int digit = 1 + row * 3; digit <= 3 + row * 3; digit++)
            if (digit <= 9)
              NumberButton(
                digit: digit.toString(),
                controller: controller,
                buttonColor: buttonColor,
              ),
        ],
      ),
    );
  }
}

class NumberPadLastRow extends StatelessWidget {
  final TextEditingController controller;
  final Color? buttonColor;
  final double height;

  const NumberPadLastRow({
    super.key,
    required this.controller,
    this.buttonColor,
    required this.height,
  });

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      height: height,
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
        children: [
          NumberButton(
            digit: '',
            controller: controller,
            buttonColor: buttonColor,
          ),
          NumberButton(
            digit: '0',
            controller: controller,
            buttonColor: buttonColor,
          ),
          BackspaceButton(
            controller: controller,
            color: AppColors.greyColor,
          ),
        ],
      ),
    );
  }
}
