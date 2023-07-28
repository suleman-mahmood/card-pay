import 'package:cardpay/src/presentation/widgets/boxes/height_box.dart';
import 'package:cardpay/src/presentation/views/payment_dashboard_view.dart';
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
class RequestView extends HookWidget {
  const RequestView({Key? key}) : super(key: key);

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
          ),
          HeightBox(slab: 1),
          Align(
              alignment: Alignment.centerLeft,
              child: Text(PaymentStrings.enterAmount,
                  style: AppTypography.headingFont)),
          HeightBox(slab: 5),
          PrimaryButton(
            text: PaymentStrings.next,
            color: AppColors.secondaryColor,
            textColor: AppColors.purpleColor,
            onPressed: () {
              String uniqueIdentifier = rollNumberController.text;

              context.router
                  .push(RequestAmountRoute(uniqueIdentifier: uniqueIdentifier));
            },
          ),
        ],
      );
    }

    // return PaymentLayout(
    //   showBottomBar: false,
    //   useHorizontalPadding: true,
    //   backgroundColor: AppColors.purpleColor,
    return Scaffold(
      backgroundColor: AppColors.purpleColor,
      body: SingleChildScrollView(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Header(
                title: PaymentStrings.requestMoney,
              ),
              buildTransferForm(),
            ],
          ),
        ),
      ),
    );
  }
}