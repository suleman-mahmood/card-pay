import 'package:flutter/material.dart';
import 'package:frontend_futter/src/config/themes/colors.dart';

class CustomButton extends StatelessWidget {
  final String text;
  final VoidCallback onPressed;
  final double width;
  final double height;

  const CustomButton({
    required this.text,
    required this.onPressed,
    this.width = 272,
    this.height = 48,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      width: width,
      height: height,
      margin: EdgeInsets.only(
          top: 0.03 * MediaQuery.of(context).size.height,
          left: 0.05 * MediaQuery.of(context).size.width),
      child: ElevatedButton(
        onPressed: onPressed,
        child: Container(
          constraints: BoxConstraints.expand(),
          alignment: Alignment.center,
          padding: EdgeInsets.symmetric(vertical: 8, horizontal: 16),
          child: Text(
            text,
            style: TextStyle(
              fontWeight: FontWeight.bold,
              color: AppColors().secondaryColor,
            ),
          ),
        ),
        style: ButtonStyle(
          padding: MaterialStateProperty.all<EdgeInsets>(EdgeInsets.zero),
          backgroundColor:
              MaterialStateProperty.all<Color>(AppColors().primaryColor),
          shape: MaterialStateProperty.all<RoundedRectangleBorder>(
              RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(10),
          )),
        ),
      ),
    );
  }
}
