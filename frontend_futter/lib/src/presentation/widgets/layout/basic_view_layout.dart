import 'package:cardpay/src/presentation/widgets/boxes/height_box.dart';
import 'package:cardpay/src/presentation/widgets/boxes/horizontal_padding.dart';
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

  BasicViewLayout({
    Key? key,
    required this.headerTitle,
    required this.backgroundColor,
    required this.children,
    this.centered = true,
    this.headerColor = AppColors.secondaryColor,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    Widget shouldCenter({required Widget child}) {
      if (centered) {
        return Center(child: child);
      }
      return child;
    }
    return Scaffold(
      resizeToAvoidBottomInset: true,
      backgroundColor: backgroundColor,
      body: SafeArea(
        child: Column(          
          children: [
             PaddingHorizontal(
              slab: 2,
              child: Header(title: headerTitle, color: headerColor),
            ),
            shouldCenter(
                child: PaddingHorizontal(
                  slab: 2,
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
    );
  }
}