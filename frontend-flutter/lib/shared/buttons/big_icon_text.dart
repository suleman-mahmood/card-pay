import 'package:flutter/material.dart';

class BigIconTextButtonWidget extends StatelessWidget {
  // Configurations
  final double width = 75;
  final double cardElevation = 5;
  final double marginBetween = 5;
  final double paddingCardIcon = 10;
  final double cardBorderRadius = 15;
  final Color iconColor = Colors.blue;

  final String content;
  final IconData icon;
  final VoidCallback onPressed;

  const BigIconTextButtonWidget({
    Key? key,
    required this.content,
    required this.icon,
    required this.onPressed,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
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
            style: Theme.of(context).textTheme.titleMedium,
          ),
        ),
      ],
    );
  }
}
