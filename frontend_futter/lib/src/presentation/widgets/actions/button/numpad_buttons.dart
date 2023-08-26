import 'package:cardpay/src/presentation/widgets/number_pad/numpad_controllers.dart';
import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:cardpay/src/config/themes/colors.dart';
import 'package:cardpay/src/presentation/widgets/actions/button/backspace_button.dart';

class NumPad extends HookWidget {
  final TextEditingController controller;
  final Color? buttonColor;

  const NumPad({
    Key? key,
    required this.controller,
    this.buttonColor,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    useEffect(() {
      return () {
        controller.dispose();
      };
    }, []);
    return Padding(
      padding: EdgeInsets.only(top: 16),
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
    Key? key,
    required this.row,
    required this.controller,
    this.buttonColor,
    required this.height,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    useEffect(() {
      return () {
        controller.dispose();
      };
    }, []);
    return SizedBox(
      height: height,
      child: Row(
        children: [
          for (int digit = 1 + row * 3; digit <= 3 + row * 3; digit++)
            if (digit <= 9)
              Expanded(
                child: GestureDetector(
                  onTap: () {
                    controller.text += digit.toString();
                  },
                  behavior: HitTestBehavior.translucent,
                  child: FractionallySizedBox(
                    widthFactor: 0.33,
                    child: NumberButton(
                      digit: digit.toString(),
                      controller: controller,
                      buttonColor: buttonColor,
                    ),
                  ),
                ),
              ),
        ],
      ),
    );
  }
}

class NumberPadLastRow extends HookWidget {
  final TextEditingController controller;
  final Color? buttonColor;
  final double height;

  const NumberPadLastRow({
    Key? key,
    required this.controller,
    this.buttonColor,
    required this.height,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      height: height,
      child: Row(
        children: [
          Expanded(
            child: FractionallySizedBox(
              widthFactor: 0.33,
              child: NumberButton(
                controller: controller,
                digit: '',
                buttonColor: buttonColor,
              ),
            ),
          ),
          Expanded(
            child: FractionallySizedBox(
              widthFactor: 0.33,
              child: NumberButton(
                digit: '0',
                controller: controller,
                buttonColor: buttonColor,
              ),
            ),
          ),
          Expanded(
            child: FractionallySizedBox(
              widthFactor: 0.33,
              child: BackspaceButton(
                controller: controller,
                color: AppColors.greyColor,
              ),
            ),
          ),
        ],
      ),
    );
  }
}
