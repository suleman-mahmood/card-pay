import 'package:flutter/material.dart';
import 'package:frontend_futter/src/config/themes/colors.dart';

class MainHeading extends StatelessWidget {
  final String accountTitle;
  final String accountDescription;

  const MainHeading({
    required this.accountTitle,
    required this.accountDescription,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Text(accountTitle, style: AppColors().headingFont),
        SizedBox(height: 10),
        Text(
          accountDescription,
          style: AppColors().inputFont.copyWith(
                color: AppColors().greyColor,
                fontSize: 16,
              ),
        ),
      ],
    );
  }
}
