import 'package:auto_route/auto_route.dart';
import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:frontend_futter/src/config/themes/colors.dart';
import 'package:frontend_futter/src/presentation/widgets/navigations/top_navigation.dart';
import 'package:frontend_futter/src/presentation/widgets/containment/history_list.dart';
import 'package:frontend_futter/src/utils/constants/payment_string.dart';

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
    final decoration = useMemoized(
      () => _getBoxDecoration(),
      [],
    );

    return Scaffold(
      backgroundColor: AppColors.purpleColor,
      body: Stack(
        children: [
          Align(
            alignment: Alignment.bottomCenter,
            child: Container(
              child: SingleChildScrollView(
                child: ConstrainedBox(
                  constraints: BoxConstraints(
                    maxHeight: MediaQuery.of(context).size.height * 0.75,
                  ),
                  child: DecoratedBox(
                    decoration: decoration,
                    child: Column(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        SizedBox(
                            height: MediaQuery.of(context).size.height * 0.01),
                        _buildRow(
                          context,
                          const Text(
                            PaymentStrings.transaction,
                            style: TextStyle(fontWeight: FontWeight.bold),
                          ),
                          const Text(
                            PaymentStrings.seeAll,
                            style: TextStyle(color: AppColors.purpleColor),
                          ),
                        ),
                        Expanded(
                          child: TransactionList(),
                        ),
                        SizedBox(
                            height: MediaQuery.of(context).size.height * 0.02),
                      ],
                    ),
                  ),
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

  Row _buildRow(BuildContext context, Widget leftWidget, Widget rightWidget) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        _buildPadding(context, leftWidget),
        _buildPadding(context, rightWidget),
      ],
    );
  }

  Padding _buildPadding(BuildContext context, Widget child) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 16.0),
      child: child,
    );
  }

  BoxDecoration _getBoxDecoration() {
    return BoxDecoration(
      color: AppColors.secondaryColor,
      borderRadius: const BorderRadius.only(
        topLeft: Radius.circular(_borderRadiusValue),
        topRight: Radius.circular(_borderRadiusValue),
      ),
      boxShadow: boxShadow,
    );
  }
}
