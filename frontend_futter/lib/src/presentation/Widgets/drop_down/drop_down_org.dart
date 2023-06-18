import 'package:flutter/material.dart';
import 'package:frontend_futter/src/config/themes/colors.dart';

class DropDown extends StatefulWidget {
  final void Function(String?) onChanged;

  const DropDown({required this.onChanged});

  @override
  _DropDownState createState() => _DropDownState();
}

class _DropDownState extends State<DropDown> {
  String? selectedOrganization;

  List<String> organizations = [
    'None',
    'Organization 1',
    'Organization 2',
    'Organization 3',
  ];

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Expanded(
          child: DropdownButtonFormField<String>(
            decoration: InputDecoration(
              hintText: 'Enter your organization',
              icon: Icon(Icons.arrow_drop_down),
            ),
            value: selectedOrganization,
            dropdownColor:
                AppColors().primaryColor, // Set the desired dropdown color
            items: organizations.map((String organization) {
              return DropdownMenuItem<String>(
                value: organization,
                child: Text(
                  organization,
                  style: TextStyle(
                    color: AppColors().blackColor,
                  ), // Set the text color to white
                ),
              );
            }).toList(),
            onChanged: widget.onChanged,
          ),
        ),
      ],
    );
  }
}
