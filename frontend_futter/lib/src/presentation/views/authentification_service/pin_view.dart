import 'package:cardpay/src/config/screen_utills/screen_util.dart';
import 'package:cardpay/src/presentation/cubits/remote/balance_cubit.dart';
import 'package:cardpay/src/presentation/cubits/remote/pin_cubit.dart';
import 'package:cardpay/src/presentation/cubits/remote/recent_transactions_cubit.dart';
import 'package:cardpay/src/presentation/cubits/remote/user_cubit.dart';
import 'package:cardpay/src/presentation/widgets/boxes/horizontal_padding.dart';
import 'package:cardpay/src/presentation/widgets/loadings/overlay_loading.dart';
import 'package:flutter/material.dart';
import 'package:auto_route/auto_route.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:cardpay/src/config/router/app_router.dart';
import 'package:cardpay/src/config/themes/colors.dart';
import 'package:cardpay/src/utils/constants/signUp_string.dart';
import '../../widgets/layout/pin_numpad_layout.dart';

@RoutePage()
class PinView extends HookWidget {
  const PinView({super.key});

  @override
  Widget build(BuildContext context) {
    final pinController = useTextEditingController();
    final showErrorMessage = useState(false);
    final isPinConfirmed = useState(false);
    final error = useState('');

    String prevPin = '';

    final userCubit = BlocProvider.of<UserCubit>(context);
    final pinCubit = BlocProvider.of<PinCubit>(context);
    final balanceCubit = BlocProvider.of<BalanceCubit>(context);
    final recentTransactionsCubit =
        BlocProvider.of<RecentTransactionsCubit>(context);

    void handlePinSetup() {
      String newPin = pinController.text;

      if (isPinConfirmed.value) {
        if (newPin == prevPin && prevPin != '0000') {
          pinCubit.changePin(pinController.text);
          return;
        }

        showErrorMessage.value = true;
        isPinConfirmed.value = false;
        error.value = AppStrings.passwordNotMatched;
        prevPin = '';
        pinController.clear();
        return;
      }

      if (newPin == '0000') {
        showErrorMessage.value = true;
        isPinConfirmed.value = false;
        error.value = AppStrings.weakPassword;
        pinController.clear();
        return;
      }

      isPinConfirmed.value = true;
      prevPin = newPin;
      pinController.clear();
    }

    useEffect(() {
      return () {
        pinController.dispose();
      };
    }, []);

    return Scaffold(
      backgroundColor: AppColors.darkBlueColor,
      body: SingleChildScrollView(
        child: Stack(
          children: [
            BlocConsumer<PinCubit, PinState>(
              builder: (_, state) {
                switch (state.runtimeType) {
                  case PinLoading:
                    return const OverlayLoading(inSafeArea: false);
                  default:
                    return const SizedBox.shrink();
                }
              },
              listener: (_, state) {
                switch (state.runtimeType) {
                  case PinSuccess:
                    userCubit.getUser();
                    balanceCubit.getUserBalance();
                    recentTransactionsCubit.getUserRecentTransactions();

                    context.router.pushAndPopUntil(
                      PaymentDashboardRoute(),
                      predicate: (route) => route.data?.name == "IntroRoute",
                    );
                }
              },
            ),
            SizedBox(
              height: ScreenUtil.screenHeight(context),
              child: Column(
                children: [
                  Expanded(flex: 2, child: Container()),
                  PaddingHorizontal(
                    slab: 2,
                    child: Text(
                      textAlign: TextAlign.center,
                      isPinConfirmed.value
                          ? AppStrings.confirmPin
                          : AppStrings.enterPin,
                      style: AppTypography.mainHeadingWhite,
                    ),
                  ),
                  Expanded(flex: 1, child: Container()),
                  if (showErrorMessage.value)
                    Text(
                      error.value,
                      style: AppTypography.errorText,
                    ),
                  Expanded(flex: 2, child: Container()),
                  PinEntry(
                    controller: pinController,
                    onPinEntered: handlePinSetup,
                  ),
                  Expanded(flex: 1, child: Container()),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
