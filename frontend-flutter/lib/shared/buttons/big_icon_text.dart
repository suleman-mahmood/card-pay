import 'package:cardpay/theme/colors.dart';
import 'package:flutter/material.dart';

class BigIconTextButtonCustomWidget extends StatelessWidget {
  // Configurations
  final double width = 50;
  final double cardElevation = 5;
  final double marginBetween = 5;
  final double paddingCardIcon = 10;
  final double cardBorderRadius = 15;
  final Color iconColor = Colors.blue;

  final String content;
  final bool invertColors;
  final IconData icon;
  final VoidCallback onPressed;

  const BigIconTextButtonCustomWidget({
    Key? key,
    required this.content,
    required this.icon,
    required this.onPressed,
    this.invertColors = false,
  }) : super(key: key);

  Color primaryColorDisplay() {
    return invertColors ? AppColors().secondaryColor : AppColors().primaryColor;
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Column(
      children: <Widget>[
        // Card
        Card(
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(cardBorderRadius),
          ),
          elevation: cardElevation,
          child: Padding(
            padding: EdgeInsets.all(paddingCardIcon),
            child: SizedBox.square(
              dimension: width,
              child: IconButton(
                padding: const EdgeInsets.all(0),
                icon: Icon(
                  color: iconColor,
                  icon,
                  size: width,
                ),
                onPressed: onPressed,
              ),
            ),
          ),
        ),
        SizedBox(height: marginBetween),
        // Text
        SizedBox(
          width: width + paddingCardIcon,
          child: Text(
            content,
            textAlign: TextAlign.center,
            // style: Theme.of(context).textTheme.titleMedium,
            style: theme
                .copyWith(
                  textTheme: theme.textTheme.copyWith(
                    titleMedium: theme.textTheme.titleMedium!.copyWith(
                      color: primaryColorDisplay(),
                    ),
                  ),
                )
                .textTheme
                .titleMedium,
          ),
        ),
      ],
    );
  }
}
