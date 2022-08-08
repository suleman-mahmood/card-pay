import 'package:cardpay/services/auth.dart';
import 'package:cardpay/services/firestore.dart';
import 'package:flutter/material.dart';
import 'package:flutter/src/foundation/key.dart';
import 'package:flutter/src/widgets/framework.dart';
import 'package:cardpay/services/models.dart' as model;
import 'package:lottie/lottie.dart';
import 'package:provider/provider.dart';

class DashboardScreen extends StatelessWidget {
  const DashboardScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<model.User>(
      future: FirestoreService().getUser(),
      builder: ((context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          return Lottie.network(
              "https://assets8.lottiefiles.com/packages/lf20_g3ki3g0v.json");
        } else if (snapshot.hasData) {
          // Update the User model to reflect changes in the the entire app
          final userData = snapshot.data!;
          context.read<model.User>().updateUser(userData);

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
                            userData.balance.toString(),
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
                                userData.rollNumber,
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
                GridView(
                  shrinkWrap: true,
                  gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                    crossAxisCount: 2,
                    crossAxisSpacing: 0,
                    mainAxisExtent: 100,
                  ),
                  children: [
                    const DashboardButton(
                      routeName: 'deposit',
                      bottomText: 'Deposit',
                      isLogout: false,
                    ),
                    const DashboardButton(
                      routeName: 'transfer',
                      bottomText: 'Transfer',
                      isLogout: false,
                    ),
                    const DashboardButton(
                      routeName: 'transactions',
                      bottomText: 'Transactions',
                      isLogout: false,
                    ),
                    const DashboardButton(
                      routeName: 'deposit',
                      bottomText: 'Log Out',
                      isLogout: true,
                    ),
                  ],
                ),
              ],
            ),
          );
        } else {
          return const Text('Error!');
        }
      }),
    );
  }
}

class DashboardButton extends StatelessWidget {
  final String routeName;
  final String bottomText;
  final bool isLogout;

  const DashboardButton({
    required this.routeName,
    required this.bottomText,
    required this.isLogout,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      children: <Widget>[
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
              backgroundColor: MaterialStateProperty.all(Colors.transparent),
            ),
            onPressed: () async {
              if (isLogout) {
                await AuthService().signOut();
                Navigator.pushNamedAndRemoveUntil(
                  context,
                  '/',
                  (route) => false,
                );
              } else {
                Navigator.pushNamed(context, '/$routeName');
              }
            },
            child: Icon(
              Icons.arrow_upward,
            ),
          ),
        ),
        Text(
          bottomText,
          style: Theme.of(context).textTheme.bodyText2,
        ),
      ],
    );
  }
}
