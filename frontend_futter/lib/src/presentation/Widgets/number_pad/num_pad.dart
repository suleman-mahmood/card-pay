import 'package:flutter/material.dart';
import 'package:frontend_futter/src/config/themes/colors.dart';

class NumberPad extends StatelessWidget {
  final TextEditingController controller;

  const NumberPad({required this.controller});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(top: 70),
      child: Column(
        children: [
          SizedBox(height: 20), // Added top padding here
          for (int row = 0; row < 4; row++)
            Padding(
              padding: const EdgeInsets.symmetric(vertical: 16.0),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: [
                  for (int digit = 1 + row * 3; digit <= 3 + row * 3; digit++)
                    NumberButton(
                      digit: digit.toString(),
                      controller: controller,
                    ),
                ],
              ),
            ),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: [
              SizedBox(width: 64),
              NumberButton(digit: '0', controller: controller),
              BackspaceButton(controller: controller),
            ],
          ),
        ],
      ),
    );
  }
}

class NumberButton extends StatelessWidget {
  final String digit;
  final TextEditingController controller;

  const NumberButton({
    required this.digit,
    required this.controller,
  });

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () {
        controller.text += digit;
      },
      child: Container(
        width: 64,
        height: 64,
        alignment: Alignment.center,
        child: Text(
          digit,
          style: AppTypography.headingFont.copyWith(
            color: AppColors.secondaryColor,
            fontSize: 24,
          ),
        ),
      ),
    );
  }
}

class BackspaceButton extends StatelessWidget {
  final TextEditingController controller;

  const BackspaceButton({required this.controller});

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () {
        final text = controller.text;
        if (text.isNotEmpty) {
          controller.text = text.substring(0, text.length - 1);
        }
      },
      child: Container(
        width: 64,
        height: 64,
        alignment: Alignment.center,
        child: Icon(Icons.backspace),
      ),
    );
  }
}
