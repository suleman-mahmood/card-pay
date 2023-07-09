import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';

class AuthLayout extends HookWidget {
  final Widget child;
  final bool scrollable;

  const AuthLayout({
    required this.child,
    this.scrollable = true,
  });

  @override
  Widget build(BuildContext context) {
    final screenHeight = MediaQuery.of(context).size.height;
    final screenPaddingTop = MediaQuery.of(context).padding.top;
    final screenPaddingBottom = MediaQuery.of(context).padding.bottom;

    Widget content = Center(
      child: Container(
        constraints: BoxConstraints(
          minHeight: screenHeight - screenPaddingTop - screenPaddingBottom,
        ),
        child: child,
      ),
    );

    final childToRender =
        scrollable ? SingleChildScrollView(child: content) : content;

    return Scaffold(
      resizeToAvoidBottomInset: true,
      body: SafeArea(
        child: Padding(
          padding: EdgeInsets.symmetric(
              horizontal: MediaQuery.of(context).size.width * 0.088),
          child: childToRender,
        ),
      ),
    );
  }
}
