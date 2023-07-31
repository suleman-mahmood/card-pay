<<<<<<< HEAD
import 'package:cardpay/src/presentation/widgets/boxes/padding_box.dart';
import 'package:cardpay/src/presentation/widgets/loadings/list_histry_loadind.dart';
import 'package:cardpay/src/presentation/widgets/loadings/shimmer_loading.dart';
=======
import 'dart:math';
import 'package:cardpay/src/presentation/widgets/boxes/horizontal_padding.dart';
import 'package:cardpay/src/presentation/cubits/remote/user_cubit.dart';
>>>>>>> e554f655c7510d87ec59cf81541630b65a359dc0
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:cardpay/src/config/themes/colors.dart';
import 'package:cardpay/src/presentation/widgets/containment/cards/transaction_history_card.dart';

class TransactionList extends HookWidget {
  final List<Color> colors = [
    AppColors.blackColor,
    AppColors.greenColor,
    AppColors.redColor,
  ];

  TransactionList({super.key});

  @override
  Widget build(BuildContext context) {
<<<<<<< HEAD
    final transactions = useState(<dynamic>[]);
    final isLoading = true;
=======
    final userCubit = BlocProvider.of<UserCubit>(context);
>>>>>>> e554f655c7510d87ec59cf81541630b65a359dc0

    useEffect(() {
      userCubit.getUserRecentTransactions();
    }, []);

    return BlocBuilder<UserCubit, UserState>(
      builder: (_, state) {
        switch (state.runtimeType) {
          case UserLoading:
            return const Center(child: CircularProgressIndicator());
          case UserSuccess:
            return ListView.builder(
              itemCount: state.user.recentTransactions.length,
              itemBuilder: (context, index) {
                final transaction = state.user.recentTransactions[index];
                // generate a random number between 0 and 2
                final randomNumber = Random().nextInt(3);
                Color color = colors[randomNumber];

<<<<<<< HEAD
        return PaddingHorizontal(
          slab: 1,
          child: isLoading
              ? ShimmerLoading(
                  isLoading: isLoading,
                  child: ListItemLoading(),
                )
              : TransactionContainer(
                  icon: Icons.send,
                  firstText: transaction['id'],
                  secondText: transaction['amount'],
                  firstTextColor: color,
                  secondTextColor: color,
                  iconColor: color,
                  display: true,
                ),
        );
=======
                return PaddingHorizontal(
                  slab: 1,
                  child: TransactionContainer(
                    icon: Icons.send,
                    firstText: transaction.id,
                    secondText: transaction.amount.toString(),
                    firstTextColor: color,
                    secondTextColor: color,
                    iconColor: color,
                  ),
                );
              },
            );
          default:
            return const SizedBox.shrink();
        }
>>>>>>> e554f655c7510d87ec59cf81541630b65a359dc0
      },
    );
  }
}
