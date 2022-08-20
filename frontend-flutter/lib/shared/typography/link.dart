import 'package:cardpay/theme/colors.dart';
import 'package:flutter/material.dart';
import 'package:flutter/src/foundation/key.dart';
import 'package:flutter/src/widgets/framework.dart';
import 'package:flutter/widgets.dart';

class LinkWidget extends StatelessWidget {
  final String content;
  final String redirectTo;
  final bool invertColors;

  const LinkWidget({
    Key? key,
    required this.content,
    required this.redirectTo,
    this.invertColors = false,
  }) : super(key: key);

  Color primaryColorDisplay() {
    return invertColors ? AppColors().OrangeColor : AppColors().PrimaryColor;
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
