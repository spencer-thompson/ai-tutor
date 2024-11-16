import 'package:flutter/material.dart';
import 'package:playground/basic_chat_ui.dart';
import 'package:playground/qr_code/qr_code.dart';

class SplashPage extends StatelessWidget {
  const SplashPage({super.key});

  @override
  Widget build(BuildContext context) {
    //final bool isLoggedIn = accessToken != null && accessToken!.isNotEmpty;
    final bool isLoggedIn = true;
    final Widget goToPage = isLoggedIn ? BasicApp() : QrApp();
    return goToPage;
  }

  //final String? accessToken;
  //final String? apiVersion;
  //
  //const SplashPage(this.accessToken, this.apiVersion, {super.key});
  //
  //@override
  //Widget build(BuildContext context) {
  //  final bool isLoggedIn = accessToken != null && accessToken!.isNotEmpty;
  //  final Widget goToPage =
  //      isLoggedIn ? HomePage(accessToken, apiVersion) : LoginPage();
  //  return goToPage;
  //}
}
