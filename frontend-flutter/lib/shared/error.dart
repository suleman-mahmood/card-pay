import 'package:flutter/material.dart';
import 'package:flutter/src/foundation/key.dart';
import 'package:flutter/src/widgets/framework.dart';
import 'package:flutter/widgets.dart';
import 'package:provider/src/provider.dart';
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
    return const SizedBox.shrink();
  }
}
