import 'package:auto_route/auto_route.dart';
import 'package:cardpay/src/presentation/widgets/boxes/height_box.dart';
import 'package:cardpay/src/presentation/widgets/layout/payment_layouts.dart';
import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:cardpay/src/config/themes/colors.dart';
import 'package:cardpay/src/presentation/widgets/containment/bottom_sheet_check_box.dart';
import 'package:cardpay/src/presentation/widgets/containment/history_list.dart';
import 'package:cardpay/src/utils/constants/payment_string.dart';

@RoutePage()
class FilterHistoryView extends HookWidget {
  const FilterHistoryView({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final checked1 = useState(false);
    final checked2 = useState(false);
    final checked3 = useState(false);
    final checked4 = useState(false);

    final checks = [checked1, checked2, checked3, checked4];
    final labels = ["Checkbox 1", "Checkbox 2", "Checkbox 3", "Checkbox 4"];
    final icons = [
      Icons.calendar_today,
      null,
      Icons.calendar_today,
      Icons.calendar_today
    ];

    final header = Padding(
      padding: const EdgeInsets.symmetric(horizontal: 5.5),
      child: Row(
        children: [
          Expanded(
            child: Text(PaymentStrings.transactionHistory,
                style: AppTypography.bodyText),
          ),
          Builder(
            builder: (BuildContext innerContext) {
              return InkWell(
                onTap: () {
                  Scaffold.of(innerContext).showBottomSheet<void>(
                    (BuildContext context) {
                      return FilterBottomSheet(
                        checks: checks,
                        labels: labels,
                        icons: icons,
                      );
                    },
                  );
                },
                child: Icon(
                  Icons.filter_alt,
                  color: AppColors.greyColor.withOpacity(0.35),
                  size: 34,
                ),
              );
            },
          ),
        ],
      ),
    );

    final transactionList = Flexible(
      flex: 1,
      child: TransactionList(),
    );

    return PaymentLayout(
      child: Column(
        children: [
          const HeightBox(slab: 5),
          header,
          const HeightBox(slab: 3),
          transactionList,
        ],
      ),
    );
  }
}
