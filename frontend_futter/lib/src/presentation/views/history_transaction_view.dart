import 'package:auto_route/auto_route.dart';
import 'package:cardpay/src/config/screen_utills/box_shadow.dart';
import 'package:cardpay/src/presentation/widgets/boxes/height_box.dart';
import 'package:cardpay/src/presentation/widgets/layout/payment_layouts.dart';
import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:cardpay/src/config/themes/colors.dart';
import 'package:cardpay/src/presentation/widgets/navigations/top_navigation.dart';
import 'package:cardpay/src/presentation/widgets/containment/history_list.dart';
import 'package:cardpay/src/utils/constants/payment_string.dart';

const double _borderRadiusValue = 30.0;

List<BoxShadow> boxShadow = [
  BoxShadow(
    color: AppColors.greyColor.withOpacity(0.5),
    spreadRadius: 5,
    blurRadius: 7,
    offset: const Offset(0, 3),
  ),
];

@RoutePage()
class HistroyView extends HookWidget {
  const HistroyView({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return PaymentLayout(
      useHorizontalPadding: false,
      backgroundColor: AppColors.purpleColor,
      child: Stack(
        children: [
          Align(
            alignment: Alignment.bottomCenter,
            child: FractionallySizedBox(
              heightFactor: 3 / 4,
              child: DecoratedBox(
                decoration: CustomBoxDecoration.getDecoration(),
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    const HeightBox(slab: 3),
                    Padding(
                      padding: const EdgeInsets.all(16.0),
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          const Text(
                            PaymentStrings.transaction,
                            style: TextStyle(fontWeight: FontWeight.bold),
                          ),
                          const Text(
                            PaymentStrings.seeAll,
                            style: TextStyle(color: AppColors.purpleColor),
                          ),
                        ],
                      ),
                    ),
                    Expanded(
                      child: TransactionList(),
                    ),
                  ],
                ),
              ),
            ),
          ),
          const Header(
            title: PaymentStrings.history,
            showMainHeading: true,
            mainHeadingText: PaymentStrings.balance,
          ),
        ],
      ),
    );
  }
}
