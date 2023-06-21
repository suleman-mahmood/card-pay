import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:frontend_futter/src/config/themes/colors.dart';

class PhoneNumberInput extends HookWidget {
  final TextEditingController controller;
  final ValueChanged<String>? onChanged;
  final List<String> dropdownItems;
  final String dropdownValue;

  PhoneNumberInput({
    required this.controller,
    required this.dropdownItems,
    required this.dropdownValue,
    this.onChanged,
  });

  @override
  Widget build(BuildContext context) {
    final screenHeight = MediaQuery.of(context).size.height;
    final screenWidth = MediaQuery.of(context).size.width;

    final dropdownMenuItems =
        dropdownItems.map<DropdownMenuItem<String>>((String value) {
      return DropdownMenuItem<String>(
        value: value,
        child: Text(value),
      );
    }).toList();

    final selectedDropdownItem = useState<String>(dropdownValue);

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        SizedBox(height: screenHeight * 0.005), // Responsive height
        Container(
          decoration: BoxDecoration(
            color: AppColors.greyColor.withOpacity(0.6),
            borderRadius: BorderRadius.circular(19),
          ),
          child: Row(
            children: [
              Container(
                width: screenWidth * 0.18,
                child: Padding(
                  padding: EdgeInsets.only(left: screenWidth * 0.02),
                  child: DropdownButton<String>(
                    value: selectedDropdownItem.value,
                    icon: Icon(Icons.arrow_drop_down),
                    iconSize: screenWidth * 0.05,
                    elevation: 16,
                    underline: Container(
                      height: 2,
                      color: Colors.transparent,
                    ),
                    isDense: true,
                    onChanged: (String? newValue) {
                      selectedDropdownItem.value = newValue!;
                      onChanged?.call(newValue);
                    },
                    items: dropdownMenuItems,
                  ),
                ),
              ),
              Expanded(
                child: Padding(
                  padding: EdgeInsets.only(right: screenWidth * 0.02),
                  child: TextField(
                    controller: controller,
                    keyboardType: TextInputType.phone,
                    decoration: InputDecoration(
                      border: InputBorder.none,
                      hintText: 'Enter your cell number',
                      isCollapsed: true,
                      contentPadding: EdgeInsets.symmetric(
                        vertical: screenHeight * 0.021,
                        horizontal: 8,
                      ),
                    ),
                  ),
                ),
              ),
            ],
          ),
        ),
      ],
    );
  }
}
