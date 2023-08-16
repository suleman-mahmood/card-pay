import 'package:cardpay/src/config/router/app_router.dart';
import 'package:cardpay/src/config/screen_utills/box_decoration_all.dart';
import 'package:cardpay/src/config/themes/colors.dart';
import 'package:cardpay/src/presentation/widgets/actions/button/primary_button.dart';
import 'package:cardpay/src/presentation/widgets/boxes/horizontal_padding.dart';
import 'package:cardpay/src/presentation/widgets/boxes/width_between.dart';
import 'package:cardpay/src/presentation/widgets/containment/cards/greeting_card.dart';
import 'package:cardpay/src/presentation/widgets/layout/profile_layout.dart';
import 'package:cardpay/src/presentation/widgets/loadings/circle_list_item_loading.dart';
import 'package:cardpay/src/presentation/widgets/loadings/shimmer_loading.dart';
import 'package:cardpay/src/presentation/widgets/navigations/drawer_navigation.dart';
import 'package:cardpay/src/utils/constants/event_codes.dart';
import 'package:cardpay/src/utils/constants/payment_string.dart';
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
    final userCubit = BlocProvider.of<UserCubit>(context);
    final isLoading = true;
    // useEffect(() {
    //   someFunction() async {
    //     await userCubit.getUser();
    //   }

    //   someFunction();
    // }, []);
    void handleLogout() async {
      await userCubit.logout();
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
                    'Delete Account',
                    style: AppTypography.mainHeading,
                    textAlign: TextAlign.center,
                  ),
                  HeightBox(slab: 2),
                  Text(
                    'Are you sure you want to delete your account Permanently? This action cannot be undone.',
                    textAlign: TextAlign.center,
                  ),
                  HeightBox(slab: 2),
                  Container(
                    child: Center(
                      child: PrimaryButton(
                        color: AppColors.redColor,
                        text: 'Delete Account',
                        onPressed: () {
                          handleLogout();
                        },
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
      body: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
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
            slab: 2,
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                BlocBuilder<UserCubit, UserState>(
                  builder: (_, state) {
                    switch (state.runtimeType) {
                      case UserLoading:
                        return ShimmerLoading(
                          isLoading: isLoading,
                          child: CircleListItemLoading(),
                        );
                      case UserSuccess || UserInitial:
                        return GestureDetector(
                          onTap: () {
                            context.router.push(
                              EditProfileRoute(),
                            );
                          },
                          child: GreetingRow(
                            textColor: AppColors.secondaryColor,
                            name: state.user.fullName,
                            imagePath: 'assets/images/talha.jpg',
                          ),
                        );
                      case UserFailed:
                        return Text(
                          state.error!.response!.data['message'],
                          style: const TextStyle(color: Colors.red),
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
        Column(
          children: [
            BlocBuilder<UserCubit, UserState>(builder: (_, state) {
              switch (state.runtimeType) {
                case UserSuccess:
                  if (state.eventCodes == EventCodes.LOGOUT_SUCCESSFUL) {
                    WidgetsBinding.instance.addPostFrameCallback((_) {
                      context.router.pushAndPopUntil(
                        const IntroRoute(),
                        predicate: (route) => false,
                      );
                    });
                  }
                  return const SizedBox.shrink();
                default:
                  return const SizedBox.shrink();
              }
            }),
            Container(
              width: double.infinity,
              decoration: CustomBoxDecorationAll.getDecoration(
                color: AppColors.secondaryColor,
              ),
              child: CustomListTile(
                icon: Icons.logout,
                text: 'Log Out',
                subText: 'Secure Your Account for safety',
                iconEnd: Icons.arrow_forward_ios,
                onTap: handleLogout,
              ),
            ),
            const HeightBox(slab: 2),
            Container(
              width: double.infinity,
              decoration: CustomBoxDecorationAll.getDecoration(
                color: AppColors.redColor,
              ),
              child: CustomListTile(
                icon: Icons.logout,
                text: 'Delete Account',
                subText: 'Permanently delete your data',
                iconEnd: Icons.arrow_forward_ios,
                onTap: _showBottomSheetDelete,
                textColor: AppColors.secondaryColor,
                iconColor: AppColors.secondaryColor,
                suffixIconColor: AppColors.secondaryColor,
              ),
            ),
          ],
        )
      ]),
    );
  }
}
