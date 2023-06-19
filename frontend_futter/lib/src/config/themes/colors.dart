import 'package:flutter/material.dart';

class AppColors {
  static const Color primaryColor = Colors.blue;
  static const Color secondaryColor = Colors.white;

  static const Color orangeColor = Colors.orange;
  static const Color redColor = Colors.red;
  static const Color blueColor = Color(0xFF171582);
  static const Color greyColor = Colors.grey;

  static const Color greenColor = Colors.lightGreen;
  static const Color blackColor = Colors.black;

  static const Gradient dashboardButtonGradient = LinearGradient(
    begin: Alignment.topCenter,
    colors: [
      Color.fromARGB(255, 45, 87, 177),
      Color.fromRGBO(55, 114, 166, 1),
      Color.fromARGB(255, 37, 115, 184),
    ],
  );

  static const Gradient dashboardCardGradient = LinearGradient(
    begin: Alignment.topCenter,
    colors: [
      Color.fromRGBO(28, 66, 146, 1),
      Color.fromRGBO(55, 114, 166, 1),
      Color.fromRGBO(65, 160, 242, 1),
    ],
  );

  static const Gradient bottomNavbarGradient = LinearGradient(
    begin: Alignment.topCenter,
    colors: [
      Color.fromARGB(255, 28, 80, 190),
      Color.fromARGB(255, 42, 109, 168),
      Color.fromRGBO(65, 160, 242, 1),
    ],
  );

  static const Gradient animationHomeGradient = LinearGradient(
    begin: Alignment.topCenter,
    colors: [
      Color(0xFF067FCD),
      Color(0xFF171582),
      Color(0xFF42409F),
    ],
  );
}

class AppTypography {
  static const TextStyle mainHeading = TextStyle(
    fontFamily: 'poppins',
    fontSize: 35,
    fontWeight: FontWeight.bold,
  );

  static const TextStyle inputFont = TextStyle(
    fontFamily: 'plus jakarta sans',
    fontSize: 16,
    fontWeight: FontWeight.normal,
    fontStyle: FontStyle.normal,
  );

  static const TextStyle headingFont = TextStyle(
    fontFamily: 'poppins',
    fontSize: 16,
    fontWeight: FontWeight.bold,
    fontStyle: FontStyle.normal,
  );
}
