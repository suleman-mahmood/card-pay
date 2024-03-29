import 'dart:io';
import 'package:cardpay/src/config/themes/colors.dart';
import 'package:cardpay/src/presentation/cubits/remote/closed_loop_cubit.dart';
import 'package:cardpay/src/presentation/cubits/remote/user_cubit.dart';
import 'package:cardpay/src/presentation/widgets/boxes/all_padding.dart';
import 'package:cardpay/src/presentation/widgets/boxes/width_between.dart';
import 'package:cardpay/src/utils/constants/payment_strings.dart';
import 'package:flutter/material.dart';
import 'package:auto_route/auto_route.dart';
import 'package:cardpay/src/config/router/app_router.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:url_launcher/url_launcher.dart';

class DrawerItem {
  final IconData icon;
  final String text;
  final PageRouteInfo<dynamic>? route;
  final VoidCallback? onClick;

  const DrawerItem({
    required this.icon,
    required this.text,
    this.route,
    this.onClick,
  });
}

class MyDrawer extends HookWidget {
  MyDrawer({Key? key}) : super(key: key);

  final List<DrawerItem> drawerItems = [
    DrawerItem(
        icon: Icons.home,
        text: PaymentStrings.home,
        route: DashboardLayoutRoute()),
    DrawerItem(
        icon: Icons.phone_outlined,
        text: PaymentStrings.help,
        onClick: () {
          if (Platform.isIOS) {
            const whatsappUrl = 'https://wa.me/+923322208287';
            launchUrl(Uri.parse(whatsappUrl));
          } else if (Platform.isAndroid) {
            const whatsappUrl = 'whatsapp://send?phone=+923322208287';
            launchUrl(Uri.parse(whatsappUrl));
          }
        }),
    // DrawerItem(
    //     icon: Icons.history, text: 'History', route: const HistroyRoute()),
    // DrawerItem(icon: Icons.show_chart, text: 'Charts', route: DashboardRoute()),
    // DrawerItem(
    //     icon: Icons.person, text: 'Profile', route: const ConfirmationRoute()),
    // DrawerItem(
    //     icon: Icons.settings,
    //     text: 'Settings',
    //     route: const FilterHistoryRoute()),
  ];

  @override
  Widget build(BuildContext context) {
    final closedLoopCubit = BlocProvider.of<ClosedLoopCubit>(context);

    var selectedRouteName = useState(drawerItems[0].route?.routeName);

    return Drawer(
      child: Container(
        color: AppColors.secondaryColor,
        child: Column(
          children: <Widget>[
            Container(
              height: 150,
              child: DrawerHeader(
                decoration: const BoxDecoration(
                  color: AppColors.secondaryColor,
                  shape: BoxShape.rectangle,
                ),
                child: userInfo(context),
              ),
            ),
            for (var item in drawerItems)
              GestureDetector(
                child: PaddingAll(
                  slab: 1,
                  child: CustomListTile(
                    icon: item.icon,
                    text: item.text,
                    onTap: () {
                      if (item.route != null) {
                        if (context.routeData.name != item.route!.routeName) {
                          context.router.push(item.route!);
                        }
                        selectedRouteName.value = item.route!.routeName;
                      } else {
                        item.onClick!();
                      }
                    },
                    selected: selectedRouteName.value == item.route?.routeName,
                  ),
                ),
              ),
            const Expanded(child: SizedBox()),
            GestureDetector(
              onTap: () {
                closedLoopCubit.getAllClosedLoops();
                context.router.push(const ClosedLoopRoute());
              },
              child: Container(
                padding: const EdgeInsets.all(16.0),
                child: Row(
                  children: [
                    Icon(
                      Icons.add_circle_outlined,
                      color: AppColors.greyColor,
                    ),
                    WidthBetween(),
                    Text(
                      PaymentStrings.registerLoop,
                      style: TextStyle(color: AppColors.greyColor),
                    ),
                  ],
                ),
              ),
            )
          ],
        ),
      ),
    );
  }

  Widget userInfo(BuildContext context) {
    final userCubit = BlocProvider.of<UserCubit>(context);

    return PaddingAll(
      slab: 1,
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const CircleAvatar(
            backgroundImage: AssetImage('assets/images/talha.jpg'),
            radius: 30,
          ),
          const WidthBetween(),
          Column(
            children: [
              Text(
                userCubit.state.user.fullName,
                style: AppTypography.bodyTextBold,
              ),
              Text(
                userCubit.state.user.personalEmail,
                style: AppTypography.subHeading,
              ),
            ],
          ),
        ],
      ),
    );
  }
}

class CustomListTile extends HookWidget {
  final IconData icon;
  final String text;
  final String? subText;
  final IconData? iconEnd;
  final Color suffixIconColor;
  final Function()? onTap;
  final bool selected;

  final Color iconColor;
  final Color textColor;
  final Color backgroundColor;
  final Color subTextColor;

  const CustomListTile({
    Key? key,
    required this.icon,
    required this.text,
    this.iconEnd,
    this.subText,
    this.onTap,
    this.selected = false,
    this.iconColor = AppColors.greyColor,
    this.textColor = AppColors.greyColor,
    this.backgroundColor = AppColors.secondaryColor,
    this.subTextColor = AppColors.greyColor,
    this.suffixIconColor = AppColors.greyColor,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final Color finalBackgroundColor = selected ? Colors.blue : backgroundColor;
    final Color finalTextColor = selected ? Colors.white : textColor;
    return InkWell(
      onTap: onTap,
      child: Container(
        decoration: BoxDecoration(
          color: finalBackgroundColor,
          borderRadius: BorderRadius.circular(16),
        ),
        padding: EdgeInsets.all(8.0),
        child: ListTile(
          leading: CircleAvatar(
            backgroundColor:
                selected ? Colors.transparent : AppColors.lightGreyColor,
            child: Icon(
              icon,
              color: selected ? AppColors.secondaryColor : iconColor,
            ),
          ),
          title: Text(
            text,
            style: AppTypography.mainHeading.copyWith(
              fontSize: 20,
              color: finalTextColor,
            ),
          ),
          subtitle: subText != null
              ? Text(
                  subText!,
                  style: TextStyle(
                      color:
                          selected ? AppColors.secondaryColor : subTextColor),
                )
              : null,
          trailing: iconEnd != null
              ? Icon(
                  iconEnd,
                  color: selected ? AppColors.secondaryColor : suffixIconColor,
                )
              : null,
        ),
      ),
    );
  }
}
