import 'package:flutter/material.dart';
import 'package:frontend/utils/constants.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import 'package:frontend/pages/splash_page.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';

// Error occurs when signing up because email has not yet been verified

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  await dotenv.load(fileName: "secrets.env");

  String? supabase_url = dotenv.env['SUPABASE_URL'];
  String? anon_key = dotenv.env['SUPABASE_ANON_KEY'];

  if (supabase_url != null && anon_key != null) {
    await Supabase.initialize(
      url: supabase_url,
      anonKey: anon_key,
    );
  }
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'My Chat App',
      theme: appTheme,
      home: const SplashPage(),
    );
  }
}
