import 'package:cardpay/about/about.dart';
import 'package:cardpay/analysis/analysis.dart';
import 'package:cardpay/conflict/conflict.dart';
import 'package:cardpay/dashboard/dashboard.dart';
import 'package:cardpay/deposit/deposit.dart';
import 'package:cardpay/feedback/feedback.dart';
import 'package:cardpay/forgot_password/forgot_password.dart';
import 'package:cardpay/login/login.dart';
import 'package:cardpay/profile/profile.dart';
import 'package:cardpay/signup/signup.dart';
import 'package:cardpay/student_verification/student_verification.dart';
import 'package:cardpay/transactions/transactions.dart';
import 'package:cardpay/transfer/transfer.dart';
import 'package:cardpay/welcome/welcome.dart';
import 'package:cardpay/withdraw/withdraw.dart';

var appRoutes = {
  '/': (context) => WelcomeScreen(),
  '/dashboard': (context) => DashboardScreen(),
  '/login': (context) => LoginScreen(),
  '/signup': (context) => SignUpScreen(),
  '/forgot-password': (context) => ForgotPasswordScreen(),
  '/deposit': (context) => DepositScreen(),
  '/withdraw': (context) => WithdrawScreen(),
  '/transfer': (context) => TransferScreen(),
  '/transactions': (context) => TransactionsScreen(),
  '/analysis': (context) => AnalysisScreen(),
  '/conflict': (context) => ConflictScreen(),
  '/feedback': (context) => FeedbackScreen(),
  '/about': (context) => AboutScreen(),
  '/profile': (context) => ProfileScreen(),
  '/student-verification': (context) => StudentVerificationScreen(),
};
