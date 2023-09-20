import 'package:cardpay/src/config/themes/colors.dart';
import 'package:cardpay/src/presentation/widgets/boxes/all_padding.dart';
import 'package:cardpay/src/presentation/widgets/boxes/height_box.dart';
import 'package:cardpay/src/utils/constants/payment_strings.dart';
import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';

class ConfirmationContainer extends HookWidget {
  final String mainHeading1;
  final String mainHeading2;
  final String subHeading1;
  final String subHeading2;

  const ConfirmationContainer({
    Key? key,
    required this.mainHeading1,
    required this.subHeading1,
    required this.mainHeading2,
    required this.subHeading2,
  }) : super(key: key);
  @override
  Widget build(BuildContext context) {
    return Align(
      alignment: Alignment.topCenter,
      child: Card(
        elevation: 2,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(32.0),
        ),
        child: SizedBox(
          width: 280,
          height: 168,
          child: PaddingAll(
            slab: 2,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(PaymentStrings.details, style: AppTypography.subHeading),
                HeightBox(slab: 1),
                Text(mainHeading1, style: AppTypography.subHeading),
                Text(subHeading1, style: AppTypography.bodyText),
                HeightBox(slab: 1),
                Text(mainHeading2, style: AppTypography.subHeading),
                Text(subHeading2, style: AppTypography.bodyText),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
