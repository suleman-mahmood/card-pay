import 'package:cardpay/src/config/screen_utills/box_shadow.dart';
import 'package:cardpay/src/presentation/widgets/boxes/horizontal_padding.dart';
import 'package:cardpay/src/presentation/widgets/navigations/top_navigation.dart';
import 'package:flutter/material.dart';
import 'package:auto_route/auto_route.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:cardpay/src/config/themes/colors.dart';

@RoutePage()
class FaqsView extends HookWidget {
  const FaqsView({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.purpleColor,
      body: Stack(
        children: [
          Align(
            alignment: Alignment.bottomCenter,
            child: Container(
              decoration: CustomBoxDecoration.getDecoration(),
              child: const Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  // HeightBox(slab: 3),
                  // Text('Woah super important questions'),
                  // HeightBox(slab: 5),
                ],
              ),
            ),
          ),
          const PaddingHorizontal(slab: 2, child: Header(title: "FAQs")),
        ],
      ),
    );
  }
}
