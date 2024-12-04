import 'dart:convert';
import 'dart:math';
import 'package:flutter/material.dart';
import 'package:playground/splash.dart';
import 'package:playground/basic_chat_ui.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';

import 'package:provider/provider.dart';
import 'package:playground/header_manager.dart';

//import 'package:playground/qr_code/qr_code.dart';

//import 'package:playground/markdown_2.dart';

// it would be cool to have the user press a key for which 'version' of main they want to run. That way I could have multiple
// main.dart's within the same flutter project. I'm thinking of adding a terminal command of sorts
//flutter run -d chrome web-server --web-port 1234

String randomString() {
  final random = Random.secure();
  final values = List<int>.generate(16, (i) => random.nextInt(255));
  return base64UrlEncode(values);
}

void main() async {
  //SystemChrome.setSystemUIOverlayStyle(const SystemUiOverlayStyle(
  //  //statusBarColor: Colors.pink,
  //  systemNavigationBarColor: Colors.black,
  //  systemNavigationBarIconBrightness: Brightness.light,
  //));
  //runApp(const MyApp());
  //runApp(QrApp());

  //runApp(const BasicApp());
  //runApp(const SideDrawer());
  //runApp(const SplashPage());
  await dotenv.load();
  runApp(ChangeNotifierProvider(
      create: (_) => HeaderManager(), child: const MyApp()));
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: '!RScanner App',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: const SplashPage(),
    );
  }
}

//
//curl https://api.aitutor.live/user -H "AITUTOR-API-KEY: <the_key>" -H "Authorization: Bearer <the_token>"
//
//the key is the key
//L52XnyeWj9PfPVZ5Uef8scMr0XgYYrQ0PNm1V6w0gvs
//
//qr_code string is the token
//
//check out api.aitutor.live/docs
//
//Make a get request first with whatever jwt I have
//
//api.aitutor.live/v1/smart_chat_stream --> always include the same headers
//--> This is the endpoint that
