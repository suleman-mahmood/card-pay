import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class AppColors {
  static const Color secondaryColor = Colors.white;
  static const Color bluishColor = Color.fromRGBO(224, 235, 255, 1);
  static const Color primaryColor = Color.fromRGBO(6, 127, 205, 1);

  static const Color lightBlueColor = Color.fromRGBO(65, 160, 242, 1);
  static const Color darkBlueColor = Color.fromRGBO(20, 94, 185, 0.998);
  static const Color mediumBlueColor = Color.fromRGBO(6, 127, 205, 1);
  static const Color skyColor = Color.fromRGBO(1, 204, 192, 1);
  static const Color mediumGreenColor = Color.fromRGBO(1, 204, 136, 1);
  static const Color parrotColor = Color.fromRGBO(1, 204, 136, 1);

  static const Color purpleColor = Color.fromRGBO(90, 39, 200, 1);

  static const Color orangeColor = Colors.orange;
  static const Color darkOrangeColor = Color.fromRGBO(237, 117, 4, 1);

  static const Color redColor = Colors.red;
  static const Color blueColor = Color(0xFF171582);
  static const Color greyColor = Colors.grey;
  static const Color lightGreyColor = Color.fromARGB(255, 234, 233, 233);

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
  static const Gradient splashGradient = LinearGradient(
    begin: Alignment.topCenter,
    colors: [
      Color.fromARGB(255, 28, 80, 190),
      Color.fromARGB(255, 6, 73, 132),
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
  static TextStyle introHeading = TextStyle(
    fontFamily: GoogleFonts.poppins().fontFamily,
    fontSize: 48,
    fontWeight: FontWeight.bold,
  );

  static TextStyle mainHeading = TextStyle(
    fontFamily: GoogleFonts.poppins().fontFamily,
    fontSize: 28,
    fontWeight: FontWeight.bold,
  );
  static TextStyle mainHeadingWhite = TextStyle(
    fontFamily: GoogleFonts.poppins().fontFamily,
    color: AppColors.secondaryColor,
    fontSize: 28,
    fontWeight: FontWeight.bold,
  );
  static TextStyle mainHeadingGrey = TextStyle(
    fontFamily: GoogleFonts.poppins().fontFamily,
    color: AppColors.blackColor.withOpacity(0.8),
    fontSize: 40,
    fontWeight: FontWeight.bold,
  );

  static TextStyle bodyText = TextStyle(
    fontFamily: GoogleFonts.plusJakartaSans().fontFamily,
    color: AppColors.blackColor,
    fontSize: 16,
  );
  static TextStyle bodyTextBold = TextStyle(
    fontFamily: GoogleFonts.plusJakartaSans().fontFamily,
    color: AppColors.blackColor,
    fontSize: 16,
    fontWeight: FontWeight.bold,
  );

  static TextStyle linkText = TextStyle(
    fontFamily: GoogleFonts.plusJakartaSans().fontFamily,
    color: AppColors.primaryColor,
    fontWeight: FontWeight.bold,
    fontSize: 16,
  );
  static TextStyle errorText = TextStyle(
    fontFamily: GoogleFonts.plusJakartaSans().fontFamily,
    color: AppColors.darkOrangeColor,
    fontWeight: FontWeight.bold,
    fontSize: 16,
  );

  static TextStyle subHeading = TextStyle(
    fontFamily: GoogleFonts.plusJakartaSans().fontFamily,
    color: AppColors.greyColor,
    fontSize: 16,
  );
  static TextStyle subHeadingBold = TextStyle(
    fontFamily: GoogleFonts.plusJakartaSans().fontFamily,
    color: AppColors.greyColor,
    fontSize: 16,
    fontWeight: FontWeight.bold,
  );

  static TextStyle inputFont = TextStyle(
    fontFamily: GoogleFonts.plusJakartaSans().fontFamily,
    fontSize: 16,
  );

  static TextStyle headingFont = TextStyle(
    fontFamily: GoogleFonts.poppins().fontFamily,
    fontSize: 16,
    color: AppColors.secondaryColor,
    fontWeight: FontWeight.bold,
    fontStyle: FontStyle.normal,
  );
}
