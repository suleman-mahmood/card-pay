import 'package:cardpay/src/presentation/cubits/remote/full_name_cubit.dart';
import 'package:cardpay/src/presentation/cubits/remote/user_cubit.dart';
import 'package:cardpay/src/presentation/widgets/boxes/height_box.dart';
import 'package:cardpay/src/presentation/widgets/navigations/top_navigation.dart';
import 'package:cardpay/src/presentation/widgets/boxes/horizontal_padding.dart';
import 'package:flutter/material.dart';
import 'package:auto_route/auto_route.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:cardpay/src/config/router/app_router.dart';
import 'package:cardpay/src/config/themes/colors.dart';
import 'package:cardpay/src/presentation/widgets/actions/button/primary_button.dart';
import 'package:cardpay/src/presentation/widgets/text_inputs/input_field.dart';
import 'package:cardpay/src/utils/constants/payment_strings.dart';
import 'package:cardpay/src/utils/constants/auth_strings.dart';

@RoutePage()
class TransferRecipientView extends HookWidget {
  const TransferRecipientView({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final rollNumberController = useTextEditingController();

    final userNameCubit = BlocProvider.of<FullNameCubit>(context);
    final userCubit = BlocProvider.of<UserCubit>(context);

    void handleSubmit() {
      FocusScope.of(context).unfocus();
      final uniqueIdentifier = rollNumberController.text;

      userNameCubit.getFullName(
        uniqueIdentifier: uniqueIdentifier,
        closedLoopId: userCubit.state.user.closedLoops[0].closedLoopId,
      );

      context.router.push(
        TransferAmountRoute(
          recipientUniqueIdentifier: uniqueIdentifier,
          closedLoopId: userCubit.state.user.closedLoops[0].closedLoopId,
        ),
      );
    }

    return Scaffold(
      backgroundColor: AppColors.parrotColor,
      body: SafeArea(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            const PaddingHorizontal(
              slab: 2,
              child: Header(title: PaymentStrings.transferMoney),
            ),
            Padding(
              padding: const EdgeInsets.all(16.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.center,
                children: [
                  const HeightBox(slab: 3),
                  CustomInputField(
                    label: AppStrings.rollNumber,
                    controller: rollNumberController,
                    hint: AppStrings.enterRollNumber,
                    keyboardType: TextInputType.number,
                    hintColor: AppColors.greyColor,
                    labelColor: AppColors.secondaryColor,
                    color: AppColors.secondaryColor,
                  ),
                  const HeightBox(slab: 1),
                  Align(
                    alignment: Alignment.centerLeft,
                    child: Text(
                      PaymentStrings.enterAmount,
                      style: AppTypography.bodyText,
                    ),
                  ),
                  const HeightBox(slab: 5),
                  PrimaryButton(
                    text: PaymentStrings.next,
                    color: AppColors.secondaryColor,
                    textColor: AppColors.parrotColor,
                    onPressed: handleSubmit,
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
