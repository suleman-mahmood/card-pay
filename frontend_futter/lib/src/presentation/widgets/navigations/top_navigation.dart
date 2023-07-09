import 'package:flutter/material.dart';
import 'package:auto_route/auto_route.dart';
import 'package:frontend_futter/src/config/screen_utills/screen_util.dart';
import 'package:frontend_futter/src/config/themes/colors.dart';
import 'package:flutter_hooks/flutter_hooks.dart';

class Header extends HookWidget {
  final String title;
  final Color color;
  final bool showMainHeading;
  final String? mainHeadingText;

  const Header({super.key, 
    required this.title,
    this.color = AppColors.secondaryColor,
    this.showMainHeading = false,
    this.mainHeadingText,
  });

  @override
  Widget build(BuildContext context) {
    final double horizontalPadding = ScreenUtil.blockSizeHorizontal(context);
    final double verticalPadding = ScreenUtil.blockSizeVertical(context);

    return Column(
      children: [
        Padding(
          padding: EdgeInsets.fromLTRB(
            horizontalPadding, // left
            verticalPadding * 2, // top
            horizontalPadding * 9, // right
            verticalPadding * 3, // bottom
          ),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              _BackButton(color: color),
              Center(
                child: Text(
                  title,
                  style: AppTypography.mainHeading.copyWith(color: color),
                ),
              ),
              const Spacer(),
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

class _BackButton extends StatelessWidget {
  final Color color;

  const _BackButton({required this.color});

  @override
  Widget build(BuildContext context) {
    return IconButton(
      icon: Icon(Icons.arrow_back, color: color),
      onPressed: () => context.router.pop(),
    );
  }
}
