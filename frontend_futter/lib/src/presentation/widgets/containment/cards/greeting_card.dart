import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:cardpay/src/config/screen_utills/screen_util.dart';
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
    return Row(
      children: [
        buildCircleAvatar(context),
        buildSizedBox(context),
        buildColumn(context),
      ],
    );
  }

  CircleAvatar buildCircleAvatar(BuildContext context) {
    return CircleAvatar(
      radius: ScreenUtil.imageSizeMultiplier(context) * 7,
      backgroundImage: imagePath != null ? AssetImage(imagePath!) : null,
    );
  }

  SizedBox buildSizedBox(BuildContext context) {
    return SizedBox(
      width: ScreenUtil.widthMultiplier(context) * 3, // 3% of screen width
    );
  }

  Column buildColumn(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        buildGreetingText(context),
        buildNameText(context),
      ],
    );
  }

  Text buildGreetingText(BuildContext context) {
    return Text(
      greeting,
      style: AppTypography.headingFont.copyWith(
        fontSize: ScreenUtil.textMultiplier(context) * 1.9,
      ),
    );
  }

  Text buildNameText(BuildContext context) {
    return Text(
      name,
      style: AppTypography.mainHeading.copyWith(
        fontSize:
            ScreenUtil.textMultiplier(context) * 3.0, // 3.5% of screen height
      ),
    );
  }
}
