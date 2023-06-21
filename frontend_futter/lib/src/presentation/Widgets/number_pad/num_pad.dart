import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:frontend_futter/src/presentation/Widgets/number_pad/backspace_button.dart';
import 'package:frontend_futter/src/presentation/Widgets/number_pad/num_button.dart';

class NumPad extends HookWidget {
  final TextEditingController controller;

  const NumPad({required this.controller});

  @override
  Widget build(BuildContext context) {
    final screenHeight = MediaQuery.of(context).size.height;

    return SizedBox(
      height: screenHeight * 0.6,
      child: Padding(
        padding: EdgeInsets.only(top: screenHeight * 0.1),
        child: Column(
          children: [
            for (int row = 0; row < 3; row++)
              Expanded(
                child: Padding(
                  padding: const EdgeInsets.symmetric(vertical: 16.0),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                    children: [
                      // Number buttons
                      for (int digit = 1 + row * 3;
                          digit <= 3 + row * 3;
                          digit++)
                        if (digit <= 9)
                          Flexible(
                            child: NumberButton(
                              digit: digit.toString(),
                              controller: controller,
                            ),
                          ),
                    ],
                  ),
                ),
              ),
            Expanded(
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: [
                  Flexible(
                    child: NumberButton(digit: '', controller: controller),
                  ),
                  Flexible(
                    child: NumberButton(digit: '0', controller: controller),
                  ),
                  Flexible(
                    child: BackspaceButton(controller: controller),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
