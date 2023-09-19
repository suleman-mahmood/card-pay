import 'package:auto_route/auto_route.dart';
import 'package:cardpay/src/config/router/app_router.dart';
import 'package:cardpay/src/config/screen_utills/box_shadow.dart';
import 'package:cardpay/src/presentation/cubits/remote/deposit_cubit.dart';
import 'package:cardpay/src/presentation/cubits/remote/full_name_cubit.dart';
import 'package:cardpay/src/presentation/cubits/remote/transfer_cubit.dart';
import 'package:cardpay/src/presentation/widgets/boxes/height_box.dart';
import 'package:cardpay/src/presentation/widgets/boxes/horizontal_padding.dart';
import 'package:cardpay/src/presentation/widgets/loadings/inputfield_shimmer_loading.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:cardpay/src/config/themes/colors.dart';
import 'package:cardpay/src/presentation/widgets/actions/button/payment_input_buttons.dart';
import 'package:cardpay/src/presentation/widgets/actions/button/primary_button.dart';
import 'package:cardpay/src/presentation/widgets/navigations/top_navigation.dart';
import 'package:url_launcher/url_launcher.dart';

class TransactionView extends HookWidget {
  final String title;
  final String buttonText;
  final String? recipientVendor;
  final bool displayRecipient;
  final Color backgroundColor;
  final void Function(int) onButtonPressed;

  const TransactionView({
    super.key,
    required this.title,
    required this.buttonText,
    required this.displayRecipient,
    required this.backgroundColor,
    required this.onButtonPressed,
    this.recipientVendor,
  });

  @override
  Widget build(BuildContext context) {
    final paymentController = useTextEditingController(text: '');
    final depositCubit = BlocProvider.of<DepositCubit>(context);
    final fullNameCubit = BlocProvider.of<FullNameCubit>(context);

    useEffect(() {
      return () {
        paymentController.dispose();
      };
    }, []);

    showDepositUrl(String checkoutUrl) async {
      await launchUrl(Uri.parse(checkoutUrl));

      depositCubit.init();
    }

    return Scaffold(
      backgroundColor: backgroundColor,
      body: Stack(
        children: [
          Align(
            alignment: Alignment.bottomCenter,
            child: Container(
              decoration: CustomBoxDecoration.getDecoration(),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  const HeightBox(slab: 3),
                  BlocConsumer<TransferCubit, TransferState>(
                    builder: (_, state) {
                      switch (state.runtimeType) {
                        case TransferFailed:
                          return Text(
                            state.errorMessage,
                            style: const TextStyle(color: Colors.red),
                            textAlign: TextAlign.center,
                          );
                        default:
                          return const SizedBox.shrink();
                      }
                    },
                    listener: (_, state) {
                      switch (state.runtimeType) {
                        case TransferSuccess:
                          context.router.push(ConfirmationRoute(
                            uniqueIdentifier: fullNameCubit.state.fullName,
                            amount: int.parse(paymentController.text),
                          ));
                          break;
                      }
                    },
                  ),
                  BlocConsumer<DepositCubit, DepositState>(
                    builder: (_, state) {
                      switch (state.runtimeType) {
                        case DepositFailed:
                          return Text(
                            state.errorMessage,
                            style: const TextStyle(color: Colors.red),
                            textAlign: TextAlign.center,
                          );
                        default:
                          return const SizedBox.shrink();
                      }
                    },
                    listener: (_, state) {
                      switch (state.runtimeType) {
                        case DepositSuccess:
                          showDepositUrl(state.checkoutUrl);
                          break;
                      }
                    },
                  ),
                  Visibility(
                    visible: displayRecipient,
                    child: Container(
                      width: MediaQuery.of(context).size.width * 0.9,
                      padding: const EdgeInsets.all(8),
                      decoration: BoxDecoration(
                        color: AppColors.secondaryColor,
                        border: Border.all(
                          color: AppColors.greyColor,
                          width: 2,
                        ),
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: recipientVendor == null
                          ? BlocBuilder<FullNameCubit, FullNameState>(
                              builder: (_, state) {
                                switch (state.runtimeType) {
                                  case FullNameLoading:
                                    return Positioned.fill(
                                        child: FieldShimmer());
                                  case FullNameSuccess:
                                    return Text(
                                      state.fullName,
                                      style: AppTypography.mainHeading,
                                      textAlign: TextAlign.center,
                                    );
                                  case FullNameFailed:
                                    return Text(
                                      "User doesn't exist",
                                      style: AppTypography.mainHeading,
                                      textAlign: TextAlign.center,
                                    );
                                  default:
                                    return const SizedBox.shrink();
                                }
                              },
                            )
                          : Text(
                              recipientVendor!,
                              style: AppTypography.mainHeading,
                              textAlign: TextAlign.center,
                            ),
                    ),
                  ),
                  PaymentEntry(controller: paymentController),
                  const HeightBox(slab: 1),
                  PrimaryButton(
                    color: backgroundColor,
                    text: buttonText,
                    onPressed: () {
                      if (paymentController.text.isEmpty) return;
                      onButtonPressed(
                        int.parse(paymentController.text),
                      );
                    },
                  ),
                  const HeightBox(slab: 4),
                ],
              ),
            ),
          ),
          PaddingHorizontal(slab: 2, child: Header(title: title)),
        ],
      ),
    );
  }
}
