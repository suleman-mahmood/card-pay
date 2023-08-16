import 'package:cardpay/src/config/router/app_router.dart';
import 'package:cardpay/src/config/screen_utills/box_decoration_all.dart';
import 'package:cardpay/src/config/themes/colors.dart';
import 'package:cardpay/src/presentation/cubits/remote/user_cubit.dart';
import 'package:cardpay/src/presentation/widgets/actions/button/primary_button.dart';
import 'package:cardpay/src/presentation/widgets/boxes/all_padding.dart';
import 'package:cardpay/src/presentation/widgets/boxes/height_box.dart';
import 'package:cardpay/src/presentation/widgets/boxes/horizontal_padding.dart';
import 'package:cardpay/src/presentation/widgets/layout/profile_layout.dart';
import 'package:cardpay/src/presentation/widgets/navigations/animated_bottom_bar.dart';
import 'package:cardpay/src/presentation/widgets/selections/phonenumber_drop_down.dart';
import 'package:cardpay/src/presentation/widgets/text_inputs/input_field.dart';
import 'package:cardpay/src/utils/constants/event_codes.dart';
import 'package:cardpay/src/utils/constants/payment_string.dart';
import 'package:cardpay/src/utils/constants/signUp_string.dart';
import 'package:flutter/material.dart';
import 'package:auto_route/auto_route.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_hooks/flutter_hooks.dart';

@RoutePage()
class EditProfileView extends HookWidget {
  const EditProfileView({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final userCubit = BlocProvider.of<UserCubit>(context);
    // useEffect(() {
    //   someFunction() async {
    //     await userCubit.getUser();
    //   }

    //   someFunction();
    // }, []);
    void handleLogout() async {
      await userCubit.logout();
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
                      BlocBuilder<UserCubit, UserState>(builder: (_, state) {
                        switch (state.runtimeType) {
                          case UserSuccess:
                            if (state.eventCodes ==
                                EventCodes.LOGOUT_SUCCESSFUL) {
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
        child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          Text(
            PaymentStrings.profileEdit,
            style: AppTypography.mainHeading,
          ),
          const HeightBox(slab: 1),
          GestureDetector(
            onTap: () {
              _showBottomSheetAvatar();
            },
            child: Center(
              child: Stack(children: [
                CircleAvatar(
                  radius: 40,
                  backgroundImage: AssetImage('assets/images/talha.jpg'),
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
                return "Please enter your full name";
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
                return "Please enter your email";
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
                "hello",
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
                return "Please enter your password";
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
                return "Please enter your phone number";
              }

              return null;
            },
          ),
          const HeightBox(slab: 4),
          Center(
            child: PrimaryButton(
              text: 'Done',
              onPressed: () {},
            ),
          ),
          HeightBox(slab: 2),
          GestureDetector(
            onTap: () {
              _showBottomSheetDelete();
            },
            child: Center(
              child: PrimaryButton(
                color: AppColors.redColor,
                text: 'Delete Account',
                onPressed: () {
                  _showBottomSheetDelete();
                },
              ),
            ),
          ),
          HeightBox(slab: 5),
          AnimatedBottomBar(
            selectedIndex: ValueNotifier(3),
          ),
        ]),
      ),
    );
  }
}
