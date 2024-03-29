import 'package:flutter/material.dart';

class AppColors {
  final Color primaryColor = Colors.blue;
  final Color secondaryColor = Colors.white;

  final Color orangeColor = Colors.orange[300]!;
  final Color redColor = Colors.red;
  final Color greenColor = Colors.lightGreen[300]!;
  final Color blackColor = Colors.black;
  final Color greyColor = Color.fromARGB(255, 188, 192, 209);

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
}
