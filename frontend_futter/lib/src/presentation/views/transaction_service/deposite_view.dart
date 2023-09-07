import 'package:cardpay/src/presentation/cubits/remote/deposit_cubit.dart';
import 'package:cardpay/src/presentation/widgets/loadings/overlay_loading.dart';
import 'package:flutter/material.dart';
import 'package:auto_route/auto_route.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:cardpay/src/config/themes/colors.dart';
import 'package:cardpay/src/presentation/widgets/layout/transaction_common_layout.dart';
import 'package:cardpay/src/utils/constants/payment_string.dart';

class DepositViewConstants {
  static const title = PaymentStrings.depositMoney;
  static const buttonText = PaymentStrings.continu;
}

@RoutePage()
class DepositView extends HookWidget {
  const DepositView({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final depositCubit = BlocProvider.of<DepositCubit>(context);

    return Stack(
      children: [
        TransactionView(
          title: DepositViewConstants.title,
          buttonText: DepositViewConstants.buttonText,
          backgroundColor: AppColors.mediumBlueColor,
          onButtonPressed: (amount) => {
            depositCubit.createDepositRequest(amount),
          },
        ),
        BlocBuilder<DepositCubit, DepositState>(builder: (_, state) {
          switch (state.runtimeType) {
            case DepositLoading:
              return const OverlayLoading();
            default:
              return const SizedBox.shrink();
          }
        }),
      ],
    );
  }
}
