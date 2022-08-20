import 'package:flutter/material.dart';

class TextPlaceholderInputWidget extends StatelessWidget {
  final String prefixText;
  final String hintText;
  final void Function(String) onChanged;
  final String? Function(String?)? validator;

  const TextPlaceholderInputWidget({
    Key? key,
    required this.onChanged,
    required this.prefixText,
    required this.hintText,
    this.validator,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return TextFormField(
      autovalidateMode: AutovalidateMode.onUserInteraction,
      onChanged: onChanged,
      validator: validator,
      decoration: InputDecoration(
        prefixText: "$prefixText: ",
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(30),
          borderSide: BorderSide(
            color: Colors.blue,
            width: 5,
          ),
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(30),
          borderSide: BorderSide(
            color: Colors.blue,
            width: 2,
          ),
        ),
        contentPadding: EdgeInsets.symmetric(horizontal: 20),
        labelText: prefixText,
        labelStyle: TextStyle(color: Colors.blue),
        floatingLabelBehavior: FloatingLabelBehavior.never,
        hintStyle: TextStyle(color: Colors.blue[800]),
        hintText: hintText,
        filled: true,
        fillColor: Colors.white,
      ),
    );
  }
}
