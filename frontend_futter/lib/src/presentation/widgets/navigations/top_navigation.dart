import 'package:cardpay/src/presentation/widgets/boxes/width_between.dart';
import 'package:flutter/material.dart';
import 'package:auto_route/auto_route.dart';
import 'package:cardpay/src/config/screen_utills/screen_util.dart';
import 'package:cardpay/src/config/themes/colors.dart';
import 'package:flutter_hooks/flutter_hooks.dart';

class Header extends HookWidget {
  final String title;
  final Color color;
  final bool showMainHeading;
  final String? mainHeadingText;
  final bool? removeTopPadding;

  const Header({
    super.key,
    required this.title,
    this.color = AppColors.secondaryColor,
    this.showMainHeading = false,
    this.removeTopPadding,
    this.mainHeadingText,
  });

  @override
  Widget build(BuildContext context) {
    final double horizontalPadding = ScreenUtil.blockSizeHorizontal(context);
    final double verticalPadding = ScreenUtil.blockSizeVertical(context);
    Widget BackButton(color) => IconButton(
          icon: Icon(Icons.arrow_back, color: color, size: 40),
          onPressed: () => context.router.pop(),
        );

    return Column(
      children: [
        removeTopPadding ?? false
            ? Row(
                // mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  BackButton(color),
                  WidthArrowBetween(),
                  Text(
                    title,
                    style: AppTypography.mainHeading.copyWith(color: color),
                  ),
                  // BackButton(Colors.transparent),
                ],
              )
            : Padding(
                padding: EdgeInsets.fromLTRB(
                  horizontalPadding * 1,
                  verticalPadding * 5,
                  horizontalPadding * 9,
                  verticalPadding * 3,
                ),
                child: Row(
                  // mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    BackButton(color),
                    WidthArrowBetween(),
                    Text(
                      title,
                      style: AppTypography.mainHeading.copyWith(color: color),
                    ),
                    // BackButton(Colors.transparent),
                  ],
                ),
              ),
        if (showMainHeading && mainHeadingText != null)
          Text(
            mainHeadingText!,
            style: AppTypography.mainHeading
                .copyWith(color: AppColors.secondaryColor),
            textAlign: TextAlign.center,
          ),
      ],
    );
  }
}
