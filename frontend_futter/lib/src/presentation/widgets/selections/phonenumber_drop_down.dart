import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:frontend_futter/src/config/themes/colors.dart';
import 'package:frontend_futter/src/presentation/widgets/boxes/height_box.dart';
import 'package:frontend_futter/src/utils/constants/payment_string.dart';

class PhoneNumberInput extends HookWidget {
  final TextEditingController controller;
  final ValueChanged<String>? onChanged;
  final List<String> dropdownItems;
  final String dropdownValue;

  const PhoneNumberInput({
    super.key,
    required this.controller,
    required this.dropdownItems,
    required this.dropdownValue,
    this.onChanged,
  });

  @override
  Widget build(BuildContext context) {
    final screenHeight = MediaQuery.of(context).size.height;
    final screenWidth = MediaQuery.of(context).size.width;

    final dropdownMenuItems = _buildDropdownMenuItems(dropdownItems);

    final selectedDropdownItem = useState<String>(dropdownValue);

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text(
          PaymentStrings.phone,
          style: AppTypography.bodyText,
        ),
        const HeightBox(slab: 1),
        Container(
          decoration: BoxDecoration(
            color: AppColors.greyColor.withOpacity(0.25),
            borderRadius: BorderRadius.circular(16),
          ),
          child: Row(
            children: [
              _buildDropdown(
                screenWidth: screenWidth,
                selectedDropdownItem: selectedDropdownItem,
                dropdownMenuItems: dropdownMenuItems,
              ),
              Expanded(
                child: _buildTextField(screenHeight, screenWidth),
              ),
            ],
          ),
        ),
      ],
    );
  }

  TextField _buildTextField(double screenHeight, double screenWidth) {
    return TextField(
      controller: controller,
      keyboardType: TextInputType.phone,
      decoration: const InputDecoration(
        border: InputBorder.none,
        hintText: PaymentStrings.enterPhone,
        isCollapsed: true,
        contentPadding: EdgeInsets.only(
          right: 24,
          top: 16,
          bottom: 16,
        ),
      ),
    );
  }

  Widget _buildDropdown({
    required double screenWidth,
    required ValueNotifier<String> selectedDropdownItem,
    required List<DropdownMenuItem<String>> dropdownMenuItems,
  }) {
    return Padding(
      padding: const EdgeInsets.only(left: 24),
      child: DropdownButton<String>(
        value: selectedDropdownItem.value,
        icon: const Icon(Icons.arrow_drop_down),
        iconSize: 24,
        elevation: 16,
        isDense: true,
        onChanged: (String? newValue) {
          selectedDropdownItem.value = newValue!;
          onChanged?.call(newValue);
        },
        items: dropdownMenuItems,
      ),
    );
  }

  List<DropdownMenuItem<String>> _buildDropdownMenuItems(
      List<String> dropdownItems) {
    return dropdownItems.map<DropdownMenuItem<String>>((String value) {
      return DropdownMenuItem<String>(
        value: value,
        child: Text(value),
      );
    }).toList();
  }
}
