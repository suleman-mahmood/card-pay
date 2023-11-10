import 'package:cardpay/src/config/themes/colors.dart';
import 'package:cardpay/src/presentation/cubits/remote/checkpoints_cubit.dart';
import 'package:cardpay/src/presentation/cubits/remote/login_cubit.dart';
import 'package:cardpay/src/presentation/cubits/remote/signup_cubit.dart';
import 'package:cardpay/src/presentation/widgets/boxes/horizontal_padding.dart';
import 'package:cardpay/src/presentation/widgets/layout/root_layout.dart';
import 'package:cardpay/src/presentation/widgets/loadings/overlay_loading.dart';
import 'package:cardpay/src/presentation/widgets/navigations/top_navigation.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_hooks/flutter_hooks.dart';

class AuthLayout extends HookWidget {
  final Widget child;
  final bool showBackButton;

  const AuthLayout({
    super.key,
    required this.child,
    this.showBackButton = true,
  });

  @override
  Widget build(BuildContext context) {
    return RootLayout(
      child: Scaffold(
        resizeToAvoidBottomInset: true,
        body: SafeArea(
          child: SingleChildScrollView(
            child: Stack(
              children: [
                PaddingHorizontal(slab: 3, child: child),
                BlocBuilder<LoginCubit, LoginState>(
                  builder: (_, state) {
                    switch (state.runtimeType) {
                      case LoginLoading:
                        return const OverlayLoading();
                      default:
                        return const SizedBox();
                    }
                  },
                ),
                BlocBuilder<SignupCubit, SignupState>(
                  builder: (_, state) {
                    switch (state.runtimeType) {
                      case SignupLoading:
                        return const OverlayLoading();
                      default:
                        return const SizedBox();
                    }
                  },
                ),
                if (showBackButton)
                  const PaddingHorizontal(
                    slab: 2,
                    child: Header(
                      color: AppColors.blackColor,
                    ),
                  ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
