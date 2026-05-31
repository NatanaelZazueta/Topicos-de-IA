import 'dart:convert';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:http/http.dart' as http;
import '../core/constants.dart';

class AuthService {
  final _storage = const FlutterSecureStorage();

  Future<bool> login(String email, String password) async {
    try {
      final resp = await http.post(
        Uri.parse('${AppConstants.apiUrl}${AppConstants.loginEndpoint}'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'email': email, 'password': password}),
      );

      if (resp.statusCode == 200) {
        final data = jsonDecode(resp.body);
        await _storage.write(key: 'token', value: data['access_token']);
        await _storage.write(key: 'nombre', value: data['nombre']);
        await _storage.write(key: 'rol', value: data['rol']);
        return true;
      }
      return false;
    } catch (e) {
      return false;
    }
  }

  Future<String?> getToken() async {
    return await _storage.read(key: 'token');
  }

  Future<String?> getNombre() async {
    return await _storage.read(key: 'nombre');
  }

  Future<void> logout() async {
    await _storage.deleteAll();
  }

  Future<bool> isLoggedIn() async {
    final token = await _storage.read(key: 'token');
    return token != null;
  }
}