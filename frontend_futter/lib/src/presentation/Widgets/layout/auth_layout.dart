import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';

class AuthLayout extends HookWidget {
  final Widget child;

  const AuthLayout({required this.child});

  @override
  Widget build(BuildContext context) {
    final screenWidth = MediaQuery.of(context).size.width;

    return Scaffold(
      resizeToAvoidBottomInset: true,
      body: SafeArea(
        child: Center(
          child: SingleChildScrollView(
            child: Container(
              constraints: BoxConstraints(
                minHeight: MediaQuery.of(context).size.height -
                    MediaQuery.of(context).padding.top -
                    MediaQuery.of(context).padding.bottom,
              ),
              child: child,
            ),
          ),
        ),
      ),
    );
  }
}
