import 'package:flutter/material.dart';

class BackspaceButton extends StatelessWidget {
  final TextEditingController controller;

  const BackspaceButton({required this.controller});

  @override
  Widget build(BuildContext context) {
    final screenHeight = MediaQuery.of(context).size.height;
    final screenWidth = MediaQuery.of(context).size.width;

    return GestureDetector(
      onTap: () {
        final text = controller.text;
        if (text.isNotEmpty) {
          controller.text = text.substring(0, text.length - 1);
        }
      },
      child: Container(
        width: screenWidth * 0.15,
        height: screenHeight * 0.1,
        alignment: Alignment.center,
        child: Icon(
          Icons.backspace,
          color: Colors.white,
          size: screenHeight * 0.04,
        ),
      ),
    );
  }
}
