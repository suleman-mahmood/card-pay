import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:frontend_futter/src/config/themes/colors.dart';

class DropDown extends HookWidget {
  final void Function(String?) onChanged;

  const DropDown({required this.onChanged});

  @override
  Widget build(BuildContext context) {
    final selectedOrganization = useState<String?>('None');
    final screenHeight = MediaQuery.of(context).size.height;
    final screenWidth = MediaQuery.of(context).size.width;

    final organizations = [
      'None',
      'Organization 1',
      'Organization 2',
      'Organization 3',
    ];

    return Container(
      width: screenWidth * 0.9,
      decoration: BoxDecoration(
        color: AppColors.greyColor.withOpacity(0.6),
        borderRadius: BorderRadius.circular(19),
      ),
      child: Padding(
        padding: EdgeInsets.symmetric(
            horizontal: screenWidth * 0.04, vertical: screenHeight * 0.01),
        child: DropdownButtonFormField<String>(
          decoration: InputDecoration(
            hintText: 'Select your organization',
            border: InputBorder.none,
          ),
          value: selectedOrganization.value,
          dropdownColor: AppColors.greyColor,
          items: organizations.map((String organization) {
            return DropdownMenuItem<String>(
              value: organization,
              child: Align(
                alignment: Alignment.center,
                child: Text(
                  organization,
                  style: Theme.of(context).textTheme.subtitle1!.copyWith(
                        fontSize: screenWidth * 0.04,
                        color: AppColors.blackColor,
                      ),
                ),
              ),
            );
          }).toList(),
          onChanged: onChanged,
        ),
      ),
    );
  }
}
