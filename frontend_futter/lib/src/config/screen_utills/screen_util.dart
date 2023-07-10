import 'package:flutter/widgets.dart';

// TODO: Keep it simple
class ScreenUtil {
  static double heightSlabOne = 8;
  static double heightSlabTwo = 16;
  static double heightSlabThree = 24;

  static double widthTextBetween = 8;

  static double screenWidth(BuildContext context) {
    return MediaQuery.of(context).size.width;
  }

  static double screenHeight(BuildContext context) {
    return MediaQuery.of(context).size.height;
  }

  static double blockSizeHorizontal(BuildContext context) {
    return screenWidth(context) / 100;
  }

  static double blockSizeVertical(BuildContext context) {
    return screenHeight(context) / 100;
  }

  static double textMultiplier(BuildContext context) {
    return blockSizeVertical(context);
  }

  static double imageSizeMultiplier(BuildContext context) {
    return blockSizeHorizontal(context);
  }

  static double heightMultiplier(BuildContext context) {
    return blockSizeVertical(context);
  }

  static double widthMultiplier(BuildContext context) {
    return blockSizeHorizontal(context);
  }
}
