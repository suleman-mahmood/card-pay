import 'package:flutter/material.dart';
import 'package:flutter/src/foundation/key.dart';
import 'package:flutter/src/widgets/framework.dart';

class TransferScreen extends StatelessWidget {
  const TransferScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Container(
          margin: EdgeInsets.only(top: 50),
          child: Column(
            children: [
              Text(
                'Instant Transfer',
                style: Theme.of(context).textTheme.headline5,
              ),
              Container(
                margin: EdgeInsets.only(top: 20),
                width: 250,
                child: Text(
                  'Enter details',
                  style: Theme.of(context).textTheme.headline5,
                ),
              ),
              Container(
                width: 250,
                margin: EdgeInsets.only(top: 15),
                padding: EdgeInsets.only(left: 20),
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.all(
                    Radius.circular(10),
                  ),
                  color: Colors.orange[700],
                ),
                child: TextField(
                  decoration: InputDecoration(
                    labelText: 'Roll Number',
                    border: InputBorder.none,
                  ),
                ),
              ),
              Container(
                width: 200,
                margin: EdgeInsets.only(top: 30),
                child: MaterialButton(
                  color: Colors.orange[800],
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(10),
                  ),
                  onPressed: () => {},
                  child: Text(
                    'Transfer Now!',
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
