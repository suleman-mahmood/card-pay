import 'package:cardpay/src/config/themes/colors.dart';
import 'package:cardpay/src/presentation/widgets/boxes/width_between.dart';
import 'package:cardpay/src/utils/constants/payment_string.dart';
import 'package:flutter/material.dart';
import 'package:auto_route/auto_route.dart';
import 'package:cardpay/src/config/router/app_router.dart';
import 'package:flutter_hooks/flutter_hooks.dart';

class DrawerItem {
  final IconData icon;
  final String text;
  final PageRouteInfo<dynamic> route;

  const DrawerItem(
      {required this.icon, required this.text, required this.route});
}

const drawerItems = <DrawerItem>[
  DrawerItem(icon: Icons.home, text: 'Home', route: const SplashRoute()),
  DrawerItem(icon: Icons.history, text: 'History', route: const HistroyRoute()),
  DrawerItem(
      icon: Icons.show_chart, text: 'Charts', route: const DashboardRoute()),
  DrawerItem(
      icon: Icons.person, text: 'Profile', route: const ConfirmationRoute()),
  DrawerItem(
      icon: Icons.settings,
      text: 'Settings',
      route: const FilterHistoryRoute()),
];

class MyDrawer extends HookWidget {
  MyDrawer({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    var selectedRouteName = useState(drawerItems[0].route.routeName);

    return Drawer(
      child: Column(
        children: <Widget>[
          Container(
            height: 100,
            child: DrawerHeader(
              decoration: const BoxDecoration(
                  color: AppColors.secondaryColor, shape: BoxShape.rectangle),
              child: userInfo(context),
            ),
          ),
          for (var item in drawerItems)
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16.0),
              child: CustomListTile(
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
          Container(
            padding: const EdgeInsets.all(16.0),
            child: Row(
              children: [
                Icon(Icons.home, color: AppColors.greyColor),
                Text('Home', style: TextStyle(color: AppColors.greyColor)),
              ],
            ),
          )
        ],
      ),
    );
  }

  Widget userInfo(BuildContext context) {
    const String userName = PaymentStrings.fName;
    const String userEmail = PaymentStrings.email;
    return Padding(
      padding: const EdgeInsets.all(8.0),
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
              Text(userName, style: AppTypography.bodyTextBold),
              Text(userEmail, style: AppTypography.subHeading),
            ],
          ),
        ],
      ),
    );
  }
}

class CustomListTile extends StatelessWidget {
  final IconData icon;
  final String text;
  final Function()? onTap;
  final bool selected;

  const CustomListTile({
    Key? key,
    required this.icon,
    required this.text,
    this.onTap,
    this.selected = false,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final color = selected ? AppColors.secondaryColor : AppColors.greyColor;
    final decoration = BoxDecoration(
      color: selected ? AppColors.primaryColor : null,
      borderRadius: BorderRadius.circular(20.0),
    );

    return InkWell(
      onTap: onTap,
      child: Container(
        padding: EdgeInsets.all(8.0),
        decoration: decoration,
        child: ListTile(
          leading: Icon(icon, color: color),
          title: Text(text, style: TextStyle(color: color)),
        ),
      ),
    );
  }
}
