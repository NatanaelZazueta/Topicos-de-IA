import 'package:flutter/material.dart';
import '../services/auth_service.dart';
import 'recognition_screen.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});
  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _emailCtrl    = TextEditingController(text: 'admin@itc.edu');
  final _passwordCtrl = TextEditingController(text: 'admin123');
  bool _loading = false;
  String? _error;

  Future<void> _login() async {
    setState(() { _loading = true; _error = null; });
    final auth = AuthService();
    final ok = await auth.login(_emailCtrl.text.trim(), _passwordCtrl.text.trim());
    setState(() => _loading = false);

    if (ok && mounted) {
      Navigator.pushReplacement(context,
          MaterialPageRoute(builder: (_) => const RecognitionScreen()));
    } else {
      setState(() => _error = 'Credenciales incorrectas');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0A0A0F),
      body: Center(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(32),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Icon(Icons.face, size: 72, color: Color(0xFF6C63FF)),
              const SizedBox(height: 16),
              const Text('FaceRec EDU',
                  style: TextStyle(fontSize: 28, fontWeight: FontWeight.bold,
                      color: Colors.white)),
              const Text('Sistema de Reconocimiento Facial',
                  style: TextStyle(color: Colors.white54, fontSize: 13)),
              const SizedBox(height: 40),
              TextField(
                controller: _emailCtrl,
                style: const TextStyle(color: Colors.white),
                decoration: _inputDecoration('Correo institucional'),
                keyboardType: TextInputType.emailAddress,
              ),
              const SizedBox(height: 16),
              TextField(
                controller: _passwordCtrl,
                obscureText: true,
                style: const TextStyle(color: Colors.white),
                decoration: _inputDecoration('Contraseña'),
              ),
              if (_error != null) ...[
                const SizedBox(height: 12),
                Text(_error!, style: const TextStyle(color: Colors.redAccent)),
              ],
              const SizedBox(height: 24),
              SizedBox(
                width: double.infinity,
                height: 50,
                child: ElevatedButton(
                  onPressed: _loading ? null : _login,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: const Color(0xFF6C63FF),
                    shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(10)),
                  ),
                  child: _loading
                      ? const CircularProgressIndicator(color: Colors.white)
                      : const Text('INGRESAR',
                          style: TextStyle(fontSize: 16,
                              fontWeight: FontWeight.bold, color: Colors.white)),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  InputDecoration _inputDecoration(String label) {
    return InputDecoration(
      labelText: label,
      labelStyle: const TextStyle(color: Colors.white54),
      filled: true,
      fillColor: const Color(0xFF1E1E2E),
      border: OutlineInputBorder(borderRadius: BorderRadius.circular(10),
          borderSide: BorderSide.none),
      focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(10),
          borderSide: const BorderSide(color: Color(0xFF6C63FF))),
    );
  }
}