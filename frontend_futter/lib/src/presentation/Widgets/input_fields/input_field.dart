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
        SizedBox(height: 5),
        Container(
          width: 420,
          decoration: BoxDecoration(
            color: AppColors.greyColor.withOpacity(0.6),
            borderRadius: BorderRadius.circular(19),
          ),
          child: Row(
            children: [
              Expanded(
                flex: 2,
                child: Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 15.0),
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
                      contentPadding: EdgeInsets.symmetric(
                        vertical: 19,
                        horizontal: 8,
                      ),
                    ),
                  ),
                ),
              ),
              if (obscureText)
                GestureDetector(
                  onTap: togglePasswordVisibility,
                  child: Padding(
                    padding: const EdgeInsets.only(right: 15.0),
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
