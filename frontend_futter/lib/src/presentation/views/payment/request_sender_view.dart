import 'package:cardpay/src/presentation/cubits/remote/frequent_users_cubit.dart';
import 'package:cardpay/src/presentation/cubits/remote/full_name_cubit.dart';
import 'package:cardpay/src/presentation/cubits/remote/user_cubit.dart';
import 'package:cardpay/src/presentation/widgets/boxes/height_box.dart';
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

    return
        /* Scaffold(
      backgroundColor: AppColors.mediumGreenColor,
      body: SafeArea(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.center,
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Padding(
              padding: const EdgeInsets.fromLTRB(24, 4, 24, 0),
              child: const Header(
                title: PaymentStrings.enterAmountTitle,
                color: Colors.white,
              ),
            ),
            Column(
              children: [
                Stack(
                  alignment: Alignment.center,
                  children: [
                    CircleAvatar(
                      backgroundColor: Colors.black26,
                      radius: MediaQuery.of(context).size.width * 0.25,
                    ),
                    Text(
                      'AK',
                      style: AppTypography.mainHeadingWhite.copyWith(
                        fontSize: MediaQuery.of(context).size.width * 0.15,
                      ),
                    ),
                  ],
                ),
                const HeightBox(slab: 2),
                Text(
                  'Abdullah Khan',
                  style: AppTypography.mainHeadingWhite.copyWith(
                    fontSize: 28,
                  ),
                ),
                const HeightBox(slab: 1),
                Text(
                  '26100232',
                  style: AppTypography.bodyText.copyWith(
                    color: Colors.white70,
                    fontSize: 22,
                  ),
                ),
              ],
            ),
            Container(
              width: MediaQuery.of(context).size.width,
              height: MediaQuery.of(context).size.height * 0.42,
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.only(
                  topLeft: Radius.circular(25),
                  topRight: Radius.circular(25),
                ),
                boxShadow: const [
                  BoxShadow(
                    color: Colors.black12,
                    blurRadius: 10,
                    offset: Offset(0, -5),
                  ),
                ],
              ),
              child: Column(
                children: [
                  const HeightBox(slab: 2),
                  Container(
                    width: 40,
                    height: 5,
                    decoration: BoxDecoration(
                      color: Colors.black54,
                      borderRadius: BorderRadius.circular(25),
                    ),
                  ),
                  Spacer(),
                  Text(
                    'RS. 5000',
                    style: AppTypography.mainHeadingWhite.copyWith(
                      fontSize: 48,
                      color: AppColors.blackColor.withOpacity(0.7),
                      fontWeight: FontWeight.w900,
                    ),
                  ),
                  Text(
                    'will be sent to Abdullah Khan',
                    style: AppTypography.bodyText.copyWith(
                      color: Colors.black54,
                      fontSize: 14,
                    ),
                  ),
                  const HeightBox(slab: 4),
                  RichText(
                    text: TextSpan(
                      text: 'Remaining Balance: ',
                      style: AppTypography.bodyText.copyWith(
                        color: Colors.black54,
                        fontWeight: FontWeight.bold,
                      ),
                      children: <TextSpan>[
                        TextSpan(
                          text: 'Rs. 0',
                          style: AppTypography.bodyText.copyWith(
                            color: AppColors.blackColor.withOpacity(0.54),
                            fontWeight: FontWeight.normal,
                          ),
                        ),
                      ],
                    ),
                  ),
                  const HeightBox(slab: 4),
                  PrimaryButton(
                    text: PaymentStrings.send,
                    color: AppColors.mediumGreenColor,
                    textColor: AppColors.secondaryColor,
                    onPressed: handleSubmit,
                  ),
                  const HeightBox(slab: 2),
                  PrimaryButton(
                    text: PaymentStrings.decline,
                    color: AppColors.secondaryColor,
                    textColor: AppColors.redColor,
                    onPressed: handleSubmit,
                  ),
                  Spacer(),
                ],
              ),
            ),
          ],
        ),
      ),
    ); */
        // Request Notifications Screen:: The following screen is to be transferred to a different screen
        /* Scaffold(
      backgroundColor: AppColors.secondaryColor,
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.fromLTRB(24, 4, 24, 16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  const Header(
                    title: PaymentStrings.requestedMoney,
                    color: Colors.black,
                  ),
                  const Spacer(),
                  IconButton(
                    onPressed: () {
                      // TODO: implement search functionality
                    },
                    icon: const Icon(
                      Icons.search,
                      color: Colors.black,
                      size: 24,
                    ),
                  ),
                ],
              ),
              const HeightBox(slab: 2),
              Align(
                alignment: Alignment.centerLeft,
                child: ListView.builder(
                  shrinkWrap: true,
                  itemCount: 1,
                  itemBuilder: (context, index) {
                    return Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        // a list of people who have requested with the heading for every day on top, like if the request was one day ago, say yesterday, if this week then say This Week, Last Week, This Month and so on
                        Text(
                          'Yesterday',
                          style: AppTypography.mainHeadingGrey.copyWith(
                            fontSize: 16,
                            color: Colors.black54,
                          ),
                        ),
                        const HeightBox(slab: 2),
                        ListTile(
                          contentPadding: const EdgeInsets.all(2),
                          leading: CircleAvatar(
                            backgroundColor: AppColors.blueColor,
                            child: Text(
                              'AK',
                              style: AppTypography.bodyText.copyWith(
                                color: AppColors.secondaryColor,
                                fontWeight: FontWeight.bold,
                                fontSize: 16,
                              ),
                            ),
                            radius: 24,
                          ),
                          title: RichText(
                            text: TextSpan(
                              text: 'Abdullah Khan ',
                              style: AppTypography.bodyText.copyWith(
                                color: Colors.black,
                                fontWeight: FontWeight.bold,
                                fontSize: 16,
                              ),
                              children: <TextSpan>[
                                TextSpan(
                                  text: 'requested a payment of ',
                                  style: AppTypography.bodyText.copyWith(
                                    color: Colors.black,
                                    fontWeight: FontWeight.normal,
                                    fontSize: 16,
                                  ),
                                ),
                                TextSpan(
                                  text: 'Rs. 1000',
                                  style: AppTypography.bodyText.copyWith(
                                    color: AppColors.blueColor,
                                    fontWeight: FontWeight.bold,
                                    fontSize: 16,
                                  ),
                                ),
                              ],
                            ),
                          ),
                          subtitle: Padding(
                            padding: const EdgeInsets.only(top: 4.0),
                            child: Text(
                              '09:01 AM',
                              style: AppTypography.bodyText.copyWith(
                                color: Colors.black54,
                                fontWeight: FontWeight.w300,
                                fontSize: 14,
                              ),
                            ),
                          ),
                          trailing: const Icon(
                            Icons.arrow_forward_ios,
                            color: Colors.black54,
                            size: 16,
                          ),
                        ),
                      ],
                    );
                  },
                ),
              ),
            ],
          ),
        ),
      ),
    ); */

        // Original Screen for this view
        Scaffold(
      backgroundColor: AppColors.purpleColor,
      body: SafeArea(
        child: Scaffold(
          backgroundColor: AppColors.purpleColor,
          body: Padding(
            padding: const EdgeInsets.fromLTRB(24, 4, 24, 16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Header(title: PaymentStrings.requestMoney),
                const HeightBox(slab: 2),
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
                        return Expanded(
                          child:
                              // condition to see if there are no frequent contacts
                              state.frequentUsers.isEmpty
                                  ? Padding(
                                      padding: EdgeInsets.only(
                                          bottom: MediaQuery.of(context)
                                                  .size
                                                  .height *
                                              0.2),
                                      child: Center(
                                        child: Column(
                                          mainAxisAlignment:
                                              MainAxisAlignment.center,
                                          crossAxisAlignment:
                                              CrossAxisAlignment.center,
                                          children: [
                                            Stack(
                                              alignment: Alignment.center,
                                              children: [
                                                CircleAvatar(
                                                  backgroundColor:
                                                      Colors.white60,
                                                  radius: 30,
                                                ),
                                                CircleAvatar(
                                                  backgroundColor:
                                                      AppColors.purpleColor,
                                                  radius: 26,
                                                ),
                                                const Icon(
                                                  Icons.no_accounts_outlined,
                                                  color: Colors.white60,
                                                  size: 40,
                                                ),
                                              ],
                                            ),
                                            const HeightBox(slab: 2),
                                            Text(
                                              'No frequent contacts',
                                              style: AppTypography.bodyText
                                                  .copyWith(
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
                                        return Column(children: [
                                          ListTile(
                                            onTap: () {
                                              rollNumberController.text = state
                                                  .frequentUsers[index]
                                                  .uniqueIdentifier;
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
                                              state.frequentUsers[index]
                                                  .fullName,
                                              style: AppTypography.bodyText
                                                  .copyWith(
                                                color: Colors.white,
                                              ),
                                            ),
                                            subtitle: Text(
                                              state.frequentUsers[index]
                                                  .uniqueIdentifier,
                                              style: AppTypography.bodyText
                                                  .copyWith(
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
                                        ]);
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
            ),
          ),
        ),
      ),
    );
  }
}
