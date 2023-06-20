import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';

class CustomTextFormField extends HookWidget {
  final bool obscureText;
  final TextEditingController controller;
  final FormFieldValidator<String>? validator;
  final TextInputType? keyboardType;
  final String? hint;

  const CustomTextFormField({
    required this.obscureText,
    required this.controller,
    this.validator,
    this.keyboardType,
    this.hint,
  });

  @override
  Widget build(BuildContext context) {
    final textEditingController = useTextEditingController();

    useEffect(() {
      textEditingController.text = controller.text;
      return () {
        controller.text = textEditingController.text;
      };
    }, [controller]);

    return TextFormField(
      obscureText: obscureText,
      controller: textEditingController,
      validator: validator,
      keyboardType: keyboardType,
      decoration: InputDecoration(
        border: InputBorder.none,
        hintText: hint,
        isCollapsed: true,
        contentPadding: EdgeInsets.symmetric(
          vertical: 19,
          horizontal: 8,
        ),
      ),
    );
  }
}
