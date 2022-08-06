import 'package:cardpay/services/auth.dart';
import 'package:cardpay/services/utils.dart';
import 'package:cardpay/services/validation.dart';
import 'package:flutter/material.dart';
import 'package:flutter/src/foundation/key.dart';
import 'package:flutter/src/widgets/framework.dart';

class SignUpScreen extends StatelessWidget {
  String email = '';
  String password = '';
  String confirmpassword = '';
  final _signupformkey = GlobalKey<FormState>();
  String fullName = '';
  String rollNumber = '';

  SignUpScreen({Key? key}) : super(key: key);

  void _submit(context) async {
    if (!(email.isValidID &&
        password.isValidID &&
        (password == confirmpassword))) {
      printError("Incorrect Input - Cannot Sign up");
    }

    if (!_signupformkey.currentState!.validate()) {
      // TODO: throw proper error
      return;
    }

    // TODO: correct dependency issue on email and rollNumber
    if (!await AuthService().signUp(email, password, fullName, rollNumber)) {
      // TODO: throw proper error
      return;
    }

    Navigator.pushNamed(context, '/dashboard');
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
                    child: TextField(
                      onChanged: (String fullNameValue) {
                        fullName = fullNameValue;
                      },
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
                      onChanged: (ConfirmpasswordValue) =>
                          confirmpassword = ConfirmpasswordValue,
                      autovalidateMode: AutovalidateMode.onUserInteraction,
                      decoration: const InputDecoration(
                        labelText: 'Confirm Password',
                        border: InputBorder.none,
                      ),
                      // ignore: non_constant_identifier_names
                      validator: (ConfirmpasswordValue) {
                        if (ConfirmpasswordValue != null) {
                          print("Password is $ConfirmpasswordValue");
                          if (confirmpassword != password) {
                            printError("The Password does not Match");
                          } else {
                            printInGreen("Password Matched");
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
                      onPressed: () async {
                        _submit(context);
                      },
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
