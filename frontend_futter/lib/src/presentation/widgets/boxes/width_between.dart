import 'package:flutter/material.dart';
import 'package:cardpay/src/config/screen_utills/screen_util.dart';

class WidthBetween extends StatelessWidget {
  const WidthBetween({Key? key});

  @override
  Widget build(BuildContext context) {
    return SizedBox(width: ScreenUtil.widthTextBetween);
  }
}

class WidthArrowBetween extends StatelessWidget {
  const WidthArrowBetween({Key? key});

  @override
  Widget build(BuildContext context) {
    return SizedBox(width: ScreenUtil.widthArrowBetween);
  }
}
