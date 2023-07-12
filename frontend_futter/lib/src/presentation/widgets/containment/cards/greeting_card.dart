import 'package:cardpay/src/presentation/widgets/boxes/width_between.dart';
import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:cardpay/src/config/themes/colors.dart';

class GreetingRow extends HookWidget {
  final String greeting;
  final String name;
  final String? imagePath;

  const GreetingRow({
    super.key,
    required this.greeting,
    required this.name,
    this.imagePath,
  });

  @override
  Widget build(BuildContext context) {
    CircleAvatar buildCircleAvatar() {
      return CircleAvatar(
        radius: 30,
        backgroundImage: imagePath != null ? AssetImage(imagePath!) : null,
      );
    }

    Column buildColumn() {
      return Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(greeting, style: AppTypography.inputFont),
          Text(name, style: AppTypography.mainHeading)
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
