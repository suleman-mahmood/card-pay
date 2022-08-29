import 'package:cardpay/theme/colors.dart';
import 'package:flutter/material.dart';
import 'package:flutter_launcher_icons/xml_templates.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';

class BottomNavBarCustomWidget extends StatelessWidget {
  final bool invertColors;

  const BottomNavBarCustomWidget({
    Key? key,
    this.invertColors = false,
  }) : super(key: key);

  Color showPrimaryColorDisplay() {
    return invertColors ? AppColors().secondaryColor : AppColors().primaryColor;
  }

  Color showSecondaryColorDisplay() {
    return invertColors ? AppColors().primaryColor : AppColors().secondaryColor;
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
          gradient: AppColors().bottomNavbarGradient,
          borderRadius: BorderRadius.vertical(top: Radius.circular(15)),
          boxShadow: [
            BoxShadow(
                color: Color.fromARGB(255, 117, 116, 116).withOpacity(0.5),
                spreadRadius: 4,
                blurRadius: 8,
                offset: Offset(0, -3)),
          ]),
      child: BottomNavigationBar(
        type: BottomNavigationBarType.fixed,
        backgroundColor: Colors.transparent,
        fixedColor: Colors.white,
        unselectedItemColor: Colors.white,
        items: [
          BottomNavigationBarItem(
            icon: Icon(
              FontAwesomeIcons.house,
              size: 20,
              color: showSecondaryColorDisplay(),
            ),
            label: "Dashboard",
          ),
          BottomNavigationBarItem(
            icon: Icon(
              FontAwesomeIcons.rightLeft,
              size: 20,
              color: showSecondaryColorDisplay(),
            ),
            label: "Transfer",
          ),
          BottomNavigationBarItem(
            icon: Icon(
              FontAwesomeIcons.clockRotateLeft,
              size: 20,
              color: showSecondaryColorDisplay(),
            ),
            label: "Transactions",
          ),
          BottomNavigationBarItem(
            icon: Icon(
              FontAwesomeIcons.circleUser,
              size: 20,
              color: showSecondaryColorDisplay(),
            ),
            label: "Profile",
          ),
        ],
        onTap: (int idx) {
          switch (idx) {
            case 0:
              Navigator.pushNamed(context, '/dashboard');
              break;
            case 1:
              Navigator.pushNamed(context, '/transfer');
              break;
            case 2:
              Navigator.pushNamed(context, '/transactions');
              break;
            // TODO: Fix this route to profile
            case 3:
              Navigator.pushNamed(context, '/profile');
              break;
          }
        },
      ),
    );
  }
}
