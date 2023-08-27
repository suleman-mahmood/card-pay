import 'package:cardpay/src/config/themes/colors.dart';
import 'package:cardpay/src/presentation/widgets/boxes/horizontal_padding.dart';
import 'package:cardpay/src/presentation/cubits/remote/user_cubit.dart';
import 'package:cardpay/src/presentation/widgets/loadings/overlay_loading.dart';
import 'package:cardpay/src/presentation/widgets/navigations/top_navigation.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_hooks/flutter_hooks.dart';

class AuthLayout extends HookWidget {
  final Widget child;
  bool showBackButton = true;
  AuthLayout({
    super.key,
    required this.child,
    this.showBackButton = true,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      resizeToAvoidBottomInset: true,
      body: SafeArea(
        child: SingleChildScrollView(
          child: Stack(
            children: [
              PaddingHorizontal(slab: 3, child: child),
              BlocBuilder<UserCubit, UserState>(
                builder: (_, state) {
                  switch (state.runtimeType) {
                    case UserLoading:
                      return const OverlayLoading();
                    default:
                      return const SizedBox();
                  }
                },
              ),
              if (showBackButton)
                PaddingHorizontal(
                  slab: 2,
                  child: Header(
                    // title: AppStrings.logIn,
                    color: AppColors.blackColor,
                  ),
                ),
            ],
          ),
        ),
      ),
    );
  }
}
