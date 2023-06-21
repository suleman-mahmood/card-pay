import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:frontend_futter/src/config/themes/colors.dart';

class CustomInputField extends HookWidget {
  final String label;
  final String? hint;
  final bool obscureText;
  final FormFieldValidator<String>? validator;
  final ValueChanged<String?>? onChanged;
  final TextInputType? keyboardType;

  const CustomInputField({
    required this.label,
    this.hint,
    this.obscureText = false,
    this.validator,
    this.onChanged,
    this.keyboardType,
  });

  @override
  Widget build(BuildContext context) {
    final controller = useTextEditingController();
    final passwordVisible = useState<bool>(false);
    final screenHeight = MediaQuery.of(context).size.height;
    final screenWidth = MediaQuery.of(context).size.width;

    useEffect(() {
      return controller.dispose;
    }, []);

    void togglePasswordVisibility() {
      passwordVisible.value = !passwordVisible.value;
    }

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          label,
          style: TextStyle(
            color: Colors.black,
            fontSize: 16,
          ),
        ),
        SizedBox(height: screenHeight * 0.005),
        Container(
          width: screenWidth * 0.9,
          decoration: BoxDecoration(
            color: AppColors.greyColor.withOpacity(0.5),
            borderRadius: BorderRadius.circular(19),
          ),
          child: Row(
            children: [
              Expanded(
                flex: 2,
                child: Padding(
                  // Responsive horizontal padding
                  padding: EdgeInsets.symmetric(horizontal: screenWidth * 0.03),
                  child: TextFormField(
                    obscureText: obscureText && !passwordVisible.value,
                    controller: controller,
                    validator: validator,
                    keyboardType: keyboardType,
                    onChanged: onChanged,
                    decoration: InputDecoration(
                      border: InputBorder.none,
                      hintText: hint,
                      isCollapsed: true,
                      // Responsive content padding
                      contentPadding: EdgeInsets.symmetric(
                        vertical: screenHeight * 0.02,
                        horizontal: screenWidth * 0.02,
                      ),
                    ),
                  ),
                ),
              ),
              if (obscureText)
                GestureDetector(
                  onTap: togglePasswordVisibility,
                  child: Padding(
                    // Responsive padding
                    padding: EdgeInsets.only(right: screenWidth * 0.04),
                    child: Icon(
                      passwordVisible.value
                          ? Icons.visibility
                          : Icons.visibility_off,
                      color: AppColors.greyColor,
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
