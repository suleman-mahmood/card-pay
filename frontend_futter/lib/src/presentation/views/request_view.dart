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

    return Scaffold(
      backgroundColor: AppColors.purpleColor,
      body: LayoutBuilder(
        builder: (BuildContext context, BoxConstraints viewportConstraints) {
          return SingleChildScrollView(
            child: ConstrainedBox(
              constraints: BoxConstraints(
                minHeight: viewportConstraints.maxHeight,
              ),
              child: Padding(
                padding: const EdgeInsets.all(15.0),
                child: Column(
                  crossAxisAlignment:
                      CrossAxisAlignment.start, // updated this line
                  children: [
                    _buildTransferHeader(context),
                    _buildTransferForm(context, rollNumberController),
                  ],
                ),
              ),
            ),
          );
        },
      ),
    );
  }

  Widget _buildTransferHeader(BuildContext context) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        IconButton(
          icon: const Icon(
            Icons.arrow_back,
            color: AppColors.secondaryColor,
          ),
          onPressed: () => context.router.pop(),
        ),
        Text(
          PaymentStrings.requestMoney,
          style: AppTypography.mainHeading.copyWith(
            color: AppColors.secondaryColor,
          ),
        ),
        const IconButton(
          icon: Icon(Icons.arrow_back, color: Colors.transparent),
          onPressed: null,
          disabledColor: Colors.transparent,
        ),
      ],
    );
  }

  Widget _buildTransferForm(
      BuildContext context, TextEditingController rollNumberController) {
    return Column(
      children: [
        const SizedBox(height: 10.0),
        CustomInputField(
          label: AppStrings.rollNumber,
          hint: '24xxxxxx',
          color: AppColors.secondaryColor,
          textcolor: AppColors.secondaryColor,
          controller: rollNumberController,
          keyboardType: TextInputType.number,
        ),
        Text(
          PaymentStrings.enterAmount,
          style: AppTypography.headingFont.copyWith(
            color: AppColors.secondaryColor,
            fontSize: 16,
          ),
        ),
        const SizedBox(height: 10.0),
        PrimaryButton(
          text: PaymentStrings.next,
          color: AppColors.secondaryColor,
          textColor: AppColors.purpleColor,
          onPressed: () {
            String rollNumber = rollNumberController.text;

            context.router.push(RequestAmountRoute(rollNumber: rollNumber));
            // context.router.pop();
          },
        ),
      ],
    );
  }
}
