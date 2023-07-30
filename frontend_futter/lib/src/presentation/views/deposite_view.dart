import 'package:cardpay/src/presentation/cubits/remote/user_cubit.dart';
import 'package:cardpay/src/presentation/widgets/boxes/horizontal_padding.dart';
import 'package:cardpay/src/presentation/widgets/navigations/top_navigation.dart';
import 'package:flutter/material.dart';
import 'package:auto_route/auto_route.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:cardpay/src/config/router/app_router.dart';
import 'package:cardpay/src/config/themes/colors.dart';

import 'package:cardpay/src/presentation/widgets/layout/transaction_common_layout.dart';
import 'package:cardpay/src/utils/constants/payment_string.dart';
import 'package:url_launcher/url_launcher.dart';

class DepositViewConstants {
  static const title = PaymentStrings.depositMoney;
  static const buttonText = PaymentStrings.continu;
}

@RoutePage()
class DepositView extends HookWidget {
  const DepositView({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final userCubit = BlocProvider.of<UserCubit>(context);

    return BlocBuilder<UserCubit, UserState>(builder: (_, state) {
      switch (state.runtimeType) {
        case UserInitial:
          return TransactionView(
            title: DepositViewConstants.title,
            buttonText: DepositViewConstants.buttonText,
            backgroundColor: AppColors.mediumBlueColor,
            onButtonPressed: (amount) => {
              userCubit.createDepositRequest(amount),
            },
          );
        case UserLoading:
          return const Scaffold(
            backgroundColor: AppColors.mediumBlueColor,
            body: Column(
              children: [
                PaddingHorizontal(
                    slab: 2,
                    child: Header(
                      title: DepositViewConstants.title,
                    )),
                Center(child: CircularProgressIndicator()),
              ],
            ),
          );
        case UserSuccess:
          launchUrl(Uri.parse(state.checkoutUrl));
          return const Scaffold(
            backgroundColor: AppColors.mediumBlueColor,
            body: Column(
              children: [
                PaddingHorizontal(
                    slab: 2,
                    child: Header(
                      title: DepositViewConstants.title,
                    )),
                Center(child: CircularProgressIndicator()),
              ],
            ),
          );
        default:
          return const SizedBox.shrink();
      }
    });
  }
}
