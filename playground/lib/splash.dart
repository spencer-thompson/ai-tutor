import 'package:flutter/material.dart';
import 'package:playground/basic_chat_ui.dart';
import 'package:playground/qr_code/qr_code.dart';

class SplashPage extends StatefulWidget {
  const SplashPage({super.key});

  @override
  State<SplashPage> createState() => _SplashPageState();
}

class _SplashPageState extends State<SplashPage> {
  String? qrToken;

  void _setQrToken(String updatedQrToken) {
    setState(() {
      qrToken = updatedQrToken;
    });
  }

  @override
  Widget build(BuildContext context) {
    final bool isLoggedIn = qrToken != null && qrToken!.isNotEmpty;
    //final bool isLoggedIn = true;
    print("WE ARE HERE\n\n\n\n\n\n\n\n\n\n\n\n#################!!!!!!");
    final Widget goToPage = isLoggedIn
        ? MyHomePage()
        : QrApp(
            qrToken: qrToken,
            onQrTokenUpdate: _setQrToken); //BarcodeScannerWithOverlay();
    //return goToPage;
    return Scaffold(
      body: goToPage,
    );
    //return MyHomePage();
  }
}
