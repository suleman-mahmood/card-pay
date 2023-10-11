import 'package:flutter/widgets.dart';

// TODO: Keep it simple
class ScreenUtil {
  static double heightSlabOne = 8;
  static double heightSlabTwo = 16;
  static double heightSlabThree = 24;
  static double heightSlabFour = 32;
  static double heightSlabFive = 48;
  static double heightSlabSix = 64;
  static double heightSlabSeven = 96;

  static double paddingSlabOne = 8;
  static double paddingSlabTwo = 16;
  static double paddingSlabThree = 24;
  static double paddingSlabFour = 32;
  static double paddingSlabFive = 40;
  static double paddingSlabSix = 48;

  static double widthTextBetween = 8;
  static double widthArrowBetween = 24;

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
