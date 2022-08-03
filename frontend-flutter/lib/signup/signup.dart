import 'package:cardpay/services/auth.dart';
import 'package:cardpay/services/validation.dart';
import 'package:flutter/material.dart';
import 'package:flutter/src/foundation/key.dart';
import 'package:flutter/src/widgets/framework.dart';

class SignUpScreen extends StatelessWidget {
  String email = '';
  String password = '';
  final _signupformkey = GlobalKey<FormState>();

  SignUpScreen({Key? key}) : super(key: key);

  void _submit(context, email, password) async {
    if (_signupformkey.currentState!.validate()) {
      if (await AuthService().signUp(email, password)) {
        Navigator.pushNamed(context, '/dashboard');
      }
    }
  }

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
            Form(
              key: _signupformkey,
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Container(
                    width: 250,
                    margin: const EdgeInsets.only(top: 15),
                    padding: const EdgeInsets.only(left: 20),
                    decoration: BoxDecoration(
                      borderRadius: const BorderRadius.all(
                        Radius.circular(10),
                      ),
                      color: Colors.orange[700],
                    ),
                    child: const TextField(
                      decoration: InputDecoration(
                        labelText: 'Full Name',
                        border: InputBorder.none,
                      ),
                    ),
                  ),
                  Container(
                    width: 250,
                    margin: const EdgeInsets.only(top: 15),
                    padding: const EdgeInsets.only(left: 20),
                    decoration: BoxDecoration(
                      borderRadius: const BorderRadius.all(
                        Radius.circular(10),
                      ),
                      color: Colors.orange[700],
                    ),
                    child: TextFormField(
                      // ignore: non_constant_identifier_names
                      onChanged: (IDValue) => email = IDValue,
                      autovalidateMode: AutovalidateMode.onUserInteraction,
                      decoration: const InputDecoration(
                        labelText: 'LUMS ID',
                        border: InputBorder.none,
                      ),
                      validator: (IDValue) {
                        if (IDValue != null) {
                          print("ID is$IDValue");
                          if (!IDValue.isValidID) {
                            printWarning("Invalid LUMS ID - Out of range");
                          } else {
                            printInGreen("Valid ID");
                          }
                        } else {
                          printError("LUMS ID input field is Empty");
                        }
                      },
                    ),
                  ),
                  Container(
                    width: 250,
                    margin: const EdgeInsets.only(top: 15),
                    padding: const EdgeInsets.only(left: 20),
                    decoration: BoxDecoration(
                      borderRadius: const BorderRadius.all(
                        Radius.circular(10),
                      ),
                      color: Colors.orange[700],
                    ),
                    child: TextFormField(
                      onChanged: (passwordValue) => password = passwordValue,
                      autovalidateMode: AutovalidateMode.onUserInteraction,
                      decoration: InputDecoration(
                        labelText: 'Password',
                        border: InputBorder.none,
                      ),
                      validator: (passwordValue) {
                        if (passwordValue != null) {
                          print("Password is$passwordValue");
                          if (!passwordValue.isValidID) {
                            printWarning("Password not following regex");
                          } else {
                            printInGreen("Valid Password");
                          }
                        }
                      },
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
                    margin: const EdgeInsets.only(top: 10),
                    child: MaterialButton(
                      color: Colors.orange[800],
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(10),
                      ),
                      onPressed: () => (email.isValidID && password.isValidID)
                          ? _submit(context, email, password)
                          : printError("Incorrect Input - Cannot Sign up"),
                      child: const Text(
                        'Sign Up',
                      ),
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

// helps in debugging- will be deleted later
void printError(String text) {
  print('\x1B[31m$text\x1B[0m');
}

void printWarning(String text) {
  print('\x1B[33m$text\x1B[0m');
}

void printInGreen(String text) {
  print('\x1B[32m$text\x1B[0m');
}
