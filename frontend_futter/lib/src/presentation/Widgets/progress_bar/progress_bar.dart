import 'package:flutter/material.dart';

class CustomProgressBar extends StatelessWidget {
  final double progress;

  const CustomProgressBar({required this.progress});

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 5,
      child: LinearProgressIndicator(
        value: progress,
        valueColor: AlwaysStoppedAnimation<Color>(Colors.blue),
        backgroundColor: Colors.grey.shade300,
      ),
    );
  }
}
