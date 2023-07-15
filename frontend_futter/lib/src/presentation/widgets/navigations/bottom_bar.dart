import 'package:animated_bottom_navigation_bar/animated_bottom_navigation_bar.dart';
import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:cardpay/src/config/themes/colors.dart';

class CustomCurvedBottomBar extends HookWidget {
  final int selectedIndex;
  final Function(int) onItemTapped;
  final List<IconData>? icons;
  final Duration animationDuration;

  const CustomCurvedBottomBar({
    Key? key,
    required this.selectedIndex,
    required this.onItemTapped,
    this.icons,
    this.animationDuration = const Duration(milliseconds: 200),
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final defaultIcons = [
      Icons.home,
      Icons.history,
      Icons.show_chart,
      Icons.person,
    ];

    final iconsToUse = icons ?? defaultIcons;

    return AnimatedBottomNavigationBar(
      activeIndex: selectedIndex,
      onTap: onItemTapped,
      icons: iconsToUse,
      activeColor: AppColors.primaryColor,
      inactiveColor: AppColors.greyColor,
      splashColor: AppColors.secondaryColor,
      notchAndCornersAnimation: CurvedAnimation(
        parent: useAnimationController(
          duration: animationDuration,
        ),
        curve: Curves.easeOutCubic, // Adjust the curve as needed
      ),
      notchSmoothness: NotchSmoothness.verySmoothEdge,
      leftCornerRadius: 32,
      rightCornerRadius: 32,
      gapLocation: GapLocation.center,
    );
  }
}
