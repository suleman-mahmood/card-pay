import 'package:auto_route/auto_route.dart';
import 'package:cardpay/src/config/screen_utills/box_shadow.dart';
import 'package:cardpay/src/presentation/widgets/boxes/horizontal_padding.dart';
import 'package:cardpay/src/presentation/widgets/navigations/top_navigation.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
import 'package:cardpay/src/config/themes/colors.dart';
import 'package:cardpay/src/utils/constants/payment_strings.dart';
import 'dart:convert';

@RoutePage()
class FaqsView extends HookWidget {
  const FaqsView({Key? key}) : super(key: key);
  @override
  Widget build(BuildContext context) {
    return Stack(
      children: [
        Container(
          color: AppColors.teal,
          child: Align(
            alignment: Alignment.bottomCenter,
            child: FractionallySizedBox(
              heightFactor: 3 / 4,
              child: DecoratedBox(
                decoration: CustomBoxDecoration.getDecoration(),
                child: PaddingHorizontal(
                    slab: 1,
                    child: FutureBuilder(
                      future: rootBundle.loadString('assets/files/faqs.json'),
                      builder: (context, snapshot) {
                        if (snapshot.hasData) {
                          final List<dynamic> data =
                              json.decode(snapshot.data.toString());
                          return ListView(
                            children: data.map<Widget>((item) {
                              return Card(
                                child: ExpansionTile(
                                  title: Text(item['title']),
                                  children: <Widget>[
                                    ListTile(title: Text(item['listTile'])),
                                  ],
                                ),
                              );
                            }).toList(),
                          );
                        } else if (snapshot.hasError) {
                          return Text('Error: ${snapshot.error}');
                        }
                        return const CircularProgressIndicator();
                      },
                    )),
              ),
            ),
          ),
        ),
        const PaddingHorizontal(
          slab: 2,
          child: Header(
            showBackButton: true,
            showMainHeading: true,
            mainHeadingText: PaymentStrings.helpDetail,
          ),
        ),
      ],
    );
  }
}
