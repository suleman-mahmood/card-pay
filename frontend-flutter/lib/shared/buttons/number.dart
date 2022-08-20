import 'package:flutter/material.dart';
import 'package:flutter/src/foundation/key.dart';
import 'package:flutter/src/widgets/framework.dart';

class NumberButtonWidget extends StatelessWidget {
  // Configurations
  final double buttonBorderRadius = 20;

  final int number;
  final VoidCallback onPressed;

  const NumberButtonWidget({
    Key? key,
    required this.number,
    required this.onPressed,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return ElevatedButton(
      style: ButtonStyle(
        shape: MaterialStateProperty.all(
          RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(buttonBorderRadius),
          ),
        ),
      ),
      onPressed: onPressed,
      child: Text(number.toString()),
    );
  }
}
