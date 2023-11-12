import 'package:cardpay/src/presentation/cubits/local/local_balance_cubit.dart';
import 'package:cardpay/src/presentation/cubits/remote/balance_cubit.dart';
import 'package:cardpay/src/presentation/widgets/boxes/all_padding.dart';
import 'package:cardpay/src/utils/constants/payment_strings.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:cardpay/src/config/themes/colors.dart';
import 'package:skeleton_loader/skeleton_loader.dart';

class BalanceCard extends HookWidget {
  const BalanceCard({
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    final localBalanceCubit = BlocProvider.of<LocalBalanceCubit>(context);

    String topRightImage = 'assets/images/balance_corner.png';
    String bottomLeftImage = 'assets/images/balance_corner2.png';
    final deviceHeight = MediaQuery.of(context).size.height;

    String formatBalance(String amount) {
      return 'Rs. $amount';
    }

    Widget _balanceContent(String balance) {
      return Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(PaymentStrings.totalBalance, style: AppTypography.subHeading),
          Text(formatBalance(balance), style: AppTypography.mainHeadingWhite),
        ],
      );
    }

    return Card(
      color: AppColors.purpleColor,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(10),
      ),
      child: ConstrainedBox(
        constraints: BoxConstraints(
          minHeight: deviceHeight > 900
              ? deviceHeight * 0.19
              : deviceHeight > 750
                  ? deviceHeight * 0.16
                  : deviceHeight * 0.19,
          minWidth: double.infinity,
        ),
        child: Stack(
          children: [
            PaddingAll(
              slab: 2,
              child: BlocBuilder<BalanceCubit, BalanceState>(
                builder: (_, state) {
                  switch (state.runtimeType) {
                    case BalanceSuccess:
                      localBalanceCubit.updateBalance(state.balance.amount);
                      return _balanceContent(state.balance.amount.toString());
                    case BalanceLoading:
                      return BlocBuilder<LocalBalanceCubit, LocalBalanceState>(
                        builder: (_, state) {
                          switch (state.runtimeType) {
                            case LocalBalanceSuccess:
                              return SizedBox(
                                height: 60,
                                width: 200,
                                child: SkeletonLoader(
                                  builder: _balanceContent(
                                    state.balance.amount.toString(),
                                  ),
                                  items: 1,
                                  period: const Duration(seconds: 2),
                                  highlightColor: AppColors.greyColor,
                                  direction: SkeletonDirection.ltr,
                                ),
                              );
                            default:
                              return const SizedBox.shrink();
                          }
                        },
                      );
                    default:
                      return const SizedBox.shrink();
                  }
                },
              ),
            ),
            Positioned(
              top: 0,
              right: 0,
              child: ClipRRect(
                borderRadius: const BorderRadius.only(
                  topRight:
                      Radius.circular(10.0), // Adjust the radius as needed
                ),
                child: Image.asset(
                  topRightImage,
                ),
              ),
            ),
            Positioned(
              bottom: 0,
              left: 0,
              child: ClipRRect(
                borderRadius: const BorderRadius.only(
                  bottomLeft:
                      Radius.circular(10.0), // Adjust the radius as needed
                ),
                child: Image.asset(
                  bottomLeftImage,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
