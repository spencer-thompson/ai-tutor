import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';

class HeaderManager extends ChangeNotifier {
  String? _apiKey;
  String? _jwt;

  String? get apiKey => _apiKey;
  String? get jwt => _jwt;

  HeaderManager() {
    _loadHeaders();
  }

  void _loadHeaders() async {
    final prefs = await SharedPreferences.getInstance();
    _jwt = prefs.getString('jwt');
    _apiKey = dotenv.env['API_KEY'];
    notifyListeners();
  }

  Future<void> updateHeaders(String jwt) async {
    _jwt = jwt;

    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('jwt', jwt);

    notifyListeners();
  }
}
