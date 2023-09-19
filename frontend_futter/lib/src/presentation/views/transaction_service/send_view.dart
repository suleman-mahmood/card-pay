import 'package:cardpay/src/presentation/cubits/remote/transfer_cubit.dart';
import 'package:cardpay/src/presentation/cubits/remote/user_cubit.dart';
import 'package:cardpay/src/presentation/cubits/remote/full_name_cubit.dart';
import 'package:cardpay/src/presentation/widgets/loadings/overlay_loading.dart';
import 'package:cardpay/src/utils/constants/payment_string.dart';
import 'package:flutter/material.dart';
import 'package:auto_route/auto_route.dart';
import 'package:cardpay/src/config/themes/colors.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:cardpay/src/presentation/widgets/layout/transaction_common_layout.dart';

@RoutePage()
class SendView extends HookWidget {
  final String? uniqueIdentifier;
  final String? qrId;
  final int? v;
  final bool? isQr;

  const SendView(
      {Key? key, this.uniqueIdentifier, this.qrId, this.v, this.isQr})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    final userNameCubit = BlocProvider.of<FullNameCubit>(context);
    final transferCubit = BlocProvider.of<TransferCubit>(context);
    final userCubit = BlocProvider.of<UserCubit>(context);
    final name = useState<String>('');

    useEffect(() {
      userNameCubit.getFullName(
        uniqueIdentifier: uniqueIdentifier!,
        closedLoopId: userCubit.state.user.closedLoops[0].closedLoopId,
      );
      return null;
    }, []);

    return Stack(
      children: [
        TransactionView(
          title: PaymentStrings.transferMoney,
          buttonText: PaymentStrings.continu,
          displayRecipient: true,
          recipientVendor: uniqueIdentifier,
          backgroundColor: AppColors.parrotColor,
          onButtonPressed: (amount) {
            if ((isQr ?? false) && uniqueIdentifier == null) {
              return;
            }

            if (isQr ?? false) {
              transferCubit.executeQrTransaction(
                qrId ?? '',
                amount,
                v ?? 0,
              );
            } else {
              transferCubit.executeP2PPushTransaction(
                uniqueIdentifier!,
                amount,
                userCubit.state.user.closedLoops[0].closedLoopId,
              );
            }
          },
        ),
        BlocListener<FullNameCubit, FullNameState>(
          listener: (_, state) {
            switch (state.runtimeType) {
              case FullNameSuccess:
                name.value = state.fullName.toString();
              case FullNameFailed:
                name.value = 'User Not Found';
            }
          },
          child: const SizedBox.shrink(),
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
