import 'package:cardpay/services/auth.dart';
import 'package:cardpay/shared/shared.dart';
import 'package:flutter/material.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';

class DashboardScreen extends StatelessWidget {
  const DashboardScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return WalletLayoutCustomWidget(
      children: [
        GridView.count(
          crossAxisCount: 2,
          shrinkWrap: true,
          childAspectRatio: 1.3,
          children: [
            BigIconTextButtonCustomWidget(
              content: "Deposit",
              icon: FontAwesomeIcons.arrowDown,
              onPressed: () => {
                Navigator.pushNamed(context, "/deposit"),
              },
            ),
            BigIconTextButtonCustomWidget(
              content: "Logout",
              icon: FontAwesomeIcons.arrowRightFromBracket,
              onPressed: () async {
                await AuthService().signOut();
                Navigator.pushNamedAndRemoveUntil(
                  context,
                  '/',
                  (route) => false,
                );
              },
            ),
            // TODO: Uncomment later when implemented
            // BigIconTextButtonCustomWidget(
            //   content: "Analysis",
            //   icon: Icons.analytics,
            //   onPressed: () => {
            //     Navigator.pushNamed(context, "/analysis"),
            //   },
            // ),
            // BigIconTextButtonCustomWidget(
            //   content: "Budget",
            //   icon: Icons.calculate_outlined,
            //   onPressed: () => {
            //     Navigator.pushNamed(context, "/analysis"),
            //   },
            // ),
          ],
        ),
        DashboardCardCustomWidget(),
        SizedBox(height: 20),
      ],
    );
  }
}
