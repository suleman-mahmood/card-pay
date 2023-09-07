import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:cardpay/src/config/themes/colors.dart';

class BackspaceButton extends HookWidget {
  final TextEditingController controller;
  final Color color;

  const BackspaceButton({
    super.key,
    required this.controller,
    this.color = AppColors.secondaryColor,
  });
  @override
  Widget build(BuildContext context) {
    useEffect(() {
      return () {
        controller.dispose();
      };
    }, []);

    return GestureDetector(
      onTap: () {
        final text = controller.text;
        if (text.isNotEmpty) {
          controller.text = text.substring(0, text.length - 1);
        }
      },
      child: Container(
        alignment: Alignment.center,
        child: Transform.scale(
          scale: 1.5,
          child: Icon(
            Icons.backspace,
            color: color,
          ),
        ),
      ),
    );
  }
}
