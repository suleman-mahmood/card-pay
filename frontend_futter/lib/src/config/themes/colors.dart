import 'package:flutter/material.dart';

class AppColors {
  final Color primaryColor = Colors.blue;
  final Color secondaryColor = Colors.white;

  final Color orangeColor = Colors.orange[300]!;
  final Color redColor = Colors.red;
  final Color blueColor = Color(0xFF171582);
  final Color greyColor = Colors.grey[300]!;
  // final Color greyColor = Color.fromARGB(235, 235, 235, 209);

  final Color greenColor = Colors.lightGreen[300]!;
  final Color blackColor = Colors.black;
  // final Color greyColor = Color.fromARGB(255, 188, 192, 209);

  final Gradient dashboardButtonGradient = const LinearGradient(
    begin: Alignment.topCenter,
    colors: [
      Color.fromARGB(255, 45, 87, 177),
      Color.fromRGBO(55, 114, 166, 1),
      Color.fromARGB(255, 37, 115, 184),
    ],
  );
  final Gradient dashboardCardGradient = const LinearGradient(
    begin: Alignment.topCenter,
    colors: [
      Color.fromRGBO(28, 66, 146, 1),
      Color.fromRGBO(55, 114, 166, 1),
      Color.fromRGBO(65, 160, 242, 1),
    ],
  );
  final Gradient bottomNavbarGradient = const LinearGradient(
    begin: Alignment.topCenter,
    colors: [
      Color.fromARGB(255, 28, 80, 190),
      Color.fromARGB(255, 42, 109, 168),
      Color.fromRGBO(65, 160, 242, 1),
    ],
  );
  final Gradient animationHomeGradient = const LinearGradient(
    begin: Alignment.topCenter,
    colors: [
      Color(0xFF067FCD),
      Color(0xFF171582),
      Color(0xFF42409F),
    ],
  );

  final TextStyle mainHeading = const TextStyle(
    fontFamily: 'poppins',
    fontSize: 35, // Replace with your desired main font size
    fontWeight: FontWeight.bold,
    // fontStyle: FontStyle.normal,
  );

  final TextStyle inputFont = const TextStyle(
    fontFamily:
        'plus jakarta sans', // Replace with your desired primary font family
    fontSize: 16, // Replace with your desired primary font size
    fontWeight:
        FontWeight.normal, // Replace with your desired primary font weight
    fontStyle: FontStyle.normal, // Replace with your desired primary font style
  );

  final TextStyle headingFont = const TextStyle(
    fontFamily: 'poppins', // Replace with your desired heading font family
    fontSize: 16, // Replace with your desired heading font size
    fontWeight:
        FontWeight.bold, // Replace with your desired heading font weight
    fontStyle: FontStyle.normal, // Replace with your desired heading font style
  );
}
