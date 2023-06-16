import 'package:flutter/material.dart';

class CustomTextFormField extends StatelessWidget {
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
    return TextFormField(
      obscureText: obscureText,
      controller: controller,
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
