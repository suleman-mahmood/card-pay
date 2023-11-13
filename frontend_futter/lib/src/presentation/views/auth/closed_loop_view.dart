import 'package:cardpay/src/config/router/app_router.dart';
import 'package:cardpay/src/config/screen_utills/box_shadow.dart';
import 'package:cardpay/src/config/themes/colors.dart';
import 'package:cardpay/src/presentation/widgets/boxes/height_box.dart';
import 'package:cardpay/src/presentation/widgets/communication/progress_bar/divder.dart';
import 'package:cardpay/src/domain/models/closed_loop.dart';
import 'package:cardpay/src/presentation/cubits/remote/closed_loop_cubit.dart';
import 'package:cardpay/src/utils/constants/event_codes.dart';
import 'package:flutter/material.dart';
import 'package:auto_route/auto_route.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:cardpay/src/presentation/widgets/containment/bottom_sheets/bottom_sheet_otp.dart';
import 'package:cardpay/src/presentation/widgets/headings/main_heading.dart';
import 'package:cardpay/src/presentation/widgets/layout/auth_layout.dart';
import 'package:cardpay/src/presentation/widgets/selections/organization_drop_down.dart';
import 'package:cardpay/src/presentation/widgets/actions/button/primary_button.dart';
import 'package:cardpay/src/presentation/widgets/text_inputs/input_field.dart';
import 'package:cardpay/src/utils/constants/auth_strings.dart';

@RoutePage()
class ClosedLoopView extends HookWidget {
  const ClosedLoopView({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final showRollNumberField = useState<bool>(false);
    final uniqueIdentifier = useState<String>('');
    final referralUniqueIdentifier = useState<String>('');
    final selectedClosedLoop = useState<ClosedLoop>(ClosedLoop());
    final formKey = useMemoized(() => GlobalKey<FormState>());

    final closedLoopCubit = BlocProvider.of<ClosedLoopCubit>(context);

    void _showOTPBottomSheet() {
      showModalBottomSheet(
        context: context,
        builder: (BuildContext context) {
          return SingleChildScrollView(
            child: Container(
              decoration: CustomBoxDecoration.getDecoration(),
              child: BottomSheetOTP(
                deviceCheckHeading: AppStrings.checkEmail,
                otpDeviceText:
                    '${AppStrings.otpEmailText} ${uniqueIdentifier.value}@lums.edu.pk',
                onAction: (otp) => closedLoopCubit.verifyClosedLoop(
                  selectedClosedLoop.value.id,
                  otp,
                  referralUniqueIdentifier.value,
                ),
              ),
            ),
          );
        },
      );
    }

    void handleRegisterClosedLoop() async {
      if (!formKey.currentState!.validate()) {
        return;
      }

      await closedLoopCubit.registerClosedLoop(
        selectedClosedLoop.value.id,
        uniqueIdentifier.value,
      );
    }

    return AuthLayout(
      logoutOnBack: true,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const HeightBox(slab: 4),
          const Row(
            children: [
              HeightBox(slab: 5),
              Expanded(
                flex: 2,
                child: CustomDivider(
                  thickness: 3,
                  indent: 70,
                  color: AppColors.primaryColor,
                  endIndent: 5,
                ),
              ),
              Expanded(
                flex: 2,
                child: CustomDivider(
                  indent: 5,
                  thickness: 3,
                  color: AppColors.primaryColor,
                  endIndent: 70,
                ),
              ),
            ],
          ),
          const MainHeading(
            accountTitle: AppStrings.register,
            accountDescription: AppStrings.sign,
          ),
          const HeightBox(slab: 4),
          DropDown(
            onInstituteChanged: (value, closedLoop) {
              if (value == promptText) {
                showRollNumberField.value = false;
                return;
              }
              showRollNumberField.value = true;
              selectedClosedLoop.value = closedLoop!;
            },
          ),
          Visibility(
            visible: showRollNumberField.value,
            maintainSize: false,
            child: const HeightBox(slab: 2),
          ),
          Visibility(
            visible: showRollNumberField.value,
            maintainSize: false,
            child: Form(
              key: formKey,
              child: Column(
                children: [
                  CustomInputField(
                    label: AppStrings.rollNumber,
                    hint: AppStrings.enterRollNumber,
                    onChanged: (v) => uniqueIdentifier.value = v.trim(),
                    validator: (uniqueIdentifierValue) {
                      if (uniqueIdentifierValue == null) {
                        return AppStrings.nullRollNumber;
                      }
                      final regExp = RegExp(selectedClosedLoop.value.regex);
                      if (!regExp.hasMatch(uniqueIdentifierValue)) {
                        return AppStrings.invalidRollNumber;
                      }
                      return null;
                    },
                  ),
                  const HeightBox(slab: 2),
                  CustomInputField(
                    label: AppStrings.referralRollNumber,
                    hint: AppStrings.enterRollNumber,
                    onChanged: (v) => referralUniqueIdentifier.value = v.trim(),
                    validator: (referralUniqueIdentifierValue) {
                      if (referralUniqueIdentifierValue == null ||
                          referralUniqueIdentifierValue == '') {
                        return null;
                      }
                      final regExp = RegExp(selectedClosedLoop.value.regex);
                      if (!regExp.hasMatch(referralUniqueIdentifierValue)) {
                        return AppStrings.invalidRollNumber;
                      }
                      return null;
                    },
                  ),
                ],
              ),
            ),
          ),
          const HeightBox(slab: 4),
          BlocBuilder<ClosedLoopCubit, ClosedLoopState>(
            builder: (_, state) {
              switch (state.runtimeType) {
                case ClosedLoopFailed || ClosedLoopUnknownFailure:
                  return Column(
                    children: [
                      Text(
                        state.errorMessage,
                        style: const TextStyle(color: Colors.red),
                        textAlign: TextAlign.center,
                      ),
                      const HeightBox(slab: 4),
                    ],
                  );
                default:
                  return const SizedBox.shrink();
              }
            },
          ),
          Visibility(
            visible: showRollNumberField.value,
            child: Center(
              child: PrimaryButton(
                text: AppStrings.create,
                onPressed: handleRegisterClosedLoop,
              ),
            ),
          ),
          BlocListener<ClosedLoopCubit, ClosedLoopState>(
            listener: (_, state) {
              switch (state.runtimeType) {
                case ClosedLoopSuccess:
                  if (state.eventCodes == EventCodes.ORGANIZATION_REGISTERED) {
                    WidgetsBinding.instance.addPostFrameCallback((_) {
                      _showOTPBottomSheet();
                    });
                  } else if (state.eventCodes ==
                      EventCodes.ORGANIZATION_VERIFIED) {
                    context.router.push(const PinRoute());
                  }
                  break;
              }
            },
            child: const SizedBox.shrink(),
          ),
        ],
      ),
    );
  }
}
