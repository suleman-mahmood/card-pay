import 'package:flutter/material.dart';
import 'package:cardpay/src/config/screen_utills/screen_util.dart';

class HeightBox extends StatelessWidget {
  final int slab;

  const HeightBox({super.key, required this.slab});

  @override
  Widget build(BuildContext context) {
    switch (slab) {
      case 1:
        return SizedBox(height: ScreenUtil.heightSlabOne);
      case 2:
        return SizedBox(height: ScreenUtil.heightSlabTwo);
      case 3:
        return SizedBox(height: ScreenUtil.heightSlabThree);
      case 4:
        return SizedBox(height: ScreenUtil.heightSlabFour);
      case 5:
        return SizedBox(height: ScreenUtil.heightSlabFive);
      case 6:
        return SizedBox(height: ScreenUtil.heightSlabSix);
      case 7:
        return SizedBox(height: ScreenUtil.heightSlabSeven);

      default:
        return SizedBox(height: ScreenUtil.heightSlabOne);
    }
  }
}
