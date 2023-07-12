import 'package:cardpay/src/config/themes/colors.dart';
import 'package:flutter/material.dart';
import 'package:cardpay/src/presentation/widgets/actions/button/primary_button.dart';

class FilterBottomSheet extends StatelessWidget {
  final ValueNotifier<bool> checked1;
  final ValueNotifier<bool> checked2;
  final ValueNotifier<bool> checked3;
  final ValueNotifier<bool> checked4;

  const FilterBottomSheet({
    required this.checked1,
    required this.checked2,
    required this.checked3,
    required this.checked4,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      height: MediaQuery.of(context).size.height * 0.35,
      padding: EdgeInsets.only(top: 12, left: 12, right: 12, bottom: 20),
      decoration: BoxDecoration(
        color: AppColors.secondaryColor,
        borderRadius: const BorderRadius.only(
          topLeft: Radius.circular(24),
          topRight: Radius.circular(24),
        ),
        boxShadow: [
          BoxShadow(
            color: Colors.grey.withOpacity(0.5),
            spreadRadius: 5,
            blurRadius: 7,
            offset: Offset(0, 3),
          ),
        ],
      ),
      child: Column(
        children: [
          Text(
            'Filter',
            style: AppTypography.bodyText,
          ),
          SizedBox(height: 10),
          _buildCheckbox("Checkbox 1", checked1),
          _buildCheckbox("Checkbox 2", checked2),
          _buildCheckbox("Checkbox 3", checked3),
          _buildCheckbox("Checkbox 4", checked4),
          Spacer(),
          PrimaryButton(
            onPressed: () => Navigator.pop(context),
            text: "Apply",
          ),
        ],
      ),
    );
  }

  Widget _buildCheckbox(String title, ValueNotifier<bool> checked) {
    return CheckboxListTile(
      title: Text(title),
      value: checked.value,
      onChanged: (bool? value) {
        if (value != null) {
          checked.value = value;
        }
      },
    );
  }
}
