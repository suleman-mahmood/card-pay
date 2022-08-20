import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

var appTheme = ThemeData();

var appThemeOld = ThemeData(
  fontFamily: GoogleFonts.nunito().fontFamily,
  bottomAppBarTheme: const BottomAppBarTheme(
    color: Colors.black87,
  ),
  brightness: Brightness.dark,
  textTheme: const TextTheme(
    bodyText1: TextStyle(
      fontSize: 16,
      color: Colors.black,
    ),
    bodyText2: TextStyle(
      fontSize: 16,
      color: Colors.yellow,
    ),
    button: TextStyle(
      letterSpacing: 1.5,
      fontWeight: FontWeight.bold,
      fontSize: 18,
    ),
    headline1: TextStyle(
      fontWeight: FontWeight.bold,
    ),
    headline5: TextStyle(
      fontSize: 20,
      fontWeight: FontWeight.bold,
      color: Colors.yellow,
    ),
    headline6: TextStyle(
      fontSize: 20,
      fontWeight: FontWeight.bold,
      color: Colors.black,
    ),
    subtitle1: TextStyle(
      color: Colors.grey,
    ),
  ),
  buttonTheme: const ButtonThemeData(),
);
