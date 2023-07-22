import 'package:flutter/material.dart';
import 'package:cardpay/src/config/screen_utills/screen_util.dart';

class PaddingBoxVertical extends StatelessWidget {
  final int slab;
  final Widget child;

  const PaddingBoxVertical({Key? key, required this.slab, required this.child})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    switch (slab) {
      case 1:
        return Padding(
          padding: EdgeInsets.symmetric(vertical: ScreenUtil.paddingSlabOne),
          child: child,
        );
      case 2:
        return Padding(
          padding: EdgeInsets.symmetric(vertical: ScreenUtil.paddingSlabTwo),
          child: child,
        );
      case 3:
        return Padding(
          padding: EdgeInsets.symmetric(vertical: ScreenUtil.paddingSlabThree),
          child: child,
        );
      case 4:
        return Padding(
          padding: EdgeInsets.symmetric(vertical: ScreenUtil.paddingSlabFour),
          child: child,
        );
      case 5:
        return Padding(
          padding: EdgeInsets.symmetric(vertical: ScreenUtil.paddingSlabFive),
          child: child,
        );

      default:
        return Padding(
          padding: EdgeInsets.symmetric(vertical: ScreenUtil.paddingSlabOne),
          child: child,
        );
    }
  }
}
