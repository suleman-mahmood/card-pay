import 'package:auto_route/auto_route.dart';
import 'package:cardpay/src/config/themes/colors.dart';
import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';

class BottomBar extends HookWidget {
  final ValueNotifier<int> selectedIndex;
  final List<PageRouteInfo> pages;

  BottomBar({required this.selectedIndex, required this.pages});

  @override
  Widget build(BuildContext context) {
    return Stack(
      clipBehavior: Clip.none,
      alignment: Alignment.bottomCenter,
      children: [
        Container(
          child: BottomNavigationBar(
            type: BottomNavigationBarType.fixed,
            backgroundColor: AppColors.secondaryColor,
            selectedItemColor: AppColors.primaryColor,
            unselectedItemColor: AppColors.greyColor,
            currentIndex: selectedIndex.value,
            onTap: (index) {
              selectedIndex.value = index;
              context.router.push(pages[index]);
            },
            items: [
              BottomNavigationBarItem(
                icon: Icon(Icons.home),
                label: 'Home',
              ),
              BottomNavigationBarItem(
                icon: Icon(Icons.history),
                label: 'History',
              ),
              BottomNavigationBarItem(
                icon: Icon(Icons.show_chart),
                label: 'Chart',
              ),
              BottomNavigationBarItem(
                icon: Icon(Icons.person),
                label: 'Profile',
              ),
            ],
          ),
        ),
        Positioned(
          bottom: 25,
          child: FloatingActionButton(
            child: Image.asset(
              'assets/images/tickbox.png',
              height: 60,
              width: 60,
            ),
            onPressed: () {},
            backgroundColor: AppColors.secondaryColor,
          ),
        ),
      ],
    );
  }
}
