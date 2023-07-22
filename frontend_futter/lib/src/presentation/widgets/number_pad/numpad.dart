import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:cardpay/src/presentation/widgets/actions/button/numpad_buttons.dart';

class NumpadWithDisplay extends HookWidget {
  final Widget display;
  final TextEditingController controller;
  const NumpadWithDisplay(
      {super.key, required this.display, required this.controller});
  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        display,
        NumPad(controller: controller),
      ],
    );
  }
}
