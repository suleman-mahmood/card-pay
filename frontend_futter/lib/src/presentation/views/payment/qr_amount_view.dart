import 'package:cardpay/src/config/router/app_router.dart';
import 'package:cardpay/src/presentation/cubits/remote/balance_cubit.dart';
import 'package:cardpay/src/presentation/cubits/remote/recent_transactions_cubit.dart';
import 'package:cardpay/src/presentation/cubits/remote/transfer_cubit.dart';
import 'package:cardpay/src/presentation/widgets/actions/button/numpad_buttons.dart';
import 'package:cardpay/src/presentation/widgets/actions/button/primary_button.dart';
import 'package:cardpay/src/presentation/widgets/boxes/all_padding.dart';
import 'package:cardpay/src/presentation/widgets/boxes/height_box.dart';
import 'package:cardpay/src/presentation/widgets/boxes/horizontal_padding.dart';
import 'package:cardpay/src/presentation/widgets/loadings/overlay_loading.dart';
import 'package:cardpay/src/presentation/widgets/navigations/top_navigation.dart';
import 'package:cardpay/src/utils/constants/payment_strings.dart';
import 'package:flutter/material.dart';
import 'package:auto_route/auto_route.dart';
import 'package:cardpay/src/config/themes/colors.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_hooks/flutter_hooks.dart';

@RoutePage()
class QrAmountView extends HookWidget {
  final String vendorName;
  final String qrId;
  final int v;

  const QrAmountView({
    Key? key,
    required this.vendorName,
    required this.qrId,
    required this.v,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final paymentController = useTextEditingController(text: '');

    final transferCubit = BlocProvider.of<TransferCubit>(context);
    final balanceCubit = BlocProvider.of<BalanceCubit>(context);
    final recentTransactionsCubit =
        BlocProvider.of<RecentTransactionsCubit>(context);

    Widget buildAmountDisplay() {
      return PaddingAll(
        slab: 1,
        child: ValueListenableBuilder(
          valueListenable: paymentController,
          builder: (context, value, child) {
            final text = paymentController.text.isEmpty
                ? 'Rs. 0'
                : 'Rs. ${paymentController.text}';

            return SizedBox(
              height: MediaQuery.of(context).size.width * 0.12,
              child: ListView.separated(
                shrinkWrap: true,
                itemCount: text.length,
                separatorBuilder: (context, index) => const HeightBox(slab: 1),
                scrollDirection: Axis.horizontal,
                itemBuilder: (context, index) {
                  return Text(
                    text[index],
                    style: AppTypography.mainHeadingGrey.copyWith(
                      fontSize: MediaQuery.of(context).size.width * 0.1,
                    ),
                  );
                },
              ),
            );
          },
        ),
      );
    }

    Widget paymentButton(int amount) {
      return OutlinedButton(
        style: OutlinedButton.styleFrom(
          side: const BorderSide(color: AppColors.greyColor),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(10),
          ),
        ),
        onPressed: () => paymentController.text = amount.toString(),
        child: Padding(
          padding: const EdgeInsets.fromLTRB(8, 8, 8, 8),
          child: Text(amount.toString(),
              style: AppTypography.bodyText.copyWith(
                fontSize: MediaQuery.of(context).size.width * 0.04,
              )),
        ),
      );
    }

    Widget buildQuickAmountButtons() {
      return SingleChildScrollView(
        scrollDirection: Axis.horizontal,
        child: Row(
          children: PaymentStrings.quickAmountsQr
              .map((amount) => paymentButton(amount))
              .toList(),
        ),
      );
    }

    Widget buildRecipientInfo() {
      return Container(
        padding: const EdgeInsets.all(8),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(
              Icons.shopping_cart_outlined,
              size: MediaQuery.of(context).size.width * 0.1,
              color: AppColors.secondaryColor,
            ),
            const SizedBox(width: 10),
            Text(
              vendorName,
              style: AppTypography.mainHeading.copyWith(
                fontSize: MediaQuery.of(context).size.width * 0.1,
                color: AppColors.secondaryColor,
              ),
              textAlign: TextAlign.center,
            ),
          ],
        ),
      );
    }

    return Scaffold(
      backgroundColor: AppColors.parrotColor,
      body: Stack(
        children: [
          SafeArea(
            bottom: false,
            child: Column(
              mainAxisAlignment: MainAxisAlignment.start,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const PaddingHorizontal(
                  slab: 2,
                  child: Header(title: PaymentStrings.qrTitle),
                ),
                Spacer(),
                buildRecipientInfo(),
                Container(
                  height: MediaQuery.of(context).size.height * 0.7,
                  decoration: const BoxDecoration(
                    color: AppColors.secondaryColor,
                    borderRadius: BorderRadius.only(
                      topLeft: Radius.circular(30.0),
                      topRight: Radius.circular(30.0),
                    ),
                  ),
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      const HeightBox(slab: 1),
                      BlocConsumer<TransferCubit, TransferState>(
                        builder: (_, state) {
                          switch (state.runtimeType) {
                            case TransferFailed:
                              return Column(
                                children: [
                                  Text(
                                    state.errorMessage,
                                    style: const TextStyle(color: Colors.red),
                                    textAlign: TextAlign.center,
                                  ),
                                  const HeightBox(slab: 3),
                                ],
                              );
                            default:
                              return const SizedBox.shrink();
                          }
                        },
                        listener: (_, state) {
                          switch (state.runtimeType) {
                            case TransferSuccess:
                              balanceCubit.getUserBalance();
                              recentTransactionsCubit
                                  .getUserRecentTransactions();
                              context.router.push(
                                ReceiptRoute(
                                  recipientName: vendorName,
                                  amount: int.parse(paymentController.text),
                                ),
                              );
                              break;
                          }
                        },
                      ),
                      buildAmountDisplay(),
                      //buildQuickAmountButtons(),
                      NumPad(
                        controller: paymentController,
                        buttonColor: AppColors.greyColor,
                      ),
                      const HeightBox(slab: 1),
                      PrimaryButton(
                        color: AppColors.parrotColor,
                        text: PaymentStrings.continueText,
                        onPressed: () {
                          if (paymentController.text.isEmpty) return;

                          final amount = int.parse(paymentController.text);
                          transferCubit.executeQrTransaction(
                            qrId,
                            amount,
                            v,
                          );
                        },
                      ),
                      const HeightBox(slab: 2),
                    ],
                  ),
                ),
              ],
            ),
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
      ),
    );
  }
}
