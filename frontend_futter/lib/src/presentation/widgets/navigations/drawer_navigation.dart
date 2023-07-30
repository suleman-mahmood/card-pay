import 'package:cardpay/src/config/themes/colors.dart';
import 'package:cardpay/src/presentation/cubits/remote/user_cubit.dart';
import 'package:cardpay/src/presentation/widgets/boxes/all_padding.dart';
import 'package:cardpay/src/presentation/widgets/boxes/horizontal_padding.dart';
import 'package:cardpay/src/presentation/widgets/boxes/width_between.dart';
import 'package:flutter/material.dart';
import 'package:auto_route/auto_route.dart';
import 'package:cardpay/src/config/router/app_router.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_hooks/flutter_hooks.dart';

class DrawerItem {
  final IconData icon;
  final String text;
  final PageRouteInfo<dynamic> route;

  const DrawerItem(
      {required this.icon, required this.text, required this.route});
}

class MyDrawer extends HookWidget {
  MyDrawer({Key? key}) : super(key: key);

  final List<DrawerItem> drawerItems = [
    DrawerItem(icon: Icons.home, text: 'Home', route: PaymentDashboardRoute()),
    DrawerItem(
      icon: Icons.phone_outlined,
      text: 'Help',
      route: PaymentDashboardRoute(),
    ),
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
    var selectedRouteName = useState(drawerItems[0].route.routeName);

    return Drawer(
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
            PaddingAll(
              slab: 1,
              child: CustomListTile(
                backgroundColor: AppColors.primaryColor,
                textColor: AppColors.secondaryColor,
                iconColor: AppColors.greyColor,
                icon: item.icon,
                text: item.text,
                onTap: () {
                  context.router.push(item.route);
                  selectedRouteName.value = item.route.routeName;
                },
                selected: selectedRouteName.value == item.route.routeName,
              ),
            ),
          Expanded(
            child: SizedBox(),
          ),
          GestureDetector(
            onTap: () => {context.router.push(const RegisterRoute())},
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
                    'Register loop',
                    style: TextStyle(color: AppColors.greyColor),
                  ),
                ],
              ),
            ),
          )
        ],
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
          CircleAvatar(
            backgroundImage: AssetImage('assets/images/talha.jpg'),
            radius: 30,
          ),
          WidthBetween(),
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
    this.iconColor = AppColors.primaryColor,
    this.textColor = AppColors.blackColor,
    this.backgroundColor = AppColors.greyColor,
    this.subTextColor = AppColors.greyColor,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final color = selected ? subTextColor : textColor;
    final decoration = BoxDecoration(
      color: selected ? backgroundColor : null,
      borderRadius: BorderRadius.circular(20.0),
    );

    return InkWell(
      onTap: onTap,
      child: Container(
        // margin: EdgeInsets.symmetric(vertical: 2.0),
        padding: EdgeInsets.all(8.0),
        decoration: decoration,
        child: ListTile(
          leading: Icon(
            icon,
            color: iconColor,
          ),
          title: Text(
            text,
            style: AppTypography.mainHeading
                .copyWith(fontSize: 20, color: textColor),
          ),
          subtitle: subText != null
              ? Text(
                  subText!,
                  style: TextStyle(color: color),
                )
              : null,
          trailing: iconEnd != null
              ? Icon(
                  iconEnd,
                  color: AppColors.greyColor,
                )
              : null,
        ),
      ),
    );
  }
}
