import 'package:animated_bottom_navigation_bar/animated_bottom_navigation_bar.dart';
import 'package:cardpay/src/config/themes/colors.dart';
import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';

class AnimatedBottomBar extends HookWidget {
  final ValueNotifier<int> selectedIndex;

  AnimatedBottomBar({required this.selectedIndex});

  @override
  Widget build(BuildContext context) {
    final iconList = [
      Icons.home,
      Icons.compare_arrows,
      Icons.bar_chart,
      Icons.person_outlined,
    ];

    // final labelsList = ["Home", "History", "Stats", "Profile"];

    return Container(
      color: Colors.white,
      child: AnimatedBottomNavigationBar(
        icons: iconList,
        activeIndex: selectedIndex.value,
        gapLocation: GapLocation.center,
        notchSmoothness: NotchSmoothness.smoothEdge,
        notchMargin: 0,
        leftCornerRadius: 8,
        rightCornerRadius: 8,
        iconSize: 32,
        height: 56,
        activeColor: AppColors.primaryColor,
        inactiveColor: AppColors.greyColor,
        onTap: (index) {
          selectedIndex.value = index;
        },
      ),
    );
  }
}
