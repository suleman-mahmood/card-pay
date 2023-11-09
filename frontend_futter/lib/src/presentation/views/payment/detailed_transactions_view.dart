import 'package:auto_route/auto_route.dart';
import 'package:cardpay/src/presentation/widgets/boxes/height_box.dart';
import 'package:cardpay/src/presentation/widgets/boxes/horizontal_padding.dart';
import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:cardpay/src/config/themes/colors.dart';
import 'package:cardpay/src/presentation/widgets/containment/bottom_sheets/bottom_sheet_check_box.dart';
import 'package:cardpay/src/presentation/widgets/containment/lists/history_list.dart';
import 'package:cardpay/src/utils/constants/payment_strings.dart';

@RoutePage()
class DetailedTransactionsView extends HookWidget {
  const DetailedTransactionsView({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final checked1 = useState(false);
    final checked2 = useState(false);
    final checked3 = useState(false);
    final checked4 = useState(false);

    final checks = [checked1, checked2, checked3, checked4];
    final labels = [
      PaymentStrings.checkbox1,
      PaymentStrings.checkbox2,
      PaymentStrings.checkbox3,
      PaymentStrings.checkbox4
    ];
    final icons = [
      Icons.calendar_today,
      null,
      Icons.calendar_today,
      Icons.calendar_today
    ];

    final transactionList = Flexible(
      flex: 1,
      child: TransactionList(),
    );

    void _showModalBottomSheet() {
      showModalBottomSheet(
        context: context,
        builder: (BuildContext context) {
          return FilterBottomSheet(
            checks: checks,
            labels: labels,
            icons: icons,
          );
        },
      );
    }

    return SafeArea(
      child: Column(
        children: [
          const HeightBox(slab: 5),
          PaddingHorizontal(
            slab: 1,
            child: Row(
              children: [
                Expanded(
                  child: Text(PaymentStrings.transactionHistory,
                      style: AppTypography.bodyText),
                ),
                InkWell(
                  onTap: _showModalBottomSheet,
                  child: Transform.scale(
                    scale: 1.75,
                    child: Icon(
                      Icons.filter_alt,
                      color: AppColors.greyColor.withOpacity(0.35),
                    ),
                  ),
                ),
              ],
            ),
          ),
          const HeightBox(slab: 3),
          transactionList,
        ],
      ),
    );
  }
}
