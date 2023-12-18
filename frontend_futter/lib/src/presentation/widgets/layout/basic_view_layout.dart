import 'package:cardpay/src/presentation/widgets/boxes/height_box.dart';
import 'package:cardpay/src/presentation/widgets/boxes/horizontal_padding.dart';
import 'package:cardpay/src/presentation/widgets/layout/root_layout.dart';
import 'package:cardpay/src/presentation/widgets/navigations/top_navigation.dart';
import 'package:flutter/material.dart';
import 'package:cardpay/src/config/themes/colors.dart';
import 'package:flutter_hooks/flutter_hooks.dart';

class BasicViewLayout extends HookWidget {
  final String headerTitle;
  final Color backgroundColor;
  final List<Widget> children;
  final bool centered;
  final Color headerColor;

  final bool horizontalPadding;
  final bool bottomSafeArea;
  final MainAxisAlignment mainAxisAlignment;

  BasicViewLayout({
    Key? key,
    required this.headerTitle,
    required this.backgroundColor,
    required this.children,
    this.centered = true,
    this.headerColor = AppColors.secondaryColor,
    this.horizontalPadding = true,
    this.bottomSafeArea = true,
    this.mainAxisAlignment = MainAxisAlignment.start,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    Widget shouldCenter({required Widget child}) {
      if (centered) {
        return Center(child: child);
      }
      return child;
    }

    Widget shouldHorizontalPadding({required Widget child}) {
      if (horizontalPadding) {
        return PaddingHorizontal(slab: 2, child: child);
      }
      return child;
    }

    return RootLayout(
      child: Scaffold(
        resizeToAvoidBottomInset: true,
        backgroundColor: backgroundColor,
        body: SafeArea(
          bottom: bottomSafeArea,
          child: Column(
            mainAxisAlignment: mainAxisAlignment,
            children: [
              PaddingHorizontal(
                slab: 2,
                child: Header(title: headerTitle, color: headerColor),
              ),
              shouldCenter(
                child: shouldHorizontalPadding(
                  child: SingleChildScrollView(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Visibility(
                          visible: !centered,
                          child: const HeightBox(slab: 6),
                        ),
                        ...children,
                      ],
                    ),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
