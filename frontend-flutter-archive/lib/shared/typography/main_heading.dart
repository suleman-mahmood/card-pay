import 'package:cardpay/theme/colors.dart';
import 'package:flutter/material.dart';

class MainHeadingTypographyCustomWidget extends StatelessWidget {
  final String content;
  final bool invertColors;

  const MainHeadingTypographyCustomWidget({
    Key? key,
    required this.content,
    this.invertColors = false,
  }) : super(key: key);

  Color primaryColorDisplay() {
    return invertColors ? AppColors().secondaryColor : AppColors().blackColor;
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Text(
      content,
      textAlign: TextAlign.center,
      style: theme
          .copyWith(
            textTheme: theme.textTheme.copyWith(
              caption: theme.textTheme.headline4!.copyWith(
                color: primaryColorDisplay(),
              ),
            ),
          )
          .textTheme
          .caption,
    );
  }
}
