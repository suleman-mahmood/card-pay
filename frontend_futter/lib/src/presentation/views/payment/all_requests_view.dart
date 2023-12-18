import 'package:cardpay/src/presentation/cubits/remote/all_requests_cubit.dart';
import 'package:cardpay/src/presentation/widgets/boxes/height_box.dart';
import 'package:cardpay/src/presentation/widgets/layout/basic_view_layout.dart';
import 'package:cardpay/src/presentation/widgets/navigations/top_navigation.dart';
import 'package:flutter/material.dart';
import 'package:auto_route/auto_route.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:cardpay/src/config/router/app_router.dart';
import 'package:cardpay/src/config/themes/colors.dart';
import 'package:cardpay/src/utils/constants/payment_strings.dart';
import 'package:intl/intl.dart';

@RoutePage()
class AllRequestsView extends HookWidget {
  const AllRequestsView({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return BasicViewLayout(
      headerTitle: PaymentStrings.requestedMoney,
      headerColor: AppColors.blackColor,
      backgroundColor: AppColors.secondaryColor,
      children: [
        // TODO: implement search functionality
        // IconButton(
        //       onPressed: () {},
        //       icon: const Icon(
        //         Icons.search,
        //         color: Colors.black,
        //         size: 24,
        //       ),
        //     ),
        Align(
          alignment: Alignment.centerLeft,
          child: BlocBuilder<AllRequestsCubit, AllRequestsState>(
            builder: (_, state) {
              switch (state.runtimeType) {
                case AllRequestsLoading:
                  return const Center(child: CircularProgressIndicator());
                case AllRequestsSuccess:
                  return ListView.builder(
                    shrinkWrap: true,
                    itemCount: state.requestInfo.length,
                    itemBuilder: (context, index) {
                      return GestureDetector(
                        onTap: () => context.router.push(
                          RequestConfirmationRoute(
                            requestInfo: state.requestInfo[index],
                          ),
                        ),
                        child: ListTile(
                          contentPadding: const EdgeInsets.all(2),
                          leading: CircleAvatar(
                            backgroundColor: AppColors.blueColor,
                            child: Text(
                              // TODO: handle this later
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
                              text: '${state.requestInfo[index].fullName} ',
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
                                  text:
                                      'Rs. ${state.requestInfo[index].amount.toString()}',
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
                              DateFormat('d MMM h:mm a').format(
                                state.requestInfo[index].createdAt,
                              ),
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
                      );
                    },
                  );
                default:
                  return const SizedBox.shrink();
              }
            },
          ),
        ),
      ],
    );
  }
}
