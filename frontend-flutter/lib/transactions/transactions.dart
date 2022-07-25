import 'package:flutter/material.dart';
import 'package:flutter/src/foundation/key.dart';
import 'package:flutter/src/widgets/framework.dart';

class TransactionsScreen extends StatelessWidget {
  const TransactionsScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Container(
          margin: EdgeInsets.only(top: 50),
          child: Column(
            children: [
              Text(
                'Transactions',
                style: Theme.of(context).textTheme.headline5,
              ),
              SizedBox(
                height: 20,
              ),
              Container(
                width: 300,
                padding: EdgeInsets.symmetric(vertical: 10, horizontal: 15),
                margin: EdgeInsets.only(top: 10),
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.all(
                    Radius.circular(10),
                  ),
                  color: Colors.orange[700],
                ),
                child: Row(
                  children: [
                    Flexible(
                      flex: 2,
                      fit: FlexFit.tight,
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            'Jammin Java',
                            style: Theme.of(context).textTheme.bodyText2,
                          ),
                          Text(
                            'Card',
                            style: Theme.of(context).textTheme.bodyText2,
                          ),
                        ],
                      ),
                    ),
                    Spacer(flex: 1),
                    Flexible(
                      flex: 2,
                      fit: FlexFit.tight,
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.end,
                        children: [
                          Text(
                            'PKR 250',
                            style: Theme.of(context).textTheme.bodyText2,
                          ),
                          Text(
                            'Today',
                            style: Theme.of(context).textTheme.bodyText2,
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
              ),
              Container(
                width: 300,
                padding: EdgeInsets.symmetric(vertical: 10, horizontal: 15),
                margin: EdgeInsets.only(top: 10),
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.all(
                    Radius.circular(10),
                  ),
                  color: Colors.orange[700],
                ),
                child: Row(
                  children: [
                    Flexible(
                      flex: 2,
                      fit: FlexFit.tight,
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            'Baradari',
                            style: Theme.of(context).textTheme.bodyText2,
                          ),
                          Text(
                            'QR',
                            style: Theme.of(context).textTheme.bodyText2,
                          ),
                        ],
                      ),
                    ),
                    Spacer(flex: 1),
                    Flexible(
                      flex: 2,
                      fit: FlexFit.tight,
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.end,
                        children: [
                          Text(
                            'PKR 250',
                            style: Theme.of(context).textTheme.bodyText2,
                          ),
                          Text(
                            'Today',
                            style: Theme.of(context).textTheme.bodyText2,
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
              ),
              Container(
                width: 300,
                padding: EdgeInsets.symmetric(vertical: 10, horizontal: 15),
                margin: EdgeInsets.only(top: 10),
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.all(
                    Radius.circular(10),
                  ),
                  color: Colors.orange[700],
                ),
                child: Row(
                  children: [
                    Flexible(
                      flex: 2,
                      fit: FlexFit.tight,
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            'Abdullah',
                            style: Theme.of(context).textTheme.bodyText2,
                          ),
                          Text(
                            'Transfer',
                            style: Theme.of(context).textTheme.bodyText2,
                          ),
                        ],
                      ),
                    ),
                    Spacer(flex: 1),
                    Flexible(
                      flex: 2,
                      fit: FlexFit.tight,
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.end,
                        children: [
                          Text(
                            'PKR 250',
                            style: Theme.of(context).textTheme.bodyText2,
                          ),
                          Text(
                            'Today',
                            style: Theme.of(context).textTheme.bodyText2,
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
              ),
              Container(
                width: 300,
                padding: EdgeInsets.symmetric(vertical: 10, horizontal: 15),
                margin: EdgeInsets.only(top: 10),
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.all(
                    Radius.circular(10),
                  ),
                  color: Colors.orange[700],
                ),
                child: Row(
                  children: [
                    Flexible(
                      flex: 2,
                      fit: FlexFit.tight,
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            'Fatima',
                            style: Theme.of(context).textTheme.bodyText2,
                          ),
                          Text(
                            'Transfer',
                            style: Theme.of(context).textTheme.bodyText2,
                          ),
                        ],
                      ),
                    ),
                    Spacer(flex: 1),
                    Flexible(
                      flex: 2,
                      fit: FlexFit.tight,
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.end,
                        children: [
                          Text(
                            'PKR 250',
                            style: Theme.of(context).textTheme.bodyText2,
                          ),
                          Text(
                            'Today',
                            style: Theme.of(context).textTheme.bodyText2,
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
              ),
              Container(
                width: 300,
                padding: EdgeInsets.symmetric(vertical: 10, horizontal: 15),
                margin: EdgeInsets.only(top: 10),
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.all(
                    Radius.circular(10),
                  ),
                  color: Colors.orange[700],
                ),
                child: Row(
                  children: [
                    Flexible(
                      flex: 2,
                      fit: FlexFit.tight,
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            'Deposit',
                            style: Theme.of(context).textTheme.bodyText2,
                          ),
                          Text(
                            'Account',
                            style: Theme.of(context).textTheme.bodyText2,
                          ),
                        ],
                      ),
                    ),
                    Spacer(flex: 1),
                    Flexible(
                      flex: 2,
                      fit: FlexFit.tight,
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.end,
                        children: [
                          Text(
                            'PKR 250',
                            style: Theme.of(context).textTheme.bodyText2,
                          ),
                          Text(
                            'Today',
                            style: Theme.of(context).textTheme.bodyText2,
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
