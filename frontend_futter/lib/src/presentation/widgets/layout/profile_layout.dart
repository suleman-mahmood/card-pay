import 'package:cardpay/src/presentation/widgets/boxes/all_padding.dart';
import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';

class ProfileLayout extends HookWidget {
  final Widget child;

  ProfileLayout({
    Key? key,
    required this.child,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      resizeToAvoidBottomInset: true,
      body: SafeArea(
        child: SingleChildScrollView(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              SizedBox(height: 40),
              PaddingAll(
                slab: 2,
                child: child,
              ),
            ],
          ),
        ),
      ),
    );
  }
}
