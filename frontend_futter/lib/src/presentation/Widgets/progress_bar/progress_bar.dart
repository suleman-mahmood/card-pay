import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';

class CustomProgressBar extends HookWidget {
  final double progress;

  const CustomProgressBar({required this.progress});

  @override
  Widget build(BuildContext context) {
    final valueColor =
        useMemoized(() => AlwaysStoppedAnimation<Color>(Colors.blue));

    return Container(
      height: 5,
      child: LinearProgressIndicator(
        value: progress,
        valueColor: valueColor,
        backgroundColor: Colors.grey.shade300,
      ),
    );
  }
}
