// TODO: delete this in future when adding detailed transactions
import 'package:auto_route/auto_route.dart';
import 'package:cardpay/src/config/screen_utills/box_shadow.dart';
import 'package:cardpay/src/presentation/cubits/remote/balance_cubit.dart';
import 'package:cardpay/src/presentation/widgets/boxes/all_padding.dart';
import 'package:cardpay/src/presentation/widgets/boxes/height_box.dart';
import 'package:cardpay/src/presentation/widgets/boxes/horizontal_padding.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:cardpay/src/config/themes/colors.dart';
import 'package:cardpay/src/presentation/widgets/navigations/top_navigation.dart';
import 'package:cardpay/src/presentation/widgets/containment/lists/history_list.dart';
import 'package:cardpay/src/utils/constants/payment_strings.dart';
import 'package:skeleton_loader/skeleton_loader.dart';

@RoutePage()
class TransactionsView extends HookWidget {
  const TransactionsView({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
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
                  const HeightBox(slab: 1),
                  const PaddingAll(
                    slab: 2,
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.start,
                      children: [
                        SizedBox(
                          width: 10,
                        ),
                        Text(
                          PaymentStrings.transaction,
                          style: TextStyle(
                              fontWeight: FontWeight.bold, fontSize: 24),
                        ),
                        const Spacer(),
                        Text(
                          PaymentStrings.seeAll,
                          style: TextStyle(color: AppColors.purpleColor),
                        ),
                        SizedBox(
                          width: 5,
                        ),
                      ],
                    ),
                  ),
                  Expanded(child: TransactionList()),
                ],
              ),
            ),
          ),
        ),
        BlocBuilder<BalanceCubit, BalanceState>(
          builder: (_, state) {
            switch (state.runtimeType) {
              case BalanceSuccess:
                return PaddingHorizontal(
                  slab: 1,
                  child: Header(
                    showBackButton: false,
                    title: PaymentStrings.history,
                    showMainHeading: true,
                    mainHeadingText: "Rs.${state.balance.amount.toString()}",
                  ),
                );
              default:
                return SkeletonLoader(
                  builder: PaddingHorizontal(
                    slab: 1,
                    child: Header(
                      showBackButton: false,
                      title: PaymentStrings.history,
                      showMainHeading: true,
                      mainHeadingText: "",
                    ),
                  ),
                  highlightColor: AppColors.secondaryColor,
                  direction: SkeletonDirection.ltr,
                );
            }
          },
        ),
      ],
    );
  }
}
