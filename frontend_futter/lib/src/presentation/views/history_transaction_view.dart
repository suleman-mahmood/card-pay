import 'package:auto_route/auto_route.dart';
import 'package:cardpay/src/config/screen_utills/box_shadow.dart';
import 'package:cardpay/src/presentation/widgets/boxes/all_padding.dart';
import 'package:cardpay/src/presentation/widgets/boxes/height_box.dart';
<<<<<<< HEAD
import 'package:cardpay/src/presentation/widgets/boxes/padding_box.dart';
import 'package:cardpay/src/presentation/widgets/layout/payment_layouts.dart';
import 'package:cardpay/src/presentation/widgets/loadings/list_histry_loadind.dart';
import 'package:cardpay/src/presentation/widgets/loadings/shimmer_loading.dart';
=======
import 'package:cardpay/src/presentation/widgets/boxes/horizontal_padding.dart';
import 'package:cardpay/src/presentation/views/payment_dashboard_view.dart';
>>>>>>> e554f655c7510d87ec59cf81541630b65a359dc0
import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:cardpay/src/config/themes/colors.dart';
import 'package:cardpay/src/presentation/widgets/navigations/top_navigation.dart';
import 'package:cardpay/src/presentation/widgets/containment/history_list.dart';
import 'package:cardpay/src/utils/constants/payment_string.dart';

const double _borderRadiusValue = 30.0;

@RoutePage()
class HistroyView extends HookWidget {
  const HistroyView({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
<<<<<<< HEAD
    // final isLoading = true;

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
                  children: [
                    const HeightBox(slab: 3),
                    PaddingAll(
                      slab: 2,
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
                    Expanded(child: TransactionList()),
                  ],
                ),
=======
    // return PaymentLayout(
    // useHorizontalPadding: false,
    // backgroundColor: AppColors.purpleColor,
    return Stack(
      children: [
        Align(
          alignment: Alignment.bottomCenter,
          child: FractionallySizedBox(
            heightFactor: 3 / 4,
            child: DecoratedBox(
              decoration: CustomBoxDecoration.getDecoration(),
              child: Column(
                children: [
                  const HeightBox(slab: 3),
                  const PaddingAll(
                    slab: 2,
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Text(
                          PaymentStrings.transaction,
                          style: TextStyle(fontWeight: FontWeight.bold),
                        ),
                        Text(
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
>>>>>>> e554f655c7510d87ec59cf81541630b65a359dc0
              ),
            ),
          ),
        ),
        const PaddingHorizontal(
          slab: 2,
          child: Header(
            title: PaymentStrings.history,
            showMainHeading: true,
            mainHeadingText: PaymentStrings.balance,
          ),
        ),
      ],
    );
  }
}
