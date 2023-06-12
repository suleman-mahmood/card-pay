import 'package:cardpay/shared/shared.dart';
import 'package:flutter/material.dart';

class ProfileScreen extends StatelessWidget {
  const ProfileScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return const WalletLayoutCustomWidget(
      children: [
        MainHeadingTypographyCustomWidget(
          content: "Profile feature coming soon.\n Stay tuned!!!",
        ),
      ],
    );
  }
}
