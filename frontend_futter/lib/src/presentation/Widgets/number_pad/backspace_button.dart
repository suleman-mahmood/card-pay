import 'package:flutter/material.dart';

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
        width: 70, // Increased width
        height: 70, // Increased height
        alignment: Alignment.center,
        child: Icon(
          Icons.backspace,
          color: Colors.white, // Changed color to white
          size: 35.0, // Increased icon size
        ),
      ),
    );
  }
}
