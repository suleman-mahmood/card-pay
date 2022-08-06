// ignore_for_file: non_constant_identifier_names

import 'package:cardpay/services/auth.dart';
import 'package:cardpay/services/utils.dart';
import 'package:cardpay/services/validation.dart';
import 'package:flutter/material.dart';
import 'package:flutter/src/foundation/key.dart';
import 'package:flutter/src/widgets/framework.dart';

class SignUpScreen extends StatelessWidget {
  String rollNumber = '';
  String password = '';
  String confirmpassword = '';
  String fullName = '';

  SignUpScreen({Key? key}) : super(key: key);
  final signupformkey = GlobalKey<FormState>();

  void _submit(context) async {
    if (!signupformkey.currentState!.validate()) {
      // No need to throw any error as each textfield will take care
      // of its own validation error
      return;
    }

    // TODO: correct dependency issue on email and rollNumber
    if (!await AuthService().signUp(fullName, rollNumber, password)) {
      // TODO: throw proper error and update UI accordingly
      return;
    }

    printWarning("$fullName has rollnumber: $rollNumber with pass: $password");
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
              key: signupformkey,
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
                    child: TextFormField(
                      autovalidateMode: AutovalidateMode.onUserInteraction,
                      onChanged: (nameValue) => fullName = nameValue,
                      decoration: const InputDecoration(
                        labelText: 'Full Name',
                        border: InputBorder.none,
                      ),
                      validator: (nameValue) {
                        if (nameValue == null) {
                          return "Please enter your name";
                        }
                        if (!nameValue.isValidName) {
                          return "Please enter your first name and last name";
                        }
                        return null;
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
                      autovalidateMode: AutovalidateMode.onUserInteraction,
                      onChanged: (rollNumberValue) =>
                          rollNumber = rollNumberValue,
                      decoration: const InputDecoration(
                        labelText: 'LUMS Roll number',
                        border: InputBorder.none,
                      ),
                      validator: (rollNumberValue) {
                        if (rollNumberValue == null) {
                          return "Please enter Roll Number";
                        }
                        if (!rollNumberValue.isValidRollNumber) {
                          return "Invalid ID";
                        }
                        return null;
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
                      obscureText: true,
                      autovalidateMode: AutovalidateMode.onUserInteraction,
                      onChanged: (passwordValue) => password = passwordValue,
                      decoration: const InputDecoration(
                        labelText: 'Password',
                        border: InputBorder.none,
                      ),
                      validator: (passwordValue) {
                        if (passwordValue == null) {
                          return "Please enter Password";
                        }
                        if (!passwordValue.isValidPassword) {
                          return "Weak Password";
                        }
                        return null;
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
                      obscureText: true,
                      autovalidateMode: AutovalidateMode.onUserInteraction,
                      onChanged: (ConfirmpasswordValue) =>
                          confirmpassword = ConfirmpasswordValue,
                      decoration: const InputDecoration(
                        labelText: 'Confirm Password',
                        border: InputBorder.none,
                      ),
                      validator: (ConfirmpasswordValue) {
                        if (ConfirmpasswordValue == null) {
                          return "Please re-enter Password";
                        }
                        if (ConfirmpasswordValue != password) {
                          return "The passwords don't match";
                        }
                        return null;
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
                      onPressed: () => _submit(context),
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
