import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:frontend_futter/src/presentation/Widgets/input_fields/drop_down.dart';
import 'package:frontend_futter/src/config/themes/colors.dart';

class CustomInputField extends HookWidget {
  final String label;
  final String? hint;
  final bool obscureText;
  final FormFieldValidator<String>? validator;
  final List<String>? dropdownItems; // Optional list of dropdown items
  final ValueChanged<String?>? onChanged; // New onChanged property

  const CustomInputField({
    required this.label,
    this.hint,
    this.dropdownItems,
    this.obscureText = false,
    this.validator,
    this.onChanged, // Include onChanged property in the constructor
  });

  @override
  Widget build(BuildContext context) {
    final selectedDropdownItem = useState<String?>(dropdownItems?[0]);
    final controller = useTextEditingController();

    useEffect(() {
      return controller.dispose;
    }, []);

    // Call onChanged callback when dropdown value changes
    void handleDropdownChange(String? newValue) {
      selectedDropdownItem.value = newValue;
      onChanged?.call(newValue);
    }

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          label,
          style: AppColors().inputFont.copyWith(
                color: AppColors().blackColor,
                fontSize: 16,
              ),
        ),
        SizedBox(height: 5),
        Stack(
          alignment: Alignment.center,
          children: [
            Container(
              width: 420,
              decoration: BoxDecoration(
                color: AppColors().greyColor.withOpacity(0.6),
                borderRadius: BorderRadius.circular(19),
              ),
              child: Row(
                children: [
                  if (dropdownItems != null && dropdownItems!.isNotEmpty)
                    CustomDropdown(
                      items: dropdownItems!,
                      onChanged:
                          handleDropdownChange, // Use the modified callback
                      value: selectedDropdownItem.value,
                    ),
                  Expanded(
                    child: TextFormField(
                      obscureText: obscureText,
                      controller: controller,
                      validator: validator,
                      decoration: InputDecoration(
                        border: InputBorder.none,
                        hintText: hint,
                        isCollapsed: true,
                        contentPadding: EdgeInsets.symmetric(
                          vertical: 19,
                          horizontal: 8,
                        ),
                      ),
                      style: TextStyle(
                        color: AppColors().greenColor,
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
