import 'package:cardpay/theme/colors.dart';
import 'package:flutter/material.dart';

class AuthLayout2CustomWidget extends StatelessWidget {
  final bool invertColors;
  final List<Widget> children;

  const AuthLayout2CustomWidget({
    Key? key,
    required this.children,
    this.invertColors = false,
  }) : super(key: key);

  Color showPrimaryColor() {
    return invertColors ? AppColors().primaryColor : AppColors().secondaryColor;
  }

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: Container(
        decoration: BoxDecoration(
          gradient: AppColors().dashboardCardGradient,
        ),
        child: Scaffold(
          backgroundColor: Colors.transparent,
          body: Center(
            child: SingleChildScrollView(
              child: Padding(
                padding: EdgeInsets.symmetric(horizontal: 40),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: children,
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }
}
