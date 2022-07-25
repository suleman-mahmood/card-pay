import 'package:flutter/material.dart';
import 'package:flutter/src/foundation/key.dart';
import 'package:flutter/src/widgets/framework.dart';

class SignUpScreen extends StatelessWidget {
  const SignUpScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              'Welcome',
              style: Theme.of(context).textTheme.headline5,
            ),
            Container(
              width: 250,
              child: Text(
                'Lorem ipsum dolor sit amet, consectetur adipiscing elit',
                style: Theme.of(context).textTheme.bodyText2,
                textAlign: TextAlign.center,
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
                  labelText: 'Full Name',
                  border: InputBorder.none,
                ),
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
                  labelText: 'University Email',
                  border: InputBorder.none,
                ),
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
                  labelText: 'Password',
                  border: InputBorder.none,
                ),
              ),
            ),
            Container(
              margin: EdgeInsets.only(top: 15),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Checkbox(value: false, onChanged: (e) => true),
                  Container(
                    width: 200,
                    child: Text(
                      'By creating your account you agree with  our Terms and Conditions',
                      style: Theme.of(context).textTheme.bodyText2,
                    ),
                  ),
                ],
              ),
            ),
            Container(
              width: 250,
              margin: EdgeInsets.only(top: 10),
              child: MaterialButton(
                color: Colors.orange[800],
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(10),
                ),
                onPressed: () =>
                    Navigator.pushNamed(context, '/student-verification'),
                child: Text(
                  'Sign Up',
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
