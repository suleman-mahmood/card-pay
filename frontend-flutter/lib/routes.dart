import 'package:cardpay/about/about.dart';
import 'package:cardpay/analysis/analysis.dart';
import 'package:cardpay/conflict/conflict.dart';
import 'package:cardpay/dashboard/dashboard.dart';
import 'package:cardpay/deposit/deposit.dart';
import 'package:cardpay/feedback/feedback.dart';
import 'package:cardpay/forgot_password/forgot_password.dart';
import 'package:cardpay/login/login.dart';
import 'package:cardpay/signup/signup.dart';
import 'package:cardpay/student_verification/student_verification.dart';
import 'package:cardpay/transactions/transactions.dart';
import 'package:cardpay/transfer/transfer.dart';
import 'package:cardpay/welcome/welcome.dart';
import 'package:cardpay/withdraw/withdraw.dart';

var appRoutes = {
  '/': (context) => const WelcomeScreen(),
  '/dashboard': (context) => const DashboardScreen(),
  '/login': (context) => const LoginScreen(),
  '/signup': (context) => const SignUpScreen(),
  '/forgot-password': (context) => const ForgotPasswordScreen(),
  '/deposit': (context) => const DepositScreen(),
  '/withdraw': (context) => const WithdrawScreen(),
  '/transfer': (context) => const TransferScreen(),
  '/transactions': (context) => const TransactionsScreen(),
  '/analysis': (context) => const AnalysisScreen(),
  '/conflict': (context) => const ConflictScreen(),
  '/feedback': (context) => const FeedbackScreen(),
  '/about': (context) => const AboutScreen(),
  '/student-verification': (context) => const StudentVerificationScreen(),
};
