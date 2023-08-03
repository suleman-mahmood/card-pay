import 'package:cardpay/src/config/router/app_router.dart';
import 'package:cardpay/src/presentation/widgets/actions/button/primary_button.dart';
import 'package:flutter/material.dart';
import 'package:auto_route/auto_route.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:cardpay/src/config/themes/colors.dart';
import 'package:url_launcher/url_launcher.dart';

@RoutePage()
class HelpView extends HookWidget {
  const HelpView({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    void _launchWhatsApp(String phoneNumber) async {
      String url = 'https://wa.me/$phoneNumber';

      if (await canLaunch(url)) {
        await launch(url);
      } else {
        throw 'Could not launch WhatsApp';
      }
    }

    return Scaffold(
      backgroundColor: AppColors.purpleColor,
      body: Container(
        padding: const EdgeInsets.symmetric(horizontal: 56),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            PrimaryButton(
              text: 'Contact Us',
              onPressed: () {
                _launchWhatsApp('+923114739822');
              },
            ),
          ],
        ),
      ),
    );
  }
}
