import 'package:cardpay/src/config/router/app_router.dart';
import 'package:cardpay/src/config/screen_utills/box_decoration_all.dart';
import 'package:cardpay/src/config/themes/colors.dart';
import 'package:cardpay/src/presentation/cubits/remote/checkpoints_cubit.dart';
import 'package:cardpay/src/presentation/cubits/remote/login_cubit.dart';
import 'package:cardpay/src/presentation/widgets/actions/button/primary_button.dart';
import 'package:cardpay/src/presentation/widgets/boxes/horizontal_padding.dart';
import 'package:cardpay/src/presentation/widgets/boxes/verticle_padding.dart';
import 'package:cardpay/src/presentation/widgets/containment/cards/greeting_card.dart';
import 'package:cardpay/src/presentation/widgets/loadings/circle_list_item_loading.dart';
import 'package:cardpay/src/presentation/widgets/loadings/shimmer_loading.dart';
import 'package:cardpay/src/presentation/widgets/navigations/drawer_navigation.dart';
import 'package:cardpay/src/utils/constants/payment_strings.dart';
import 'package:cardpay/src/utils/constants/auth_strings.dart';
import 'package:flutter/material.dart';
import 'package:cardpay/src/presentation/cubits/remote/user_cubit.dart';
import 'package:cardpay/src/presentation/widgets/boxes/all_padding.dart';
import 'package:cardpay/src/presentation/widgets/boxes/height_box.dart';
import 'package:auto_route/auto_route.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_hooks/flutter_hooks.dart';

class ProfileItem {
  final IconData icon;
  final String text;
  final PageRouteInfo<dynamic> route;

  const ProfileItem(
      {required this.icon, required this.text, required this.route});
}

@RoutePage()
class ProfileView extends HookWidget {
  ProfileView({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final loginCubit = BlocProvider.of<LoginCubit>(context);
    final checkpointsCubit = BlocProvider.of<CheckpointsCubit>(context);

    void handleLogout() {
      loginCubit.logout();
    }

    void _showBottomSheetDelete() {
      showModalBottomSheet(
        context: context,
        builder: (context) {
          return Container(
            child: PaddingAll(
              slab: 2,
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Text(
                    AppStrings.deleteAccount,
                    style: AppTypography.mainHeading,
                    textAlign: TextAlign.center,
                  ),
                  HeightBox(slab: 2),
                  Text(
                    AppStrings.deleteAccountDesc,
                    textAlign: TextAlign.center,
                  ),
                  HeightBox(slab: 2),
                  Container(
                    child: Center(
                      child: PrimaryButton(
                        color: AppColors.redColor,
                        text: AppStrings.deleteAccount,
                        onPressed: handleLogout,
                      ),
                    ),
                  ),
                ],
              ),
            ),
          );
        },
      );
    }

    return Scaffold(
      body: PaddingHorizontal(
        slab: 1,
        child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          const HeightBox(slab: 5),
          Text(
            PaymentStrings.profile,
            style: AppTypography.mainHeading,
          ),
          const HeightBox(slab: 1),
          Container(
            decoration: CustomBoxDecorationAll.getDecoration(),
            width: double.infinity,
            child: PaddingAll(
              slab: 1,
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  BlocBuilder<UserCubit, UserState>(
                    builder: (_, state) {
                      switch (state.runtimeType) {
                        case UserLoading:
                          return const ShimmerLoading(
                            child: CircleListItemLoading(),
                          );
                        case UserSuccess || UserInitial:
                          return GestureDetector(
                            onTap: () {
                              // context.router.push(
                              //   EditProfileRoute(),
                              // );
                            },
                            child: PaddingBoxVertical(
                              slab: 1,
                              child: GreetingRow(
                                textColor: AppColors.secondaryColor,
                                name: state.user.fullName,
                                size: 16,
                                imagePath: 'assets/images/talha.jpg',
                              ),
                            ),
                          );
                        default:
                          return const SizedBox.shrink();
                      }
                    },
                  ),
                ],
              ),
            ),
          ),
          const HeightBox(slab: 3),
          Container(
              decoration: CustomBoxDecorationAll.getDecoration(
                color: AppColors.secondaryColor,
              ),
              child: Column(
                children: [
                  BlocListener<LoginCubit, LoginState>(
                    listener: (_, state) {
                      switch (state.runtimeType) {
                        case LogoutSuccess:
                          checkpointsCubit.init();
                          WidgetsBinding.instance.addPostFrameCallback((_) {
                            context.router.pushAndPopUntil(
                              const IntroRoute(),
                              predicate: (route) => false,
                            );
                          });
                          break;
                      }
                    },
                    child: const SizedBox.shrink(),
                  ),
                  const HeightBox(slab: 1),
                  // const CustomListTile(
                  //   iconColor: AppColors.primaryColor,
                  //   textColor: AppColors.blackColor,
                  //   icon: Icons.person,
                  //   text: PaymentStrings.personalDetails,
                  //   subText: PaymentStrings.personalDetailsDescription,
                  //   iconEnd: Icons.arrow_forward_ios,
                  // ),
                  // const CustomListTile(
                  //   iconColor: AppColors.primaryColor,
                  //   textColor: AppColors.blackColor,
                  //   icon: Icons.notifications,
                  //   text: PaymentStrings.notification,
                  //   subText: PaymentStrings.notificationDescription,
                  //   iconEnd: Icons.arrow_forward_ios,
                  // ),
                  // const CustomListTile(
                  //   iconColor: AppColors.primaryColor,
                  //   textColor: AppColors.blackColor,
                  //   icon: Icons.privacy_tip_rounded,
                  //   text: PaymentStrings.privacyPolicy,
                  //   subText: PaymentStrings.privacyPolicyDescription,
                  //   iconEnd: Icons.arrow_forward_ios,
                  // ),
                  CustomListTile(
                    iconColor: AppColors.primaryColor,
                    textColor: AppColors.blackColor,
                    icon: Icons.delete,
                    text: PaymentStrings.delete,
                    subText: PaymentStrings.deleteDescription,
                    iconEnd: Icons.arrow_forward_ios,
                    onTap: _showBottomSheetDelete,
                  ),
                  CustomListTile(
                    iconColor: AppColors.primaryColor,
                    textColor: AppColors.blackColor,
                    icon: Icons.logout,
                    text: PaymentStrings.logout,
                    subText: PaymentStrings.logoutDescription,
                    iconEnd: Icons.arrow_forward_ios,
                    onTap: handleLogout,
                  ),
                  const HeightBox(slab: 1)
                ],
              ))
        ]),
      ),
    );
  }
}
