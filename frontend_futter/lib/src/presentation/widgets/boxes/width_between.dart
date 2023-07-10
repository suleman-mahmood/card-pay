import 'package:flutter/material.dart';
import 'package:frontend_futter/src/config/screen_utills/screen_util.dart';

class WidthBetween extends StatelessWidget {
  const WidthBetween({super.key});

  @override
  Widget build(BuildContext context) {
    return SizedBox(width: ScreenUtil.widthTextBetween);
  }
}
