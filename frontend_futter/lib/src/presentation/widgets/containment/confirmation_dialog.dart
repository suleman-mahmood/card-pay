import 'package:cardpay/src/config/themes/colors.dart';
import 'package:cardpay/src/presentation/widgets/boxes/height_box.dart';
import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';

class ConfirmationContainer extends HookWidget {
  final String title1;
  final String title2;
  final String text1;
  final String text2;
  const ConfirmationContainer({
    Key? key,
    required this.title1,
    required this.text1,
    required this.title2,
    required this.text2,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      home: Scaffold(
        body: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 40.0),
          child: Card(
            elevation: 8.0,
            borderOnForeground: true,
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(32.0),
            ),
            child: Padding(
              padding:
                  const EdgeInsets.symmetric(horizontal: 24.0, vertical: 16.0),
              child: SizedBox(
                width: 200,
                height: 120,
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text('Details', style: AppTypography.subHeading),
                    HeightBox(slab: 1),
                    Text(title1, style: AppTypography.subHeading),
                    Text(text1, style: AppTypography.bodyText),
                    HeightBox(slab: 1),
                    Text(title2, style: AppTypography.subHeading),
                    Text(text2, style: AppTypography.bodyText),
                  ],
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }
}
