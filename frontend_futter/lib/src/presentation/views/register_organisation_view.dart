import 'package:cardpay/src/config/router/app_router.dart';
import 'package:cardpay/src/config/themes/colors.dart';
import 'package:cardpay/src/presentation/widgets/boxes/height_box.dart';
import 'package:cardpay/src/presentation/widgets/communication/progress_bar/divder.dart';
import 'package:cardpay/src/domain/models/closed_loop.dart';
import 'package:cardpay/src/presentation/cubits/remote/closed_loop_cubit.dart';
import 'package:cardpay/src/presentation/cubits/remote/user_cubit.dart';
import 'package:cardpay/src/presentation/widgets/boxes/height_box.dart';
import 'package:cardpay/src/utils/constants/event_codes.dart';
import 'package:flutter/material.dart';
import 'package:auto_route/auto_route.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:cardpay/src/presentation/widgets/containment/bottom_sheet_otp.dart';
import 'package:cardpay/src/presentation/widgets/headings/main_heading.dart';
import 'package:cardpay/src/presentation/widgets/layout/auth_layout.dart';
import 'package:cardpay/src/presentation/widgets/selections/organization_drop_down.dart';
import 'package:cardpay/src/presentation/widgets/actions/button/primary_button.dart';
import 'package:cardpay/src/presentation/widgets/text_inputs/input_field.dart';
import 'package:cardpay/src/utils/constants/signUp_string.dart';

@RoutePage()
class RegisterView extends HookWidget {
  const RegisterView({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final showRollNumberField = useState<bool>(false);
    final uniqueIdentifier = useState<String>('');
    final selectedClosedLoop = useState<ClosedLoop>(ClosedLoop());
    final uniqueIdentifierOtp = useState<String>('');

    final userCubit = BlocProvider.of<UserCubit>(context);
    final closedLoopCubit = BlocProvider.of<ClosedLoopCubit>(context);

    useEffect(() {
      someFunction() async {
        await closedLoopCubit.getAllClosedLoops();
      }

      someFunction();
    }, []);

    void _showOTPBottomSheet() {
      showModalBottomSheet(
        context: context,
        builder: (BuildContext context) {
          return SingleChildScrollView(
            child: BottomSheetOTP(
              deviceCheckHeading: AppStrings.checkEmail,
              otpDeviceText: AppStrings.otpEmailText,
              onAction: () => {
                userCubit.verifyClosedLoop(
                  selectedClosedLoop.value.id,
                  uniqueIdentifierOtp.value,
                )
              },
              onChanged: (v) => uniqueIdentifierOtp.value = v,
            ),
          );
        },
      );
    }

    return AuthLayout(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          BlocBuilder<UserCubit, UserState>(builder: (_, state) {
            switch (state.runtimeType) {
              case UserSuccess:
                if (state.eventCodes == EventCodes.ORGANIZATION_REGISTERED) {
                  WidgetsBinding.instance.addPostFrameCallback((_) {
                    _showOTPBottomSheet();
                  });
                } else if (state.eventCodes ==
                    EventCodes.ORGANIZATION_VERIFIED) {
                  context.router.push(const AuthRoute());
                }
                return const SizedBox.shrink();
              default:
                return const SizedBox.shrink();
            }
          }),
          const HeightBox(slab: 4),
          Row(
            children: [
              Expanded(
                flex: 2,
                child: CustomDivider(
                  indent: 50,
                  color: AppColors.primaryColor,
                  endIndent: 10,
                ),
              ),
              Expanded(
                flex: 2,
                child: CustomDivider(
                  indent: 10,
                  color: AppColors.primaryColor,
                  endIndent: 50,
                ),
              ),
            ],
          ),
          const HeightBox(slab: 4),
          const MainHeading(
            accountTitle: AppStrings.register,
            accountDescription: AppStrings.sign,
          ),
          const HeightBox(slab: 4),
          DropDown(
            onChanged: (value, closedLoop) {
              showRollNumberField.value = value != 'None';
              selectedClosedLoop.value = closedLoop;
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
            child: CustomInputField(
              label: AppStrings.rollNumber,
              hint: AppStrings.enterRollNumber,
              onChanged: (v) => uniqueIdentifier.value = v,
              validator: (uniqueIdentifierValue) {
                if (uniqueIdentifierValue == null) {
                  return "Please enter your roll number";
                }
                final regExp = RegExp(selectedClosedLoop.value.regex);
                if (!regExp.hasMatch(uniqueIdentifierValue)) {
                  return "Invalid roll number";
                }
                return null;
              },
            ),
          ),
          const HeightBox(slab: 4),
          Center(
            child: PrimaryButton(
              text: AppStrings.create,
              onPressed: () => {
                userCubit.registerClosedLoop(
                  selectedClosedLoop.value.id,
                  uniqueIdentifier.value,
                )
              },
            ),
          )
        ],
      ),
    );
  }
}
