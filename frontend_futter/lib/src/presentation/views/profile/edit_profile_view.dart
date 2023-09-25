// TODO: fix this when we are using it
import 'package:cardpay/src/config/router/app_router.dart';
import 'package:cardpay/src/config/themes/colors.dart';
import 'package:cardpay/src/presentation/cubits/remote/login_cubit.dart';
import 'package:cardpay/src/presentation/widgets/actions/button/primary_button.dart';
import 'package:cardpay/src/presentation/widgets/boxes/all_padding.dart';
import 'package:cardpay/src/presentation/widgets/boxes/height_box.dart';
import 'package:cardpay/src/presentation/widgets/boxes/horizontal_padding.dart';
import 'package:cardpay/src/presentation/widgets/layout/profile_layout.dart';
import 'package:cardpay/src/presentation/widgets/navigations/top_navigation.dart';
import 'package:cardpay/src/presentation/widgets/selections/phonenumber_drop_down.dart';
import 'package:cardpay/src/presentation/widgets/text_inputs/input_field.dart';
import 'package:cardpay/src/utils/constants/payment_strings.dart';
import 'package:cardpay/src/utils/constants/auth_strings.dart';
import 'package:flutter/material.dart';
import 'package:auto_route/auto_route.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_hooks/flutter_hooks.dart';

@RoutePage()
class EditProfileView extends HookWidget {
  const EditProfileView({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final loginCubit = BlocProvider.of<LoginCubit>(context);

    void handleLogout() async {
      await loginCubit.logout();
    }

    Widget _buildAvatarWidget(String url) {
      return CircleAvatar(
        radius: 12,
        backgroundImage: NetworkImage(url),
      );
    }

    final dropdownValue = useState<String>(AppStrings.defaultCountryCode);
    final phoneNumberController = useTextEditingController();

    void _showBottomSheetAvatar() {
      final modalContext = context;

      showModalBottomSheet(
        context: context,
        builder: (context) {
          List<String> avatarUrls = [
            'https://via.placeholder.com/100',
            'https://via.placeholder.com/100',
            'https://via.placeholder.com/100',
            'https://via.placeholder.com/100',
            'https://via.placeholder.com/100',
            'https://via.placeholder.com/100',
            'https://via.placeholder.com/100',
            'https://via.placeholder.com/100',
            'https://via.placeholder.com/100',
            'https://via.placeholder.com/100',
          ];

          return Container(
            child: PaddingAll(
              slab: 2,
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                mainAxisSize: MainAxisSize.min,
                children: [
                  Text(
                    'Choose Profile Avatar',
                    style: AppTypography.mainHeading,
                    textAlign: TextAlign.center,
                  ),
                  HeightBox(slab: 2),
                  Text(
                    'Select an avatar from the options below:',
                    textAlign: TextAlign.center,
                  ),
                  HeightBox(slab: 2),
                  GridView.builder(
                    shrinkWrap: true,
                    gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
                      crossAxisCount: 5,
                      crossAxisSpacing: 8.0,
                      mainAxisSpacing: 8.0,
                    ),
                    itemCount: avatarUrls.length,
                    itemBuilder: (context, index) {
                      return _buildAvatarWidget(avatarUrls[index]);
                    },
                  ),
                  HeightBox(slab: 2),
                  Center(
                    child: PrimaryButton(
                      text: AppStrings.createAccount,
                      onPressed: () {},
                    ),
                  ),
                ],
              ),
            ),
          );
        },
      );
    }

    void onPhoneNumberChanged(String newValue) {
      dropdownValue.value = newValue;
    }

