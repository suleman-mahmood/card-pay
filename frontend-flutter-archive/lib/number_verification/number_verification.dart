import 'package:flutter/material.dart';
import 'package:pin_code_fields/pin_code_fields.dart';

class NumberVerificationScreen extends StatelessWidget {
  const NumberVerificationScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              'Verify Account',
              style: Theme.of(context).textTheme.headline5,
            ),
            Container(
              margin: EdgeInsets.only(top: 10),
              child: Text(
                'Enter 4-digit code we have sent to your email',
                style: Theme.of(context).textTheme.bodyText2,
              ),
            ),
            Text(
              '23000000@lums.edu.pk',
              style: Theme.of(context).textTheme.bodyText2,
            ),
            Container(
              width: 250,
              margin: EdgeInsets.symmetric(vertical: 40),
              child: PinCodeTextField(
                appContext: context,
                length: 4,
                animationType: AnimationType.fade,
                pinTheme: PinTheme(
                  shape: PinCodeFieldShape.box,
                  borderRadius: BorderRadius.circular(5),
                  fieldHeight: 50,
                  fieldWidth: 40,
                  activeFillColor: Colors.white,
                ),
                cursorColor: Colors.black,
                animationDuration: const Duration(milliseconds: 300),
                enableActiveFill: true,
                keyboardType: TextInputType.number,
                boxShadows: const [
                  BoxShadow(
                    offset: Offset(0, 1),
                    color: Colors.black12,
                    blurRadius: 10,
                  )
                ],
                onChanged: (value) {},
              ),
            ),
            Text(
              "Didn't receive the code?",
              style: Theme.of(context).textTheme.bodyText2,
            ),
            Text(
              "Resend Code",
              style: Theme.of(context).textTheme.bodyText2,
            ),
            Container(
              width: 250,
              margin: EdgeInsets.only(top: 10),
              child: MaterialButton(
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(10),
                ),
                color: Colors.orange[800],
                onPressed: () => Navigator.pushNamed(context, '/dashboard'),
                child: Text(
                  'Proceed',
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
