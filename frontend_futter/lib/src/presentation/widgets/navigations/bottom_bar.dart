import 'package:flutter/material.dart';
import 'package:curved_navigation_bar/curved_navigation_bar.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:cardpay/src/config/themes/colors.dart';
import 'package:cardpay/src/config/screen_utills/screen_util.dart';

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

    return CurvedNavigationBar(
      index: selectedIndex,
      color: AppColors.secondaryColor,
      backgroundColor: AppColors.primaryColor,
      buttonBackgroundColor: AppColors.secondaryColor,
      height: 50,
      items: iconsToUse
          .asMap()
          .entries
          .map((e) => _buildIcon(e.value, e.key))
          .toList(),
      animationDuration: animationDuration,
      animationCurve: Curves.bounceInOut,
      onTap: onItemTapped,
    );
  }

  Widget _buildIcon(IconData iconData, int index) {
    final color =
        index == selectedIndex ? AppColors.primaryColor : AppColors.greyColor;
    return Icon(iconData, color: color);
  }
}
