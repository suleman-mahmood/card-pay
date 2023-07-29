import 'package:cardpay/src/presentation/cubits/remote/user_cubit.dart';
import 'package:cardpay/src/utils/constants/event_codes.dart';
import 'package:cardpay/src/utils/constants/payment_string.dart';
import 'package:flutter/material.dart';
import 'package:auto_route/auto_route.dart';
import 'package:cardpay/src/config/router/app_router.dart';
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
  final String uniqueIdentifier;
  const SendView({Key? key, required this.uniqueIdentifier}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final recipientUniqueIdentifier = useState<String>(uniqueIdentifier);
    final userCubit = BlocProvider.of<UserCubit>(context);

    return BlocBuilder<UserCubit, UserState>(builder: (_, state) {
      switch (state.runtimeType) {
        case UserLoading:
          return const Scaffold(
            backgroundColor: AppColors.parrotColor,
            body: Center(child: CircularProgressIndicator()),
          );
        case UserSuccess:
          // TODO: fix this and pass data
          if (state.eventCodes == EventCodes.TRANSFER_SUCCESSFUL) {
            context.router.push(const ConfirmationRoute());
          }
          return const SizedBox.shrink();
        default:
          return TransactionView(
            title: PaymentStrings.transferMoney,
            buttonText: PaymentStrings.continu,
            rollNumber: recipientUniqueIdentifier.value,
            backgroundColor: AppColors.parrotColor,
            onButtonPressed: (amount) => {
              userCubit.executeP2PPushTransaction(
                recipientUniqueIdentifier.value,
                amount,
              )
            },
          );
      }
    });
  }
}
