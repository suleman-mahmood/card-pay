import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';

class CustomDropdown extends HookWidget {
  final List<String> items;
  final void Function(String?)? onChanged;
  final String? value;

  CustomDropdown({
    required this.items,
    this.onChanged,
    this.value,
  });

  @override
  Widget build(BuildContext context) {
    final dropdownValue = useMemoized(() => value);

    return DropdownButton<String>(
      value: dropdownValue,
      onChanged: onChanged,
      items: useMemoized(() {
        return items.map((String item) {
          return DropdownMenuItem<String>(
            value: item,
            child: Text(item),
          );
        }).toList();
      }),
    );
  }
}
