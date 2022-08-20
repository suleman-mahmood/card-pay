import 'package:cardpay/dashboard/dashboard.dart';
import 'package:cardpay/services/auth.dart';
import 'package:flutter/material.dart';

class WelcomeScreen extends StatelessWidget {
  const WelcomeScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return StreamBuilder(
      stream: AuthService().userStream,
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          return const Scaffold(
            body: Center(
              child: Text('loading'),
            ),
          );
        } else if (snapshot.hasError) {
          return const Scaffold(
            body: Center(
              child: Text('error'),
            ),
          );
        } else if (snapshot.hasData) {
          // There is data if the user is logged in so goto dashboard
          return const DashboardScreen();
        } else {
          return const WelcomeWidget();
        }
      },
    );
  }
}

class WelcomeWidget extends StatelessWidget {
  const WelcomeWidget({
    Key? key,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Column(
        children: [
          Spacer(
            flex: 1,
          ),
          Row(
            children: [
              Flexible(
                flex: 9,
                fit: FlexFit.tight,
                child: Card(
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.only(
                      topRight: Radius.circular(125),
                    ),
                  ),
                  color: Colors.yellow[700],
                  child: Container(
                    padding: EdgeInsets.symmetric(vertical: 20, horizontal: 30),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          children: [
                            Container(
                              margin: EdgeInsets.only(right: 10),
                              decoration: BoxDecoration(
                                color: Colors.orange[900],
                                borderRadius:
                                    BorderRadius.all(Radius.circular(10)),
                              ),
                              width: 50,
                              height: 10,
                            ),
                            Container(
                              margin: EdgeInsets.only(right: 10),
                              decoration: BoxDecoration(
                                color: Colors.orange[800],
                                borderRadius:
                                    BorderRadius.all(Radius.circular(10)),
                              ),
                              width: 20,
                              height: 10,
                            ),
                            Container(
                              decoration: BoxDecoration(
                                color: Colors.orange[800],
                                borderRadius:
                                    BorderRadius.all(Radius.circular(10)),
                              ),
                              width: 20,
                              height: 10,
                            ),
                          ],
                        ),
                        Container(
                          margin: EdgeInsets.only(top: 10),
                          child: Text(
                            'Welcome',
                            style: Theme.of(context).textTheme.headline6,
                          ),
                        ),
                        Container(
                          margin: EdgeInsets.only(top: 10),
                          child: Text(
                            'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed rutrum vehicula mi, in varius metus vulputate vel. Phasellus aliquam lorem non ipsum mattis pretium. Quisque nec varius magna. Vestibulum in.',
                            style: Theme.of(context).textTheme.bodyText1,
                          ),
                        ),
                        Row(
                          children: [
                            Flexible(
                              fit: FlexFit.tight,
                              child: Container(
                                margin: EdgeInsets.only(top: 10),
                                child: MaterialButton(
                                  color: Colors.orange[800],
                                  shape: RoundedRectangleBorder(
                                    borderRadius: BorderRadius.circular(10),
                                  ),
                                  onPressed: () =>
                                      Navigator.pushNamed(context, '/login'),
                                  child: Text(
                                    'Start Paying',
                                  ),
                                ),
                              ),
                            ),
                          ],
                        ),
                      ],
                    ),
                  ),
                ),
              ),
              Spacer(
                flex: 1,
              ),
            ],
          ),
        ],
      ),
    );
  }
}
