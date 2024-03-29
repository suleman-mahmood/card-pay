import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:cardpay/src/config/themes/colors.dart';

class MainHeading extends HookWidget {
  final String? accountTitle;
  final String? accountDescription;

  const MainHeading({
    super.key,
    this.accountTitle,
    this.accountDescription,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        (accountTitle != null)
            ? Text(
                accountTitle!,
                style: AppTypography.mainHeading,
              )
            : const SizedBox.shrink(),
        (accountDescription != null)
            ? Text(
                accountDescription!,
                style: AppTypography.subHeading,
              )
            : const SizedBox.shrink()
      ],
    );
  }
}
