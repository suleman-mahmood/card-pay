import 'package:cardpay/src/config/router/app_router.dart';
import 'package:cardpay/src/domain/models/p2p_request_info.dart';
import 'package:cardpay/src/presentation/cubits/remote/balance_cubit.dart';
import 'package:cardpay/src/presentation/cubits/remote/transfer_cubit.dart';
import 'package:cardpay/src/presentation/widgets/boxes/height_box.dart';
import 'package:cardpay/src/presentation/widgets/layout/basic_view_layout.dart';
import 'package:cardpay/src/presentation/widgets/loadings/overlay_loading.dart';
import 'package:flutter/material.dart';
import 'package:auto_route/auto_route.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:cardpay/src/config/themes/colors.dart';
import 'package:cardpay/src/presentation/widgets/actions/button/primary_button.dart';
import 'package:cardpay/src/utils/constants/payment_strings.dart';

@RoutePage()
class RequestConfirmationView extends HookWidget {
  final P2PRequestInfo requestInfo;

  const RequestConfirmationView({
    Key? key,
    required this.requestInfo,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final balanceCubit = BlocProvider.of<BalanceCubit>(context);

    final transferCubit = BlocProvider.of<TransferCubit>(context);

    void handleRequestAcceptance() {
      FocusScope.of(context).unfocus();
      transferCubit.acceptP2PPullTransaction(requestInfo.txId);
    }

    void handleRequestDeclination() {
      FocusScope.of(context).unfocus();
      transferCubit.declineP2PPullTransaction(requestInfo.txId);
    }

    return BasicViewLayout(
      headerTitle: PaymentStrings.enterAmountTitle,
      backgroundColor: AppColors.mediumGreenColor,
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      bottomSafeArea: false,
      children: [
        Stack(
          children: [
            Column(
              children: [
                SizedBox(
                  width: MediaQuery.of(context).size.width,
                  child: Column(
                    children: [
                      Stack(
                        alignment: Alignment.center,
                        children: [
                          CircleAvatar(
                            backgroundColor: Colors.black26,
                            radius: MediaQuery.of(context).size.width * 0.25,
                          ),
                          Text(
                            // TODO: handle this
                            'AK',
                            style: AppTypography.mainHeadingWhite.copyWith(
                              fontSize:
                                  MediaQuery.of(context).size.width * 0.15,
                            ),
                          ),
                        ],
                      ),
                      const HeightBox(slab: 2),
                      Text(
                        requestInfo.fullName,
                        style: AppTypography.mainHeadingWhite.copyWith(
                          fontSize: 28,
                        ),
                      ),
                      const HeightBox(slab: 1),
                      Text(
                        // TODO: fix this
                        '23100011', // requestInfo.uniqueIdentifier
                        style: AppTypography.bodyText.copyWith(
                          color: Colors.white70,
                          fontSize: 22,
                        ),
                      ),
                    ],
                  ),
                ),
                SizedBox(height: 10),
                Container(
                  width: MediaQuery.of(context).size.width,
                  height: MediaQuery.of(context).size.height * 0.42,
                  decoration: const BoxDecoration(
                    color: Colors.white,
                    borderRadius: BorderRadius.only(
                      topLeft: Radius.circular(25),
                      topRight: Radius.circular(25),
                    ),
                    boxShadow: [
                      BoxShadow(
                        color: Colors.black12,
                        blurRadius: 10,
                        offset: Offset(0, -5),
                      ),
                    ],
                  ),
                  child: Column(
                    children: [
                      const HeightBox(slab: 2),
                      Container(
                        width: 40,
                        height: 5,
                        decoration: BoxDecoration(
                          color: Colors.black54,
                          borderRadius: BorderRadius.circular(25),
                        ),
                      ),
                      Spacer(),
                      Text(
                        'RS. ${requestInfo.amount}',
                        style: AppTypography.mainHeadingWhite.copyWith(
                          fontSize: 48,
                          color: AppColors.blackColor.withOpacity(0.7),
                          fontWeight: FontWeight.w900,
                        ),
                      ),
                      Text(
                        'will be sent to ${requestInfo.fullName}',
                        style: AppTypography.bodyText.copyWith(
                          color: Colors.black54,
                          fontSize: 14,
                        ),
                      ),
                      const HeightBox(slab: 4),
                      RichText(
                        text: TextSpan(
                          text: 'Remaining Balance: ',
                          style: AppTypography.bodyText.copyWith(
                            color: Colors.black54,
                            fontWeight: FontWeight.bold,
                          ),
                          children: <TextSpan>[
                            TextSpan(
                              text:
                                  'Rs. ${balanceCubit.state.balance.amount - requestInfo.amount}',
                              style: AppTypography.bodyText.copyWith(
                                color: AppColors.blackColor.withOpacity(0.54),
                                fontWeight: FontWeight.normal,
                              ),
                            ),
                          ],
                        ),
                      ),
                      const HeightBox(slab: 4),
                      PrimaryButton(
                        text: PaymentStrings.send,
                        color: AppColors.mediumGreenColor,
                        textColor: AppColors.secondaryColor,
                        onPressed: handleRequestAcceptance,
                      ),
                      const HeightBox(slab: 2),
                      PrimaryButton(
                        text: PaymentStrings.decline,
                        color: AppColors.secondaryColor,
                        textColor: AppColors.redColor,
                        onPressed: handleRequestDeclination,
                      ),
                      const Spacer(),
                    ],
                  ),
                ),

                // Shhh, listeners
                BlocListener<TransferCubit, TransferState>(
                  listener: (_, state) {
                    switch (state.runtimeType) {
                      case TransferSuccess:
                        context.router.push(
                          ReceiptRoute(
                            amount: requestInfo.amount,
                            recipientName: requestInfo.fullName,
                          ),
                        );
                        break;
                      case TransferPullDeclined:
                        //  TODO: Add a decline pop
                        context.router.pushAndPopUntil(
                          DashboardLayoutRoute(),
                          predicate: (route) =>
                              route.data?.name == "LoginRoute",
                        );
                        break;
                    }
                  },
                  child: const SizedBox.shrink(),
                ),
              ],
            ),
            BlocBuilder<TransferCubit, TransferState>(
              builder: (_, state) {
                switch (state.runtimeType) {
                  case TransferLoading:
                    return const OverlayLoading();
                  default:
                    return const SizedBox.shrink();
                }
              },
            ),
          ],
        ),
      ],
    );
  }
}
