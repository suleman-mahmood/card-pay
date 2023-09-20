import 'package:cardpay/src/config/screen_utills/box_shadow.dart';
import 'package:cardpay/src/config/themes/colors.dart';
import 'package:cardpay/src/presentation/widgets/boxes/horizontal_padding.dart';
import 'package:cardpay/src/utils/constants/payment_strings.dart';
import 'package:flutter/material.dart';
import 'package:cardpay/src/presentation/widgets/actions/button/primary_button.dart';
import 'package:flutter_hooks/flutter_hooks.dart';

class FilterBottomSheet extends HookWidget {
  final List<ValueNotifier<bool>> checks;
  final List<String> labels;
  final List<IconData?> icons;

  const FilterBottomSheet(
      {required this.checks, required this.labels, required this.icons});

  @override
  Widget build(BuildContext context) {
    Widget _buildCheckbox(String title, ValueNotifier<bool> checked,
        [IconData? icon]) {
      return ListTile(
        leading: Checkbox(
          value: checked.value,
          onChanged: (bool? value) {
            if (value != null) {
              checked.value = value;
            }
          },
        ),
        title: Text(title),
        trailing: icon != null ? Icon(icon) : null,
      );
    }

    List<Widget> _buildCheckboxes() {
      return List<Widget>.generate(checks.length, (index) {
        return PaddingHorizontal(
          slab: 2,
          child: _buildCheckbox(labels[index], checks[index], icons[index]),
        );
      });
    }

    return Container(
      height: MediaQuery.of(context).size.height * 0.40,
      padding: EdgeInsets.only(top: 12, left: 12, right: 12, bottom: 20),
      decoration: CustomBoxDecoration.getDecoration(),
      child: Column(
        children: [
          Text(
            PaymentStrings.filterTransactions,
            style: AppTypography.bodyTextBold,
          ),
          SizedBox(height: 4),
          ..._buildCheckboxes(),
          Spacer(),
          PrimaryButton(
            color: AppColors.purpleColor,
            onPressed: () => Navigator.pop(context),
            text: PaymentStrings.apply,
          ),
        ],
      ),
    );
  }
}
