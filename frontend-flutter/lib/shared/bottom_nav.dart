import 'package:flutter/material.dart';
import 'package:flutter/src/foundation/key.dart';
import 'package:flutter/src/widgets/framework.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';

class BottomNavBar extends StatelessWidget {
  const BottomNavBar({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return BottomNavigationBar(
      items: const [
        BottomNavigationBarItem(
          icon: Icon(
            FontAwesomeIcons.graduationCap,
            size: 20,
          ),
          label: "Topics",
        ),
        BottomNavigationBarItem(
          icon: Icon(
            FontAwesomeIcons.bolt,
            size: 20,
          ),
          label: "About",
        ),
        BottomNavigationBarItem(
          icon: Icon(
            FontAwesomeIcons.moneyBillTransfer,
            size: 20,
          ),
          label: "Transactions",
        ),
      ],
      fixedColor: Colors.deepPurple[200],
      onTap: (int idx) {
        switch (idx) {
          case 0:
            break;
          case 1:
            Navigator.pushNamed(context, '/about');
            break;
          case 2:
            Navigator.pushNamed(context, '/transactions');
            break;
        }
      },
    );
  }
}
