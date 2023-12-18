import 'package:cardpay/src/presentation/cubits/remote/frequent_users_cubit.dart';
import 'package:cardpay/src/presentation/cubits/remote/full_name_cubit.dart';
import 'package:cardpay/src/presentation/cubits/remote/user_cubit.dart';
import 'package:cardpay/src/presentation/widgets/boxes/height_box.dart';
import 'package:cardpay/src/presentation/widgets/layout/basic_view_layout.dart';
import 'package:cardpay/src/presentation/widgets/navigations/top_navigation.dart';
import 'package:flutter/material.dart';
import 'package:auto_route/auto_route.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:cardpay/src/config/router/app_router.dart';
import 'package:cardpay/src/config/themes/colors.dart';
import 'package:cardpay/src/presentation/widgets/actions/button/primary_button.dart';
import 'package:cardpay/src/presentation/widgets/text_inputs/input_field.dart';
import 'package:cardpay/src/utils/constants/payment_strings.dart';
import 'package:cardpay/src/utils/constants/auth_strings.dart';

@RoutePage()
class RequestSenderView extends HookWidget {
  const RequestSenderView({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final rollNumberController = useTextEditingController();

    final userNameCubit = BlocProvider.of<FullNameCubit>(context);
    final userCubit = BlocProvider.of<UserCubit>(context);

    void handleSubmit() {
      FocusScope.of(context).unfocus();
      final uniqueIdentifier = rollNumberController.text;
      final closedLoopId = userCubit.state.user.closedLoops[0].closedLoopId;

      userNameCubit.getFullName(
        uniqueIdentifier: uniqueIdentifier,
        closedLoopId: closedLoopId,
      );

      context.router.push(
        RequestAmountRoute(
          recipientUniqueIdentifier: uniqueIdentifier,
          closedLoopId: closedLoopId,
        ),
      );
    }

    return BasicViewLayout(
      headerTitle: PaymentStrings.requestMoney,
      backgroundColor: AppColors.purpleColor,
      children: [
        CustomInputField(
          label: AppStrings.rollNumber,
          controller: rollNumberController,
          hint: AppStrings.enterRollNumber,
          keyboardType: TextInputType.number,
          hintColor: AppColors.greyColor,
          labelColor: AppColors.secondaryColor,
          color: AppColors.secondaryColor,
        ),
        const HeightBox(slab: 1),
        Align(
          alignment: Alignment.centerLeft,
          child: Text(
            PaymentStrings.requestingAmount,
            style: AppTypography.bodyText.copyWith(
              color: Colors.white70,
            ),
          ),
        ),
        const HeightBox(slab: 3),
        Column(
          children: [
            Text(
              'Frequent Contacts',
              style: AppTypography.mainHeadingWhite.copyWith(
                fontSize: 20,
              ),
            ),
          ],
        ),
        const HeightBox(slab: 2),
        BlocBuilder<FrequentUsersCubit, FrequentUsersState>(
          builder: (_, state) {
            switch (state.runtimeType) {
              case FrequentUsersLoading:
                return const Center(child: CircularProgressIndicator());
              case FrequentUsersSuccess:
                return SizedBox(
                  height: MediaQuery.of(context).size.height * 0.5,
                  child: state.frequentUsers.isEmpty
                      ? Padding(
                          padding: EdgeInsets.only(
                              bottom: MediaQuery.of(context).size.height * 0.2),
                          child: Center(
                            child: Column(
                              mainAxisAlignment: MainAxisAlignment.center,
                              crossAxisAlignment: CrossAxisAlignment.center,
                              children: [
                                const Stack(
                                  alignment: Alignment.center,
                                  children: [
                                    CircleAvatar(
                                      backgroundColor: Colors.white60,
                                      radius: 30,
                                    ),
                                    CircleAvatar(
                                      backgroundColor: AppColors.purpleColor,
                                      radius: 26,
                                    ),
                                    Icon(
                                      Icons.no_accounts_outlined,
                                      color: Colors.white60,
                                      size: 40,
                                    ),
                                  ],
                                ),
                                const HeightBox(slab: 2),
                                Text(
                                  'No frequent contacts',
                                  style: AppTypography.bodyText.copyWith(
                                    color: Colors.white70,
                                  ),
                                ),
                              ],
                            ),
                          ),
                        )
                      : ListView.builder(
                          itemCount: state.frequentUsers.length,
                          itemBuilder: (context, index) {
                            return Column(
                              children: [
                                ListTile(
                                  onTap: () {
                                    rollNumberController.text = state
                                        .frequentUsers[index].uniqueIdentifier;
                                    handleSubmit();
                                    rollNumberController.clear();
                                  },
                                  leading: const CircleAvatar(
                                    backgroundColor: Colors.white,
                                    child: Icon(
                                      Icons.person,
                                      color: AppColors.purpleColor,
                                    ),
                                  ),
                                  title: Text(
                                    state.frequentUsers[index].fullName,
                                    style: AppTypography.bodyText.copyWith(
                                      color: Colors.white,
                                    ),
                                  ),
                                  subtitle: Text(
                                    state.frequentUsers[index].uniqueIdentifier,
                                    style: AppTypography.bodyText.copyWith(
                                      color: Colors.white70,
                                    ),
                                  ),
                                  trailing: const Icon(
                                    Icons.arrow_forward_ios,
                                    color: Colors.white60,
                                    size: 16,
                                  ),
                                ),
                                Container(
                                  margin: const EdgeInsets.only(
                                      left: 12.0, right: 24.0),
                                  child: Divider(
                                    color: Colors.white24,
                                    thickness: 0.2,
                                  ),
                                ),
                              ],
                            );
                          },
                        ),
                );
              case FrequentUsersFailed || FrequentUsersUnknownFailure:
                return Text(
                  "User doesn't exist",
                  style: AppTypography.mainHeading,
                  textAlign: TextAlign.center,
                );
              default:
                return const SizedBox.shrink();
            }
          },
        ),
        Container(
          padding: const EdgeInsets.only(top: 8),
          alignment: Alignment.bottomCenter,
          child: PrimaryButton(
            text: PaymentStrings.next,
            color: AppColors.secondaryColor,
            textColor: AppColors.purpleColor,
            onPressed: handleSubmit,
          ),
        ),
      ],
    );
  }
}
