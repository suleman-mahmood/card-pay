import 'package:cardpay/services/auth.dart';
import 'package:flutter/material.dart';
import 'package:flutter/src/foundation/key.dart';
import 'package:flutter/src/widgets/framework.dart';

class DashboardScreen extends StatelessWidget {
  const DashboardScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Column(
        children: [
          Container(
            margin: EdgeInsets.only(left: 40, top: 60),
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Total balance',
                      style: Theme.of(context).textTheme.bodyText2,
                    ),
                    Text(
                      'Rs. 15,000',
                      style: Theme.of(context).textTheme.headline5,
                    ),
                    Container(
                      margin: EdgeInsets.only(top: 20),
                      child: Text(
                        'This month',
                        style: Theme.of(context).textTheme.bodyText2,
                      ),
                    ),
                    Row(
                      children: [
                        Icon(Icons.arrow_drop_up, color: Colors.green),
                        Text(
                          'Rs. 5,000',
                          style: Theme.of(context).textTheme.headline5,
                        ),
                      ],
                    ),
                    Row(
                      children: [
                        Icon(Icons.arrow_drop_down, color: Colors.red),
                        Text(
                          'Rs. 3,000',
                          style: Theme.of(context).textTheme.headline5,
                        ),
                      ],
                    ),
                  ],
                ),
                Spacer(flex: 1),
                Container(
                  padding: EdgeInsets.only(
                      top: 20, left: 20, right: 20, bottom: 100),
                  decoration: BoxDecoration(
                    color: Colors.orange[700],
                    borderRadius: BorderRadius.all(
                      Radius.circular(10),
                    ),
                  ),
                  child: Column(
                    children: [
                      Text(
                        'Student Card',
                        style: Theme.of(context).textTheme.headline5,
                      ),
                      Container(
                        margin: EdgeInsets.only(top: 20),
                        child: Text(
                          '23000000',
                          style: Theme.of(context).textTheme.bodyText2,
                        ),
                      )
                    ],
                  ),
                ),
              ],
            ),
          ),
          // Dashboard Buttons
          Container(
            margin: EdgeInsets.only(top: 50),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Container(
                  margin: EdgeInsets.only(right: 20),
                  child: Column(
                    children: [
                      Container(
                        width: 150,
                        decoration: BoxDecoration(
                          borderRadius: BorderRadius.all(
                            Radius.circular(10),
                          ),
                          border: Border.all(
                            color: (Colors.orange[700])!,
                          ),
                        ),
                        child: ElevatedButton(
                          style: ButtonStyle(
                            backgroundColor:
                                MaterialStateProperty.all(Colors.transparent),
                          ),
                          onPressed: () =>
                              Navigator.pushNamed(context, '/deposit'),
                          child: Icon(
                            Icons.arrow_upward,
                          ),
                        ),
                      ),
                      Text(
                        'Deposit',
                        style: Theme.of(context).textTheme.bodyText2,
                      )
                    ],
                  ),
                ),
                Column(
                  children: [
                    Container(
                      width: 150,
                      decoration: BoxDecoration(
                        borderRadius: BorderRadius.all(
                          Radius.circular(10),
                        ),
                        border: Border.all(
                          color: (Colors.orange[700])!,
                        ),
                      ),
                      child: ElevatedButton(
                        style: ButtonStyle(
                          backgroundColor:
                              MaterialStateProperty.all(Colors.transparent),
                        ),
                        onPressed: () => {},
                        child: Icon(
                          Icons.arrow_upward,
                        ),
                      ),
                    ),
                    Text(
                      'Withdraw',
                      style: Theme.of(context).textTheme.bodyText2,
                    )
                  ],
                ),
              ],
            ),
          ),
          Container(
            margin: EdgeInsets.only(top: 20),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Container(
                  margin: EdgeInsets.only(right: 20),
                  child: Column(
                    children: [
                      Container(
                        width: 150,
                        decoration: BoxDecoration(
                          borderRadius: BorderRadius.all(
                            Radius.circular(10),
                          ),
                          border: Border.all(
                            color: (Colors.orange[700])!,
                          ),
                        ),
                        child: ElevatedButton(
                          style: ButtonStyle(
                            backgroundColor:
                                MaterialStateProperty.all(Colors.transparent),
                          ),
                          onPressed: () =>
                              Navigator.pushNamed(context, '/transfer'),
                          child: Icon(
                            Icons.arrow_upward,
                          ),
                        ),
                      ),
                      Text(
                        'Transfer',
                        style: Theme.of(context).textTheme.bodyText2,
                      )
                    ],
                  ),
                ),
                Column(
                  children: [
                    Container(
                      width: 150,
                      decoration: BoxDecoration(
                        borderRadius: BorderRadius.all(
                          Radius.circular(10),
                        ),
                        border: Border.all(
                          color: (Colors.orange[700])!,
                        ),
                      ),
                      child: ElevatedButton(
                        style: ButtonStyle(
                          backgroundColor:
                              MaterialStateProperty.all(Colors.transparent),
                        ),
                        onPressed: () =>
                            Navigator.pushNamed(context, '/transactions'),
                        child: Icon(
                          Icons.arrow_upward,
                        ),
                      ),
                    ),
                    Text(
                      'Transactions',
                      style: Theme.of(context).textTheme.bodyText2,
                    )
                  ],
                ),
              ],
            ),
          ),
          Container(
            margin: EdgeInsets.only(right: 20),
            child: Column(
              children: [
                Container(
                  width: 150,
                  decoration: BoxDecoration(
                    borderRadius: BorderRadius.all(
                      Radius.circular(10),
                    ),
                    border: Border.all(
                      color: (Colors.orange[700])!,
                    ),
                  ),
                  child: ElevatedButton(
                    style: ButtonStyle(
                      backgroundColor:
                          MaterialStateProperty.all(Colors.transparent),
                    ),
                    onPressed: () async {
                      await AuthService().signOut();
                      Navigator.pushNamedAndRemoveUntil(
                        context,
                        '/',
                        (route) => false,
                      );
                    },
                    child: Icon(
                      Icons.arrow_upward,
                    ),
                  ),
                ),
                Text(
                  'Log Out',
                  style: Theme.of(context).textTheme.bodyText2,
                )
              ],
            ),
          ),
        ],
      ),
    );
  }
}
