import 'package:cardpay/theme/colors.dart';
import 'package:flutter/material.dart';

class SubHeadingTypographyCustomWidget extends StatelessWidget {
  final String content;
  final bool invertColors;
  final TextAlign textAlign;
  final bool? isDebit;

  const SubHeadingTypographyCustomWidget({
    Key? key,
    required this.content,
    this.textAlign = TextAlign.center,
    this.invertColors = false,
    this.isDebit,
  }) : super(key: key);

  Color primaryColorDisplay() {
    return invertColors ? AppColors().secondaryColor : AppColors().blackColor;
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Text(
      content,
      textAlign: textAlign,
      style: theme
          .copyWith(
            textTheme: theme.textTheme.copyWith(
              caption: theme.textTheme.headlineSmall!.copyWith(
                fontWeight: FontWeight.bold,
                color: isDebit == null
                    ? primaryColorDisplay()
                    : (isDebit!
                        ? AppColors().redColor
                        : AppColors().greenColor),
              ),
            ),
          )
          .textTheme
          .caption,
    );
  }
}
