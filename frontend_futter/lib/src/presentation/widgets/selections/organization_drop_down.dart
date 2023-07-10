import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:frontend_futter/src/config/themes/colors.dart';

class DropDown extends HookWidget {
  final void Function(String?) onChanged;

  const DropDown({super.key, required this.onChanged});

  static const organizations = ['None', 'LUMS', 'Nust', 'FAST', 'UET', 'IBA'];

  @override
  Widget build(BuildContext context) {
    final selectedOrganization = useState<String?>('None');
    final screenHeight = MediaQuery.of(context).size.height;
    final screenWidth = MediaQuery.of(context).size.width;

    return Container(
      width: screenWidth * 0.9,
      decoration: BoxDecoration(
        color: AppColors.greyColor.withOpacity(0.6),
        borderRadius: BorderRadius.circular(19),
      ),
      child: Padding(
        padding: EdgeInsets.symmetric(
            horizontal: screenWidth * 0.04, vertical: screenHeight * 0.003),
        child: DropdownButtonFormField<String>(
          decoration: const InputDecoration(
            hintText: 'Select your organization',
            border: InputBorder.none,
          ),
          value: selectedOrganization.value,
          dropdownColor: const Color.fromARGB(255, 209, 206, 206),
          items: organizations.map((String organization) {
            return _buildDropdownMenuItem(context, organization, screenWidth);
          }).toList(),
          onChanged: (value) {
            onChanged(value);
            selectedOrganization.value = value;
          },
        ),
      ),
    );
  }

  DropdownMenuItem<String> _buildDropdownMenuItem(
      BuildContext context, String organization, double screenWidth) {
    return DropdownMenuItem<String>(
      value: organization,
      child: Align(
        alignment: Alignment.center,
        child: Text(
          organization,
          style: Theme.of(context).textTheme.titleMedium!.copyWith(
                fontSize: screenWidth * 0.04,
                color: AppColors.blackColor,
                letterSpacing: 1.8, // increased letter spacing
              ),
        ),
      ),
    );
  }
}
