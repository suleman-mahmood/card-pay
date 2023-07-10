import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:frontend_futter/src/config/themes/colors.dart';

class MainHeading extends HookWidget {
  final String accountTitle;
  final String? accountDescription;

  const MainHeading({super.key, 
    required this.accountTitle,
    this.accountDescription,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          accountTitle,
          style: AppTypography.mainHeading,
        ),
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
