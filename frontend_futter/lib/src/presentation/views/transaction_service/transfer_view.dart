import 'package:cardpay/src/presentation/widgets/boxes/height_box.dart';
import 'package:cardpay/src/presentation/widgets/navigations/top_navigation.dart';
import 'package:flutter/material.dart';
import 'package:auto_route/auto_route.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:cardpay/src/config/router/app_router.dart';
import 'package:cardpay/src/config/themes/colors.dart';
import 'package:cardpay/src/presentation/widgets/actions/button/primary_button.dart';
import 'package:cardpay/src/presentation/widgets/text_inputs/input_field.dart';
import 'package:cardpay/src/utils/constants/payment_string.dart';
import 'package:cardpay/src/utils/constants/signUp_string.dart';

@RoutePage()
class TransferView extends HookWidget {
  const TransferView({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final rollNumberController = useTextEditingController();

    Widget buildTransferForm() {
      return Column(
        children: [
          HeightBox(slab: 3),
          CustomInputField(
            label: AppStrings.rollNumber,
            hint: PaymentStrings.anyRollNumber,
            controller: rollNumberController,
            keyboardType: TextInputType.number,
            hintColor: AppColors.greyColor,
            labelColor: AppColors.secondaryColor,
            color: AppColors.secondaryColor,
          ),
          HeightBox(slab: 1),
          Align(
              alignment: Alignment.centerLeft,
              child: Text(PaymentStrings.enterAmount,
                  style: AppTypography.bodyText)),
          HeightBox(slab: 5),
          PrimaryButton(
            text: PaymentStrings.next,
            color: AppColors.secondaryColor,
            textColor: AppColors.parrotColor,
            onPressed: () {
              String uniqueIdentifier = rollNumberController.text;

              context.router.push(SendRoute(
                uniqueIdentifier: uniqueIdentifier,
              ));
            },
          ),
        ],
      );
    }

    // return PaymentLayout(
    //   showBottomBar: false,
    //   useHorizontalPadding: true,
    //   backgroundColor: AppColors.parrotColor,
    return Scaffold(
      backgroundColor: AppColors.parrotColor,
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Header(
              title: PaymentStrings.transferMoney,
            ),
            buildTransferForm(),
          ],
        ),
      ),
    );
  }
}
