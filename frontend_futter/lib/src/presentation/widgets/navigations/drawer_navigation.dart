import 'package:cardpay/src/config/themes/colors.dart';
import 'package:cardpay/src/presentation/cubits/remote/user_cubit.dart';
import 'package:cardpay/src/presentation/widgets/boxes/all_padding.dart';
import 'package:cardpay/src/presentation/widgets/boxes/padding_box.dart';
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
                  color: AppColors.secondaryColor, shape: BoxShape.rectangle),
              child: userInfo(context),
            ),
          ),
          for (var item in drawerItems)
            PaddingHorizontal(
              slab: 2,
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
          // Container(
          //   padding: const EdgeInsets.all(16.0),
          //   child: Row(
          //     children: [
          //       Icon(
          //         Icons.add_circle_outlined,
          //         color: AppColors.greyColor,
          //       ),
          //       WidthBetween(),
          //       Text(
          //         'Register loop',
          //         style: TextStyle(color: AppColors.greyColor),
          //       ),
          //     ],
          //   ),
          // )
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
