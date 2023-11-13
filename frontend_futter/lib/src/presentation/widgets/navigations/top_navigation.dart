import 'package:cardpay/src/presentation/widgets/boxes/height_box.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import 'package:auto_route/auto_route.dart';
import 'package:cardpay/src/config/screen_utills/screen_util.dart';
import 'package:cardpay/src/config/themes/colors.dart';
import 'package:flutter_hooks/flutter_hooks.dart';

class Header extends HookWidget {
  final String? title;
  final Color color;
  final bool showBackButton;
  final bool showMainHeading;
  final String? mainHeadingText;
  final bool? removeTopPadding;
  final bool logoutOnBack;

  const Header({
    super.key,
    this.showBackButton = true,
    this.title,
    this.color = AppColors.secondaryColor,
    this.showMainHeading = false,
    this.removeTopPadding,
    this.mainHeadingText,
    this.logoutOnBack = false,
  });

  @override
  Widget build(BuildContext context) {
    final double horizontalPadding = ScreenUtil.blockSizeHorizontal(context);
    final double verticalPadding = ScreenUtil.blockSizeVertical(context);
    Widget BackButton(color) => IconButton(
          icon: Icon(
            Icons.arrow_back,
            color: color,
            size: 30,
          ),
          onPressed: () => context.router.pop(),
        );
    Widget LogoutButton(color) => IconButton(
          icon: Icon(
            Icons.logout,
            color: color,
            size: 30,
          ),
          onPressed: FirebaseAuth.instance.signOut,
        );

    return Column(
      children: [
        removeTopPadding ?? false
            ? Row(
                mainAxisAlignment: logoutOnBack
                    ? MainAxisAlignment.end
                    : MainAxisAlignment.start,
                children: [
                  if (showBackButton)
                    logoutOnBack ? LogoutButton(color) : BackButton(color),
                  if (title != null)
                    Text(
                      title!,
                      style: AppTypography.mainHeading.copyWith(
                          color: color, decoration: TextDecoration.none),
                    ),
                ],
              )
            : Padding(
                padding: EdgeInsets.fromLTRB(
                  horizontalPadding * 0,
                  verticalPadding * 2,
                  horizontalPadding * 0,
                  verticalPadding * 4,
                ),
                child: Row(
                  mainAxisAlignment: logoutOnBack
                      ? MainAxisAlignment.end
                      : MainAxisAlignment.start,
                  children: [
                    if (showBackButton)
                      logoutOnBack ? LogoutButton(color) : BackButton(color),
                    if (title != null)
                      Text(
                        title!,
                        style: AppTypography.mainHeading.copyWith(
                            color: color, decoration: TextDecoration.none),
                      ),
                  ],
                ),
              ),
        HeightBox(slab: 2),
        if (showMainHeading && mainHeadingText != null)
          Text(
            mainHeadingText!,
            style: AppTypography.mainHeading.copyWith(
                color: AppColors.secondaryColor,
                decoration: TextDecoration.none),
            textAlign: TextAlign.center,
          ),
      ],
    );
  }
}
