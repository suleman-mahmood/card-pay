import 'package:cardpay/theme/colors.dart';
import 'package:flutter/material.dart';

class TextPlaceholderInputCustomWidget extends StatelessWidget {
  final String prefixText;
  final String hintText;
  final bool invertColors;
  final void Function(String) onChanged;
  final String? Function(String?)? validator;

  const TextPlaceholderInputCustomWidget({
    Key? key,
    required this.onChanged,
    required this.prefixText,
    required this.hintText,
    this.validator,
    this.invertColors = false,
  }) : super(key: key);

  Color showPrimaryColorDisplay() {
    return invertColors ? AppColors().secondaryColor : AppColors().primaryColor;
  }

  Color showSecondaryColorDisplay() {
    return invertColors ? AppColors().primaryColor : AppColors().secondaryColor;
  }

  @override
  Widget build(BuildContext context) {
    return TextFormField(
      autovalidateMode: AutovalidateMode.onUserInteraction,
      onChanged: onChanged,
      validator: validator,
      style: TextStyle(
        color: showPrimaryColorDisplay(),
      ),
      decoration: InputDecoration(
        prefixText: "$prefixText: ",
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(30),
          borderSide: BorderSide(
            color: showPrimaryColorDisplay(),
            width: 5,
          ),
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(30),
          borderSide: BorderSide(
            color: showPrimaryColorDisplay(),
            width: 2,
          ),
        ),
        contentPadding: EdgeInsets.symmetric(horizontal: 20),
        labelText: prefixText,
        labelStyle: TextStyle(color: showPrimaryColorDisplay()),
        floatingLabelBehavior: FloatingLabelBehavior.never,
        hintStyle: TextStyle(color: showPrimaryColorDisplay()),
        hintText: hintText,
        filled: true,
        fillColor: showSecondaryColorDisplay(),
      ),
    );
  }
}
