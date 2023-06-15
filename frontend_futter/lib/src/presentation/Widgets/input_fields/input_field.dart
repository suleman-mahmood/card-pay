import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:frontend_futter/src/presentation/Widgets/input_fields/drop_down.dart';
import 'package:frontend_futter/src/config/themes/colors.dart';

class CustomInputField extends HookWidget {
  final String label;
  final String? hint;
  final bool obscureText;
  final FormFieldValidator<String>? validator;
  final List<String>? dropdownItems;
  final ValueChanged<String?>? onChanged;
  final TextInputType? keyboardType;
  final Alignment
      dropdownAlignment; // New property for specifying dropdown alignment

  const CustomInputField({
    required this.label,
    this.hint,
    this.dropdownItems,
    this.obscureText = false,
    this.validator,
    this.onChanged,
    this.keyboardType,
    this.dropdownAlignment = Alignment.centerLeft, // Set the default alignment
  });

  @override
  Widget build(BuildContext context) {
    final selectedDropdownItem = useState<String?>(null);
    final controller = useTextEditingController();
    final passwordVisible = useState<bool>(false);

    useEffect(() {
      return controller.dispose;
    }, []);

    void handleDropdownChange(String? newValue) {
      selectedDropdownItem.value = newValue;
      onChanged?.call(newValue);
    }

    void togglePasswordVisibility() {
      passwordVisible.value = !passwordVisible.value;
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
                    Expanded(
                      child: Align(
                        alignment:
                            dropdownAlignment, // Use the specified alignment
                        child: CustomDropdown(
                          items: dropdownItems!,
                          onChanged: handleDropdownChange,
                          value: selectedDropdownItem.value,
                        ),
                      ),
                    ),
                  Expanded(
                    flex: 2,
                    child: TextFormField(
                      obscureText: obscureText && !passwordVisible.value,
                      controller: controller,
                      validator: validator,
                      keyboardType: keyboardType,
                      decoration: InputDecoration(
                        border: InputBorder.none,
                        hintText: selectedDropdownItem.value ?? hint,
                        isCollapsed: true,
                        contentPadding: EdgeInsets.symmetric(
                          vertical: 19,
                          horizontal: 8,
                        ),
                      ),
                      style: TextStyle(
                        color: AppColors().blackColor,
                      ),
                    ),
                  ),
                  if (obscureText)
                    GestureDetector(
                      onTap: togglePasswordVisibility,
                      child: Icon(
                        passwordVisible.value
                            ? Icons.visibility
                            : Icons.visibility_off,
                        color: Colors.grey,
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
