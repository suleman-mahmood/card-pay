import 'package:cardpay/theme/colors.dart';
import 'package:flutter/material.dart';
import 'package:flutter/src/foundation/key.dart';
import 'package:flutter/src/widgets/framework.dart';
import 'package:flutter/widgets.dart';

class MainHeadingWidget extends StatelessWidget {
  final String content;
  final bool invertColors;

  const MainHeadingWidget({
    Key? key,
    required this.content,
    this.invertColors = false,
  }) : super(key: key);

  Color primaryColorDisplay() {
    return invertColors ? AppColors().SecondaryColor : AppColors().BlackColor;
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
