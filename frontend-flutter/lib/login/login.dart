import 'package:cardpay/services/auth.dart';
import 'package:flutter/material.dart';
import 'package:flutter/src/foundation/key.dart';
import 'package:flutter/src/widgets/framework.dart';

class LoginScreen extends StatelessWidget {
  String email = '';
  String password = '';

  LoginScreen({Key? key}) : super(key: key);

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
                'Sign in to continue',
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
                onChanged: (String emailValue) {
                  email = emailValue;
                },
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
                onChanged: (String passwordValue) {
                  password = passwordValue;
                },
                decoration: InputDecoration(
                  labelText: 'Password',
                  border: InputBorder.none,
                ),
              ),
            ),
            Container(
              width: 250,
              padding: EdgeInsets.only(top: 15),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.end,
                children: [
                  GestureDetector(
                    onTap: () =>
                        Navigator.pushNamed(context, '/forgot-password'),
                    child: Text(
                      'Forgot Password?',
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
                onPressed: () async {
                  if (await AuthService().signIn(email, password)) {
                    Navigator.pushNamed(context, '/dashboard');
                  }
                },
                child: Text(
                  'Sign In',
                ),
              ),
            ),
            Container(
              width: 250,
              margin: EdgeInsets.only(top: 10),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Text(
                    "Don't have an account? ",
                  ),
                  GestureDetector(
                    onTap: () => Navigator.pushNamed(context, '/signup'),
                    child: Text(
                      "Sign Up",
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
