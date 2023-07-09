import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:frontend_futter/src/config/themes/colors.dart';

class MainHeading extends HookWidget {
  final String accountTitle;
  final String? accountDescription;

  const MainHeading({
    required this.accountTitle,
    this.accountDescription,
  });

  @override
  Widget build(BuildContext context) {
    final screenHeight = MediaQuery.of(context).size.height;
    final screenWidth = MediaQuery.of(context).size.width;

    return Column(
      children: [
        Text(accountTitle, style: AppTypography.mainHeading),
        SizedBox(height: screenHeight * 0.01),
        (accountDescription != null)
            ? Text(
                accountDescription!,
                style: AppTypography.inputFont.copyWith(
                  color: AppColors.blackColor,
                  fontSize: screenWidth * 0.04, 
                ),
              )
            : SizedBox.shrink()
      ],
    );
  }
}
