import 'package:cardpay/theme/colors.dart';
import 'package:flutter/material.dart';
import 'package:flutter/src/foundation/key.dart';
import 'package:flutter/src/widgets/framework.dart';
import 'package:flutter/widgets.dart';

class AuthLayoutWidget extends StatelessWidget {
  final bool invertColors;
  final List<Widget> children;

  const AuthLayoutWidget({
    Key? key,
    required this.children,
    this.invertColors = false,
  }) : super(key: key);

  Color showPrimaryColor() {
    return invertColors ? AppColors().PrimaryColor : AppColors().SecondaryColor;
  }

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: Scaffold(
        backgroundColor: showPrimaryColor(),
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
    );
  }
}
