import 'package:cardpay/theme/colors.dart';
import 'package:flutter/material.dart';

class LinkTypographyCustomWidget extends StatelessWidget {
  final String content;
  final String redirectTo;
  final bool invertColors;

  const LinkTypographyCustomWidget({
    Key? key,
    required this.content,
    required this.redirectTo,
    this.invertColors = false,
  }) : super(key: key);

  Color primaryColorDisplay() {
    return invertColors ? AppColors().orangeColor : AppColors().primaryColor;
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return GestureDetector(
      onTap: () => Navigator.of(context).pushNamed(redirectTo),
      child: Text(
        content,
        style: theme
            .copyWith(
              textTheme: theme.textTheme.copyWith(
                caption: theme.textTheme.caption!.copyWith(
                  color: primaryColorDisplay(),
                ),
              ),
            )
            .textTheme
            .caption,
      ),
    );
  }
}
