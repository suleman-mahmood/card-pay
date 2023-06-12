import 'package:cardpay/theme/colors.dart';
import 'package:flutter/material.dart';
import 'package:flutter_launcher_icons/main.dart';

class PlaceholderInputCustomWidget extends StatelessWidget {
  // Configurations
  final Color primaryColor = Colors.blue;
  final Color secondaryColor = Colors.white;

  final String labelText;
  final String hintText;
  final bool obscureText;
  final bool invertColors;
  final int? maxLength;

  final void Function(String) onChanged;
  final String? Function(String?)? validator;

  const PlaceholderInputCustomWidget({
    Key? key,
    required this.labelText,
    required this.hintText,
    this.obscureText = false,
    required this.onChanged,
    this.validator,
    this.invertColors = false,
    this.maxLength,
  }) : super(key: key);

  Color primaryColorDisplay() {
    return invertColors ? secondaryColor : primaryColor;
  }

  Color secondaryColorDisplay() {
    return invertColors ? primaryColor : secondaryColor;
  }

  @override
  Widget build(BuildContext context) {
    return TextFormField(
      obscureText: obscureText,
      autovalidateMode: AutovalidateMode.onUserInteraction,
      onChanged: onChanged,
      validator: validator,
      maxLength: maxLength,
      cursorColor: primaryColorDisplay(),
      style: TextStyle(
        color: primaryColorDisplay(),
      ),
      decoration: InputDecoration(
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(30),
          borderSide: BorderSide(
            color: primaryColorDisplay(),
            width: 5,
          ),
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(30),
          borderSide: BorderSide(
            color: primaryColorDisplay(),
            width: 2,
          ),
        ),
        contentPadding: EdgeInsets.symmetric(horizontal: 20),
        labelText: labelText,
        labelStyle: TextStyle(color: primaryColorDisplay()),
        hintStyle: TextStyle(color: AppColors().greyColor),
        hintText: hintText,
        filled: true,
        fillColor: secondaryColorDisplay(),
        counterText: "",
      ),
    );
  }
}
