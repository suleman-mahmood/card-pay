import 'package:cardpay/src/presentation/cubits/remote/deposit_cubit.dart';
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
import 'package:url_launcher/url_launcher.dart';

class DepositViewConstants {
  static const title = PaymentStrings.depositMoney;
  static const buttonText = PaymentStrings.continueText;
}

@RoutePage()
class DepositAmountView extends HookWidget {
  const DepositAmountView({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final paymentController = useTextEditingController(text: '');
    final selectedButton = useState<String?>(null);
    final depositCubit = BlocProvider.of<DepositCubit>(context);

    useEffect(() {
      return () {
        paymentController.dispose();
      };
    }, []);

    showDepositUrl(String checkoutUrl) async {
      await launchUrl(Uri.parse(checkoutUrl));

      depositCubit.init();
    }

    Widget buildAmountDisplay() {
      return PaddingAll(
        slab: 1,
        child: ValueListenableBuilder(
          valueListenable: paymentController,
          builder: (context, value, child) {
            final text = paymentController.text.isEmpty
                ? '_ _ _ _'
                : paymentController.text;

            return SizedBox(
              height: 48,
              child: ListView.separated(
                shrinkWrap: true,
                itemCount: text.length,
                separatorBuilder: (context, index) => const HeightBox(slab: 1),
                scrollDirection: Axis.horizontal,
                itemBuilder: (context, index) {
                  return Text(text[index],
                      style: AppTypography.mainHeadingGrey);
                },
              ),
            );
          },
        ),
      );
    }

    Widget paymentButton(String amount) {
      return OutlinedButton(
        style: OutlinedButton.styleFrom(
          side: const BorderSide(color: AppColors.greyColor),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(10),
          ),
        ),
        onPressed: () {
          selectedButton.value = amount;
          paymentController.text = amount;
        },
        child: Padding(
          padding: const EdgeInsets.fromLTRB(8, 8, 8, 8),
          child: Text(amount, style: AppTypography.bodyText),
        ),
      );
    }

    Widget buildQuickAmountButtons() {
      return Wrap(
        spacing: 9,
        runSpacing: 9,
        alignment: WrapAlignment.spaceEvenly,
        crossAxisAlignment: WrapCrossAlignment.center,
        children: PaymentStrings.quickAmounts
            .map((amount) => paymentButton(amount))
            .toList(),
      );
    }

    return Stack(
      children: [
        Scaffold(
          backgroundColor: AppColors.mediumBlueColor,
          body: Align(
            alignment: Alignment.bottomCenter,
            child: Container(
              decoration: const BoxDecoration(
                color: AppColors.secondaryColor,
                borderRadius: BorderRadius.only(
                  topLeft: Radius.circular(30.0),
                  topRight: Radius.circular(30.0),
                ),
              ),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  const HeightBox(slab: 3),
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
                  buildAmountDisplay(),
                  const HeightBox(slab: 2),
                  buildQuickAmountButtons(),
                  const HeightBox(slab: 2),
                  NumPad(
                    controller: paymentController,
                    buttonColor: AppColors.greyColor,
                  ),
                  const HeightBox(slab: 1),
                  PrimaryButton(
                    color: AppColors.mediumBlueColor,
                    text: PaymentStrings.continueText,
                    onPressed: () {
                      if (paymentController.text.isEmpty) return;

                      final amount = int.parse(paymentController.text);
                      depositCubit.createDepositRequest(amount);
                    },
                  ),
                  const HeightBox(slab: 4),
                ],
              ),
            ),
          ),
        ),
        const PaddingHorizontal(
          slab: 2,
          child: Header(title: DepositViewConstants.title),
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
