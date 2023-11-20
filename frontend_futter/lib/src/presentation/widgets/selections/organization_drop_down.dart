import 'package:cardpay/src/domain/models/closed_loop.dart';
import 'package:cardpay/src/presentation/cubits/remote/closed_loop_cubit.dart';
import 'package:cardpay/src/presentation/widgets/boxes/height_box.dart';
import 'package:cardpay/src/presentation/widgets/boxes/horizontal_padding.dart';
import 'package:cardpay/src/utils/constants/auth_strings.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:cardpay/src/config/themes/colors.dart';

String promptText = 'Select your institute';

class DropDown extends HookWidget {
  final void Function(String, ClosedLoop?) onInstituteChanged;

  const DropDown({Key? key, required this.onInstituteChanged})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    final selectedOrganization = useState<String>(promptText);
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
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
            child: Padding(
              padding: EdgeInsets.symmetric(horizontal: 0),
              child: BlocBuilder<ClosedLoopCubit, ClosedLoopState>(
                builder: (_, state) {
                  switch (state.runtimeType) {
                    case ClosedLoopSuccess:
                      return DropdownButtonFormField<String>(
                        decoration: InputDecoration(
                          hintText: promptText,
                          border: InputBorder.none,
                        ),
                        value: selectedOrganization.value,
                        elevation: 4,
                        dropdownColor: Colors.white,
                        borderRadius: BorderRadius.circular(16),
                        items: [
                          _buildDropdownMenuItem(
                            context,
                            promptText,
                          ),
                          ...state.closedLoops.map((ClosedLoop closedLoops) {
                            return _buildDropdownMenuItem(
                              context,
                              closedLoops.name,
                            );
                          }).toList(),
                        ],
                        onChanged: (value) {
                          if (value == null || value == promptText) {
                            onInstituteChanged(promptText, null);
                            return;
                          }
                          onInstituteChanged(
                            value,
                            state.closedLoops.firstWhere(
                              (e) => e.name == value,
                              orElse: () => ClosedLoop(),
                            ),
                          );
                          selectedOrganization.value = value;
                        },
                      );
                    case ClosedLoopLoading:
                      return const CircularProgressIndicator();
                    default:
                      return const SizedBox.shrink();
                  }
                },
              ),
            ),
          ),
        ),
      ],
    );
  }

  DropdownMenuItem<String> _buildDropdownMenuItem(
    BuildContext context,
    String organization,
  ) {
    return DropdownMenuItem<String>(
      value: organization,
      child: Align(
        alignment: Alignment.center,
        child: Text(organization, style: AppTypography.bodyText),
      ),
    );
  }
}
