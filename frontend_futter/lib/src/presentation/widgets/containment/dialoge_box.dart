import 'package:cardpay/src/utils/constants/signUp_string.dart';
import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:url_launcher/url_launcher.dart';
import 'dart:io';

class UpdateDialogBox extends HookWidget {
  final bool showMaybeLaterButton;

  const UpdateDialogBox({
    this.showMaybeLaterButton = true,
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    useEffect(() {
      WidgetsBinding.instance.addPostFrameCallback((_) {
        showDialog<String>(
          context: context,
          barrierDismissible: false,
          builder: (BuildContext context) => AlertDialog(
            backgroundColor: Colors.white,
            title: const Text('Update your app'),
            content: Text(Platform.isIOS
                ? AppStrings.updateMessageIOS
                : AppStrings.updateMessageAndroid),
            actions: <Widget>[
              if (showMaybeLaterButton)
                TextButton(
                  onPressed: () => Navigator.pop(context, 'Cancel'),
                  child: const Text('Maybe later'),
                ),
              TextButton(
                onPressed: () async {
                  final url = Platform.isIOS
                      ? 'https://apps.apple.com/app/1644127078'
                      : 'https://play.google.com/store/apps/details?id=io.payment.cardpay';

                  if (await launchUrl(Uri.parse(url))) {
                    await launchUrl(Uri.parse(url));
                  } else {}
                },
                child: const Text('Update Now'),
              ),
            ],
          ),
        );
      });
      return null;
    }, []);

    return const SizedBox.shrink();
  }
}