    void _showOTPBottomSheetProfile() {
      final modalContext = context;
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
                    'Change Password',
                    style: AppTypography.mainHeading,
                    textAlign: TextAlign.center,
                  ),
                  HeightBox(slab: 2),
                  Text(
                    'Please update your passward',
                    textAlign: TextAlign.center,
                  ),
                  HeightBox(slab: 2),
                  CustomInputField(
                    label: AppStrings.password,
                    hint: AppStrings.enterPassword,
                    obscureText: true,
                    validator: (passwordValue) {
                      if (passwordValue == null) {
                        return "Please enter your password";
                      }
                      return null;
                    },
                  ),
                  CustomInputField(
                    label: 'Retype Password',
                    hint: AppStrings.enterPassword,
                    obscureText: true,
                    validator: (passwordValue) {
                      if (passwordValue == null) {
                        return "Please enter your password";
                      }
                      return null;
                    },
                  ),
                  HeightBox(slab: 2),
                  Center(
                    child: PrimaryButton(
                      text: 'Done',
                      onPressed: () {},
                    ),
                  ),
                ],
              ),
            ),
          );
        },
      );
    }

    void _showBottomSheetDelete() {
      final modalContext = context;

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
                  Column(
                    children: [
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
                  )
                ],
              ),
            ),
          );
        },
      );
    }

    return ProfileLayout(
      child: PaddingHorizontal(
        slab: 2,
        child: Stack(
          children: [
            Align(
              alignment: Alignment.bottomCenter,
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  HeightBox(slab: 5),
                  GestureDetector(
                    onTap: () {
                      _showBottomSheetAvatar();
                    },
                    child: Center(
                      child: Stack(children: [
                        CircleAvatar(
                          radius: 40,
                          backgroundImage:
                              AssetImage('assets/images/talha.jpg'),
                        ),
                        Positioned(
                          bottom: 0,
                          right: 0,
                          child: Icon(
                            Icons.edit,
                            color: Colors.white,
                            size: 40,
                          ),
                        ),
                      ]),
                    ),
                  ),
                  const HeightBox(slab: 1),
                  CustomInputField(
                    label: AppStrings.username,
                    hint: AppStrings.enterUsername,
                    obscureText: false,
                    validator: (fullNameValue) {
                      if (fullNameValue == null) {
                        return AppStrings.nullName;
                      }

                      return null;
                    },
                  ),
                  const HeightBox(slab: 1),
                  CustomInputField(
                    label: AppStrings.email,
                    hint: AppStrings.enterEmail,
                    obscureText: false,
                    validator: (EmailValue) {
                      if (EmailValue == null) {
                        return AppStrings.nullEmail;
                      }

                      return null;
                    },
                  ),
                  const HeightBox(slab: 1),
                  GestureDetector(
                    onTap: () {
                      _showOTPBottomSheetProfile();
                    },
                    child: Container(
                      alignment: Alignment.bottomRight,
                      child: Text(
                        AppStrings.changePassword,
                        style: AppTypography.linkText,
                      ),
                    ),
                  ),
                  CustomInputField(
                    label: AppStrings.password,
                    hint: AppStrings.enterPassword,
                    obscureText: true,
                    validator: (passwordValue) {
                      if (passwordValue == null) {
                        return AppStrings.nullPassword;
                      }
                      return null;
                    },
                  ),
                  const HeightBox(slab: 1),
                  PhoneNumberInput(
                    controller: phoneNumberController,
                    dropdownItems: AppStrings.phoneCountryCodes,
                    dropdownValue: dropdownValue.value,
                    onChanged: onPhoneNumberChanged,
                    // onPhoneNumberChanged: (v) => phoneNumber.value = v,
                    validator: (fullNameValue) {
                      if (fullNameValue == null) {
                        return AppStrings.nullPhoneNumber;
                      }

                      return null;
                    },
                  ),
                  // const HeightBox(slab: 4),
                  // Center(
                  //   child: PrimaryButton(
                  //     text: 'Done',
                  //     onPressed: () {
                  //       context.router.push(PaymentDashboardRoute());
                  //     },
                  //   ),
                  // ),
                  HeightBox(slab: 2),
                  GestureDetector(
                    onTap: () {
                      _showBottomSheetDelete();
                    },
                    child: Center(
                      child: PrimaryButton(
                        color: AppColors.redColor,
                        text: AppStrings.deleteAccount,
                        onPressed: () {
                          _showBottomSheetDelete();
                        },
                      ),
                    ),
                  ),
                  BlocListener<LoginCubit, LoginState>(
                    listener: (_, state) {
                      switch (state.runtimeType) {
                        case LogoutSuccess:
                          context.router.pushAndPopUntil(
                            const IntroRoute(),
                            predicate: (route) => false,
                          );
                          break;
                      }
                    },
                    child: const SizedBox.shrink(),
                  ),
                ],
              ),
            ),
            Header(
              title: PaymentStrings.profileEdit,
              color: AppColors.blackColor,
              removeTopPadding: true,
            ),
          ],
        ),
      ),
    );
  }
}
