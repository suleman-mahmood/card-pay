import 'package:cardpay/shared/empty.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:cardpay/services/models.dart' as model;

class ErrorWidget extends StatelessWidget {
  const ErrorWidget({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    var error = context.watch<model.ErrorModel>();

    if (error.hasError) {
      return Container(
        margin: EdgeInsets.only(top: 10),
        width: 250,
        child: Text(
          error.message,
          style: TextStyle(color: Colors.red[500]),
          textAlign: TextAlign.center,
        ),
      );
    }
    return const EmptyWidget();
  }
}
