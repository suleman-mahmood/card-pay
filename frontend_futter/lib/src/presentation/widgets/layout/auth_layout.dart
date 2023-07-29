import 'package:cardpay/src/presentation/widgets/boxes/padding_box.dart';
import 'package:cardpay/src/presentation/cubits/remote/user_cubit.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_hooks/flutter_hooks.dart';

class AuthLayout extends HookWidget {
  final Widget child;

  AuthLayout({
    super.key,
    required this.child,
  });

  @override
  Widget build(BuildContext context) {
    Widget _buildLoader() {
      return SizedBox(
        height: MediaQuery.of(context).size.height -
            MediaQuery.of(context).padding.top,
        width: MediaQuery.of(context).size.width,
        child: Stack(
          children: [
            Container(
              color: Colors.grey.withOpacity(0.6),
            ),
            const Center(
              child: CircularProgressIndicator(),
            ),
          ],
        ),
      );
    }

    return Scaffold(
      resizeToAvoidBottomInset: true,
      body: SafeArea(
        child: SingleChildScrollView(
          child: Stack(
            children: [
              PaddingHorizontal(slab: 3, child: child),
              BlocBuilder<UserCubit, UserState>(builder: (_, state) {
                switch (state.runtimeType) {
                  case UserLoading:
                    return _buildLoader();
                  default:
                    return const SizedBox();
                }
              }),
            ],
          ),
        ),
      ),
    );
  }
}
