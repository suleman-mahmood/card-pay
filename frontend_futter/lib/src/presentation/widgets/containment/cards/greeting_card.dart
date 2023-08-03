import 'package:cardpay/src/presentation/widgets/boxes/width_between.dart';
import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:cardpay/src/config/themes/colors.dart';

class GreetingRow extends HookWidget {
  final String? greeting;
  final String name;
  final String? imagePath;
  final Color? textColor;
  final int? radius;

  const GreetingRow({
    super.key,
    this.greeting,
    required this.name,
    this.imagePath,
    this.radius,
    this.textColor,
  });

  @override
  Widget build(BuildContext context) {
    CircleAvatar buildCircleAvatar() {
      return CircleAvatar(
        // radius: 30,
        radius: radius != null ? radius!.toDouble() : 30,
        backgroundImage: imagePath != null ? AssetImage(imagePath!) : null,
      );
    }

    Column buildColumn() {
      return Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          if (greeting != null && greeting!.isNotEmpty)
            Text(greeting!, style: AppTypography.inputFont),
          Text(name,
              style: AppTypography.mainHeading.copyWith(color: textColor)),
        ],
      );
    }

    return Row(
      children: [
        buildCircleAvatar(),
        WidthBetween(),
        buildColumn(),
      ],
    );
  }
}
