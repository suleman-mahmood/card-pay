import 'package:cardpay/src/presentation/widgets/boxes/height_box.dart';
import 'package:cardpay/src/presentation/widgets/boxes/padding_box.dart';
import 'package:cardpay/src/utils/constants/signUp_string.dart';
import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:cardpay/src/config/themes/colors.dart';

class DropDown extends HookWidget {
  final void Function(String?) onChanged;

  const DropDown({Key? key, required this.onChanged}) : super(key: key);

  static const organizations = ['None', 'LUMS', 'Nust', 'FAST', 'UET', 'IBA'];

  @override
  Widget build(BuildContext context) {
    final selectedOrganization = useState<String?>('None');
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text(
          AppStrings.organization,
          style: AppTypography.bodyText,
        ),
        const HeightBox(slab: 1),
        Container(
          decoration: BoxDecoration(
            color: AppColors.lightGreyColor,
            borderRadius: BorderRadius.circular(10),
          ),
          child: PaddingHorizontal(
            slab: 2,
            child: DropdownButtonFormField<String>(
              decoration: InputDecoration(
                  hintText: 'Select your organization',
                  border: InputBorder.none),
              value: selectedOrganization.value,
              dropdownColor: AppColors.lightGreyColor,
              items: organizations.map((String organization) {
                return _buildDropdownMenuItem(context, organization);
              }).toList(),
              onChanged: (value) {
                onChanged(value);
                selectedOrganization.value = value;
              },
            ),
          ),
        ),
      ],
    );
  }

  DropdownMenuItem<String> _buildDropdownMenuItem(
      BuildContext context, String organization) {
    return DropdownMenuItem<String>(
      value: organization,
      child: Align(
        alignment: Alignment.center,
        child: Text(organization, style: AppTypography.bodyText),
      ),
    );
  }
}
