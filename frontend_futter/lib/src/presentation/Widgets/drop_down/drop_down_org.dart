import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:frontend_futter/src/config/themes/colors.dart';

class DropDown extends HookWidget {
  final void Function(String?) onChanged;

  const DropDown({required this.onChanged});

  @override
  Widget build(BuildContext context) {
    final selectedOrganization =
        useState<String?>('None'); // Set default organization to "None"

    final organizations = [
      'None',
      'Organization 1',
      'Organization 2',
      'Organization 3',
    ];

    return Container(
      decoration: BoxDecoration(
        color: AppColors.greyColor.withOpacity(0.6),
        borderRadius: BorderRadius.circular(19),
      ),
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 8),
        child: DropdownButtonFormField<String>(
          decoration: InputDecoration(
            hintText: 'Select your organizationS', // Add hint text
            border: InputBorder.none,
            isDense: true,
          ),
          value: selectedOrganization.value,
          dropdownColor: AppColors.primaryColor,
          items: organizations.map((String organization) {
            return DropdownMenuItem<String>(
              value: organization,
              child: Align(
                alignment:
                    Alignment.center, // Align the organization in the center
                child: Text(
                  organization,
                  style: TextStyle(
                    color: AppColors.blackColor,
                  ),
                ),
              ),
            );
          }).toList(),
          onChanged: (value) {
            selectedOrganization.value = value;
            onChanged(value);
          },
        ),
      ),
    );
  }
}
