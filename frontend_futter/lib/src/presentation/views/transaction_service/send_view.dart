import 'package:cardpay/src/presentation/cubits/remote/transfer_cubit.dart';
import 'package:cardpay/src/presentation/cubits/remote/user_cubit.dart';
import 'package:cardpay/src/presentation/widgets/loadings/overlay_loading.dart';
import 'package:cardpay/src/utils/constants/payment_string.dart';
import 'package:flutter/material.dart';
import 'package:auto_route/auto_route.dart';
import 'package:cardpay/src/config/themes/colors.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:cardpay/src/presentation/widgets/layout/transaction_common_layout.dart';

class SendViewConstants {
  static const title = PaymentStrings.sendMoney;
  static const buttonText = PaymentStrings.carry;
}

@RoutePage()
class SendView extends HookWidget {
  final String? uniqueIdentifier;
  final String? qrId;
  final int? v;

  const SendView({
    Key? key,
    this.uniqueIdentifier,
    this.qrId,
    this.v,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final transferCubit = BlocProvider.of<TransferCubit>(context);
    final userCubit = BlocProvider.of<UserCubit>(context);

    return Stack(
      children: [
        TransactionView(
          title: PaymentStrings.transferMoney,
          buttonText: PaymentStrings.continu,
          rollNumber: uniqueIdentifier,
          backgroundColor: AppColors.parrotColor,
          onButtonPressed: (amount) {
            if (uniqueIdentifier == null) {
              return;
            }

            if (qrId == null) {
              transferCubit.executeP2PPushTransaction(
                uniqueIdentifier!,
                amount,
                userCubit.state.user.closedLoops[0].closedLoopId,
              );
            } else {
              transferCubit.executeQrTransaction(
                qrId ?? '',
                amount,
                v ?? 0,
              );
            }
          },
        ),
        BlocBuilder<TransferCubit, TransferState>(builder: (_, state) {
          switch (state.runtimeType) {
            case TransferLoading:
              return const OverlayLoading();
            default:
              return const SizedBox.shrink();
          }
        }),
      ],
    );
  }
}
