import 'package:flutter/material.dart';
import 'package:cardpay/src/config/screen_utills/screen_util.dart';

class PaddingHorizontal extends StatelessWidget {
  final int slab;
  final Widget child; // Add this line

  const PaddingHorizontal({Key? key, required this.slab, required this.child})
      : super(key: key); // Update this line

  @override
  Widget build(BuildContext context) {
    switch (slab) {
      case 1:
        return Padding(
          padding: EdgeInsets.symmetric(horizontal: ScreenUtil.paddingSlabOne),
          child: child, // Add this line
        );
      case 2:
        return Padding(
          padding: EdgeInsets.symmetric(horizontal: ScreenUtil.paddingSlabTwo),
          child: child, // Add this line
        );
      case 3:
        return Padding(
          padding:
              EdgeInsets.symmetric(horizontal: ScreenUtil.paddingSlabThree),
          child: child, // Add this line
        );
      case 4:
        return Padding(
          padding: EdgeInsets.symmetric(horizontal: ScreenUtil.paddingSlabFour),
          child: child, // Add this line
        );
      case 5:
        return Padding(
          padding: EdgeInsets.symmetric(horizontal: ScreenUtil.paddingSlabFive),
          child: child,
        );
      case 6:
        return Padding(
          padding: EdgeInsets.symmetric(horizontal: ScreenUtil.paddingSlabSix),
          child: child,
        );

      default:
        return Padding(
          padding: EdgeInsets.symmetric(horizontal: ScreenUtil.paddingSlabOne),
          child: child,
        );
    }
  }
}
