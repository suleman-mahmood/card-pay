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

class RequestAmountViewConstants {
  static const title = 'Request Money';
  static const buttonText = 'Continue';
}

@RoutePage()
class RequestAmountView extends HookWidget {
  final String uniqueIdentifier;
  const RequestAmountView({Key? key, required this.uniqueIdentifier})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    final senderUniqueIdentifier = useState<String>(uniqueIdentifier);
    final userCubit = BlocProvider.of<UserCubit>(context);

    return BlocBuilder<UserCubit, UserState>(builder: (_, state) {
      switch (state.runtimeType) {
        case UserInitial:
          return TransactionView(
            title: PaymentStrings.requestMoney,
            buttonText: PaymentStrings.continu,
            rollNumber: senderUniqueIdentifier.value,
            backgroundColor: AppColors.purpleColor,
            onButtonPressed: (amount) => {
              userCubit.createP2PPullTransaction(
                senderUniqueIdentifier.value,
                amount,
              )
            },
          );
        case UserLoading:
          return const Scaffold(
            backgroundColor: AppColors.purpleColor,
            body: Center(child: CircularProgressIndicator()),
          );
        case UserSuccess:
          // TODO: fix this and pass data
          if (state.eventCodes == EventCodes.REQUEST_SUCCESSFUL) {
            // context.router.push(ConfirmationRoute());
          }
          return const SizedBox.shrink();
        default:
          return const SizedBox.shrink();
      }
    });
  }
}
