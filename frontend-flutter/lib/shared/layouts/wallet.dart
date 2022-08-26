import 'package:cardpay/shared/shared.dart';
import 'package:cardpay/theme/colors.dart';
import 'package:flutter/material.dart';

class WalletLayoutCustomWidget extends StatelessWidget {
  final bool invertColors;
  final List<Widget> children;

  const WalletLayoutCustomWidget({
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
      child: Scaffold(
        bottomNavigationBar: BottomNavBarCustomWidget(),
        backgroundColor: showPrimaryColor(),
        body: SingleChildScrollView(
          child: Stack(
            children: [
              Container(
                color: AppColors().primaryColor,
                height: 160,
              ),
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 40),
                child: Column(
                  children: [
                    // Top Margin
                    SizedBox(height: 50),

                    // Card area
                    StudentCardCustomWidget(),

                    // Margin
                    SizedBox(height: 30),

                    // Page content
                    Center(
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: children,
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
