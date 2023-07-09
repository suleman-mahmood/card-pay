import 'package:flutter/material.dart';
import 'package:frontend_futter/src/config/router/app_router.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:frontend_futter/src/config/themes/colors.dart';
import 'package:frontend_futter/src/config/screen_utills/screen_util.dart';
import 'package:frontend_futter/src/presentation/widgets/containment/bottom_sheet_check_box.dart';
import 'package:frontend_futter/src/presentation/widgets/containment/history_list.dart';
import 'package:auto_route/auto_route.dart';
import 'package:frontend_futter/src/presentation/widgets/navigations/bottom_bar.dart';
import 'package:frontend_futter/src/utils/constants/payment_string.dart';

final pages = [
  HistroyRoute(),
  ConfirmationRoute(),
  FilterHistoryRoute(),
  HistroyRoute(),
];

@RoutePage()
class FilterHistoryView extends HookWidget {
  const FilterHistoryView({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final _checked1 = useState(false);
    final _checked2 = useState(false);
    final _checked3 = useState(false);
    final _checked4 = useState(false);
    final selectedIndex = useState(0);

    return Scaffold(
      body: _buildBody(context, _checked1, _checked2, _checked3, _checked4),
      bottomNavigationBar: _buildBottomNavigationBar(context, selectedIndex),
    );
  }

  Widget _buildBody(
      BuildContext context,
      ValueNotifier<bool> checked1,
      ValueNotifier<bool> checked2,
      ValueNotifier<bool> checked3,
      ValueNotifier<bool> checked4) {
    return SingleChildScrollView(
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          SizedBox(height: ScreenUtil.blockSizeVertical(context) * 3),
          _buildHeader(context, checked1, checked2, checked3, checked4),
          SizedBox(height: ScreenUtil.blockSizeVertical(context) * 3),
          _buildTransactionList(context),
        ],
      ),
    );
  }

  Widget _buildHeader(
      BuildContext context,
      ValueNotifier<bool> checked1,
      ValueNotifier<bool> checked2,
      ValueNotifier<bool> checked3,
      ValueNotifier<bool> checked4) {
    return Padding(
      padding: EdgeInsets.symmetric(
          horizontal: ScreenUtil.blockSizeHorizontal(context) * 5.5),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Expanded(
            child: Text(
              PaymentStrings.transactionHistory,
              style: AppTypography.headingFont.copyWith(
                  fontSize: ScreenUtil.textMultiplier(context) *
                      2.5 // responsive font size
                  ),
            ),
          ),
          _buildFilterIcon(context, checked1, checked2, checked3, checked4)
        ],
      ),
    );
  }

  Widget _buildFilterIcon(
      BuildContext context,
      ValueNotifier<bool> checked1,
      ValueNotifier<bool> checked2,
      ValueNotifier<bool> checked3,
      ValueNotifier<bool> checked4) {
    return Builder(builder: (BuildContext context) {
      return InkWell(
        onTap: () {
          _showFilterBottomSheet(
              context, checked1, checked2, checked3, checked4);
        },
        child: Icon(
          Icons.filter_alt,
          color: AppColors.greyColor,
          size: ScreenUtil.blockSizeHorizontal(context) *
              6, // responsive icon size
        ),
      );
    });
  }

  void _showFilterBottomSheet(
      BuildContext context,
      ValueNotifier<bool> checked1,
      ValueNotifier<bool> checked2,
      ValueNotifier<bool> checked3,
      ValueNotifier<bool> checked4) {
    Scaffold.of(context).showBottomSheet<void>(
      (BuildContext context) {
        return CustomBottomSheet(
            checked1: checked1,
            checked2: checked2,
            checked3: checked3,
            checked4:
                checked4); // using a separate widget for bottom sheet content
      },
    );
  }

  Widget _buildTransactionList(BuildContext context) {
    return Container(
      height: ScreenUtil.blockSizeVertical(context) *
          100, // responsive container height
      child: TransactionList(),
    );
  }

  Widget _buildBottomNavigationBar(
      BuildContext context, ValueNotifier<int> selectedIndex) {
    return CustomCurvedBottomBar(
      selectedIndex: selectedIndex.value,
      onItemTapped: (index) {
        selectedIndex.value = index;
        context.router.push(pages[index]);
      },
    );
  }
}
