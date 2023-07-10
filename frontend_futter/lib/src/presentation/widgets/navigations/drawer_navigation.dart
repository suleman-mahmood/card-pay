import 'package:flutter/material.dart';
import 'package:auto_route/auto_route.dart';
import 'package:frontend_futter/src/config/router/app_router.dart';
import 'package:frontend_futter/src/config/screen_utills/screen_util.dart';
import 'package:flutter_hooks/flutter_hooks.dart';

class DrawerItem {
  final IconData icon;
  final String text;
  final PageRouteInfo<dynamic> route;

  DrawerItem({required this.icon, required this.text, required this.route});
}

class MyDrawer extends HookWidget {
  final List<DrawerItem> drawerItems = [
    DrawerItem(icon: Icons.home, text: 'Home', route: const SplashRoute()),
    DrawerItem(
        icon: Icons.history, text: 'History', route: const HistroyRoute()),
    DrawerItem(
        icon: Icons.show_chart, text: 'Charts', route: const DashboardRoute()),
    DrawerItem(
        icon: Icons.person, text: 'Profile', route: const ConfirmationRoute()),
    DrawerItem(
        icon: Icons.settings,
        text: 'Settings',
        route: const FilterHistoryRoute()),
  ];

  MyDrawer({super.key});

  @override
  Widget build(BuildContext context) {
    return Drawer(
      child: ListView(
        padding: EdgeInsets.zero,
        children: <Widget>[
          DrawerHeader(
            decoration: const BoxDecoration(
              color: Colors.white,
            ),
            child: userInfo(context),
          ),
          for (var item in drawerItems)
            CustomListTile(
              leading: Icon(item.icon, color: Colors.black),
              title:
                  Text(item.text, style: const TextStyle(color: Colors.black)),
              onTap: () => context.router.push(item.route),
            ),
          SizedBox(height: ScreenUtil.heightMultiplier(context) * 30),
        ],
      ),
    );
  }

  Widget userInfo(BuildContext context) {
    return Row(
      children: [
        CircleAvatar(
          backgroundColor: Colors.blue,
          child: Text(
            'T',
            style: TextStyle(fontSize: ScreenUtil.textMultiplier(context) * 4),
          ),
        ),
        SizedBox(width: ScreenUtil.widthMultiplier(context) * 2),
        Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              'Talha',
              style: TextStyle(
                  color: Colors.black,
                  fontSize: ScreenUtil.textMultiplier(context) * 1.8),
            ),
            const Text(
              '24100245example.com',
              style: TextStyle(color: Colors.black),
            ),
          ],
        ),
      ],
    );
  }
}

class CustomListTile extends StatelessWidget {
  final Widget leading;
  final Widget title;
  final Function()? onTap;

  const CustomListTile({
    Key? key,
    required this.leading,
    required this.title,
    this.onTap,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: onTap,
      child: ListTile(
        leading: leading,
        title: title,
      ),
    );
  }
}
