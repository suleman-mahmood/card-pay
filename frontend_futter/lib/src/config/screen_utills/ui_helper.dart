import 'package:flutter/material.dart';

class UIHelpers {
  static EdgeInsets calculateMargin(BuildContext context) {
    final buttonWidth = MediaQuery.of(context).size.width;
    final buttonHeight = buttonWidth * 96 / 542;

    final marginVertical = buttonHeight * 0.03;
    final marginHorizontal = buttonWidth * 0.05;

    return EdgeInsets.fromLTRB(
        marginHorizontal, marginVertical, marginHorizontal, 0);
  }

  static EdgeInsets calculatePadding(BuildContext context) {
    final buttonWidth = MediaQuery.of(context).size.width;
    final buttonHeight = buttonWidth * 96 / 542;

    final paddingVertical = buttonHeight * 0.07;
    final paddingHorizontal = buttonWidth * 0.13;

    return EdgeInsets.symmetric(
        vertical: paddingVertical, horizontal: paddingHorizontal);
  }
}
