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
    return Column(
      children: [
        Text(accountTitle, style: AppTypography.mainHeading),
        SizedBox(height: 10),
        (accountDescription != null)
            ? Text(
                accountDescription!,
                style: AppTypography.inputFont.copyWith(
                  color: AppColors.blackColor,
                  fontSize: 16,
                ),
              )
            : SizedBox.shrink()
      ],
    );
  }
}
