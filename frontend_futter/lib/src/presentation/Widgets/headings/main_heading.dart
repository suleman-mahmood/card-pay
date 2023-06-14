import 'package:flutter/material.dart';
import 'package:frontend_futter/src/config/themes/colors.dart';

class MainHeading extends StatelessWidget {
  final String accountTitle;
  final String? accountDescription; // Updated: Made accountDescription optional

  const MainHeading({
    required this.accountTitle,
    this.accountDescription, // Updated: Made accountDescription optional
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Text(accountTitle, style: AppColors().mainHeading),
        SizedBox(height: 10),
        if (accountDescription !=
            null) // Added condition to display accountDescription only if it's not null
          Text(
            accountDescription!,
            style: AppColors().inputFont.copyWith(
                  color: AppColors().blackColor,
                  fontSize: 16,
                ),
          ),
      ],
    );
  }
}
