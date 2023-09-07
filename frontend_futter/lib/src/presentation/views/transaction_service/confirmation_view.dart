import 'package:cardpay/src/config/router/app_router.dart';
import 'package:cardpay/src/presentation/cubits/remote/deposit_cubit.dart';
import 'package:cardpay/src/presentation/cubits/remote/transfer_cubit.dart';
import 'package:cardpay/src/presentation/widgets/boxes/height_box.dart';
import 'package:cardpay/src/utils/constants/signUp_string.dart';
import 'package:flutter/material.dart';
import 'package:auto_route/auto_route.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:cardpay/src/config/themes/colors.dart';
import 'package:cardpay/src/presentation/widgets/actions/button/primary_button.dart';
import 'package:cardpay/src/presentation/widgets/containment/confirmation_dialog.dart';
import 'package:cardpay/src/presentation/widgets/navigations/top_navigation.dart';
import 'package:cardpay/src/utils/constants/payment_string.dart';

@RoutePage()
class ConfirmationView extends HookWidget {
  final int amount;
  final String uniqueIdentifier;

  const ConfirmationView({
    super.key,
    required this.amount,
    required this.uniqueIdentifier,
  });

  @override
  Widget build(BuildContext context) {
    final depositCubit = BlocProvider.of<DepositCubit>(context);
    final transferCubit = BlocProvider.of<TransferCubit>(context);

    final topOfNavigationStack = ModalRoute.of(context)?.isCurrent ?? false;

    Widget buildHeader() {
      return const Header(
        title: PaymentStrings.receipt,
        color: Colors.black,
        showMainHeading: true,
      );
    }

    Widget buildSuccessImage() {
      return Image.asset('assets/images/tickbox.png');
    }

    Widget buildSuccessLabel() {
      return Text(PaymentStrings.successful,
          style: AppTypography.mainHeading.copyWith(
            color: AppColors.parrotColor,
          ));
    }

    Widget buildBalanceLabel() {
      return Text(
        amount.toString(),
        style: AppTypography.introHeading,
      );
    }

    Widget buildConfirmationContainer() {
      return Expanded(
        child: ConfirmationContainer(
          title1: PaymentStrings.send,
          text1: uniqueIdentifier,
          title2: AppStrings.date,
          text2: AppStrings.dateToday,
        ),
      );
    }

    return Scaffold(
      body: Column(
        children: [
          BlocListener<DepositCubit, DepositState>(
            listener: (_, state) {
              if (state.runtimeType == DepositSuccess && topOfNavigationStack) {
                depositCubit.init();
              }
            },
            child: const SizedBox.shrink(),
          ),
          BlocListener<TransferCubit, TransferState>(
            listener: (_, state) {
              if (state.runtimeType == TransferSuccess &&
                  topOfNavigationStack) {
                transferCubit.init();
              }
            },
            child: const SizedBox.shrink(),
          ),
          buildHeader(),
          const HeightBox(slab: 3),
          buildSuccessImage(),
          const HeightBox(slab: 3),
          buildSuccessLabel(),
          const HeightBox(slab: 2),
          buildBalanceLabel(),
          const HeightBox(slab: 2),
          buildConfirmationContainer(),
          PrimaryButton(
            text: PaymentStrings.done,
            color: AppColors.parrotColor,
            onPressed: () => context.router.push(PaymentDashboardRoute()),
          ),
          const HeightBox(slab: 5),
        ],
      ),
    );
  }
}
