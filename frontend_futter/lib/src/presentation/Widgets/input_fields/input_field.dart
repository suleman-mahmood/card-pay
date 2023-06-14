import 'package:flutter/material.dart';
import 'package:frontend_futter/src/presentation/Widgets/input_fields/drop_down.dart';
import 'package:frontend_futter/src/config/themes/colors.dart';

class CustomInputField extends StatefulWidget {
  final String label;
  final String? hint;
  final bool obscureText;
  final FormFieldValidator<String>? validator;
  final List<String>? dropdownItems; // Optional list of dropdown items

  const CustomInputField({
    required this.label,
    this.hint,
    this.dropdownItems, // This can be null
    this.obscureText = false,
    this.validator,
  });

  @override
  _CustomInputFieldState createState() => _CustomInputFieldState();
}

class _CustomInputFieldState extends State<CustomInputField> {
  final _controller = TextEditingController();
  String? selectedDropdownItem; // To hold the selected dropdown item

  @override
  void initState() {
    super.initState();
    if (widget.dropdownItems != null && widget.dropdownItems!.isNotEmpty) {
      selectedDropdownItem = widget
          .dropdownItems![0]; // Initialize with the first item in the list
    }
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          widget.label,
          style: AppColors().inputFont.copyWith(
                color: AppColors().greyColor,
                fontSize: 16,
              ),
        ),
        SizedBox(height: 5),
        Stack(
          alignment: Alignment.center, // Align elements to the left
          children: [
            Container(
              decoration: BoxDecoration(
                color: AppColors().greyColor.withOpacity(0.6),
                borderRadius: BorderRadius.circular(10),
              ),
              child: Row(
                children: [
                  if (widget.dropdownItems != null &&
                      widget.dropdownItems!
                          .isNotEmpty) // Display the dropdown only if there are items
                    CustomDropdown(
                      items: widget.dropdownItems!,
                      onChanged: (newValue) {
                        setState(() {
                          selectedDropdownItem = newValue;
                        });
                      },
                      value: selectedDropdownItem,
                    ),
                  Expanded(
                    child: TextFormField(
                      obscureText: widget.obscureText,
                      controller: _controller,
                      validator: widget.validator,
                      decoration: InputDecoration(
                        border: InputBorder.none, // Remove the border
                        hintText: widget.hint,
                        isCollapsed: true, // Remove unnecessary padding
                        contentPadding:
                            EdgeInsets.symmetric(vertical: 10, horizontal: 16),
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ],
    );
  }
}
