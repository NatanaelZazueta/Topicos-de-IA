import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
import 'package:image/image.dart' as img;
import '../models/estudiante.dart';
import '../services/auth_service.dart';
import '../services/recognition_service.dart';

class RecognitionScreen extends StatefulWidget {
  const RecognitionScreen({super.key});
  @override
  State<RecognitionScreen> createState() => _RecognitionScreenState();
}

class _RecognitionScreenState extends State<RecognitionScreen> {
  CameraController? _camera;
  final _recognitionSvc = RecognitionService();
  final _authSvc        = AuthService();
  Estudiante? _estudiante;
  bool _processing      = false;
  int  _frameCount      = 0;
  bool _initialized     = false;
  DateTime? _ultimaDeteccion;

  @override
  void initState() {
    super.initState();
    _initCamera();
  }

  Future<void> _initCamera() async {
    await _recognitionSvc.initialize();
    final cameras = await availableCameras();
    final front = cameras.firstWhere(
      (c) => c.lensDirection == CameraLensDirection.front,
      orElse: () => cameras.first,
    );
    _camera = CameraController(front, ResolutionPreset.medium,
        imageFormatGroup: ImageFormatGroup.yuv420);
    await _camera!.initialize();
    _camera!.startImageStream(_onFrame);
    setState(() => _initialized = true);
  }

  void _onFrame(CameraImage camImg) async {
    _frameCount++;
    if (_frameCount % 25 != 0 || _processing) return;
    _processing = true;

    try {
      final token = await _authSvc.getToken();
      if (token == null) return;

      // Convertir YUV420 a RGB
      final rgbImg = _yuv420ToRgb(camImg);
      if (rgbImg == null) return;

      // Enviar imagen completa al backend
      final resultado = await _recognitionSvc.identificarDesdeImagen(rgbImg, token);

      if (mounted) {
        setState(() {
          if (resultado != null) {
            _estudiante      = resultado;
            _ultimaDeteccion = DateTime.now();
          } else {
            // Limpiar después de 3 segundos sin detección
            final ahora = DateTime.now();
            if (_ultimaDeteccion == null ||
                ahora.difference(_ultimaDeteccion!).inSeconds > 3) {
              _estudiante = null;
            }
          }
        });
      }
    } finally {
      _processing = false;
    }
  }

  img.Image? _yuv420ToRgb(CameraImage camImg) {
    try {
      final yPlane = camImg.planes[0];
      final uPlane = camImg.planes[1];
      final vPlane = camImg.planes[2];
      final w = camImg.width;
      final h = camImg.height;
      final out = img.Image(width: w, height: h);

      for (int y = 0; y < h; y++) {
        for (int x = 0; x < w; x++) {
          final yVal   = yPlane.bytes[y * yPlane.bytesPerRow + x];
          final uvIdx  = (y ~/ 2) * uPlane.bytesPerRow +
              (x ~/ 2) * uPlane.bytesPerPixel!;
          final uVal   = uPlane.bytes[uvIdx];
          final vVal   = vPlane.bytes[uvIdx];

          final r = (yVal + 1.402 * (vVal - 128)).clamp(0, 255).toInt();
          final g = (yVal - 0.344136 * (uVal - 128) -
                  0.714136 * (vVal - 128))
              .clamp(0, 255).toInt();
          final b = (yVal + 1.772 * (uVal - 128)).clamp(0, 255).toInt();
          out.setPixelRgb(x, y, r, g, b);
        }
      }
      return out;
    } catch (_) {
      return null;
    }
  }

  @override
  void dispose() {
    _camera?.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    if (!_initialized || _camera == null) {
      return const Scaffold(
        backgroundColor: Color(0xFF0A0A0F),
        body: Center(
            child: CircularProgressIndicator(color: Color(0xFF6C63FF))),
      );
    }

    return Scaffold(
      backgroundColor: Colors.black,
      body: Stack(children: [
        SizedBox.expand(child: CameraPreview(_camera!)),

        if (_estudiante != null)
          Positioned(
            bottom: 0, left: 0, right: 0,
            child: Container(
              padding: const EdgeInsets.all(20),
              decoration: const BoxDecoration(
                color: Color(0xEE0A0A0F),
                borderRadius:
                    BorderRadius.vertical(top: Radius.circular(20)),
              ),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(children: [
                    const Icon(Icons.check_circle,
                        color: Color(0xFF00D4AA), size: 20),
                    const SizedBox(width: 8),
                    const Text('IDENTIFICADO',
                        style: TextStyle(
                            color: Color(0xFF00D4AA),
                            fontSize: 12,
                            fontWeight: FontWeight.bold,
                            letterSpacing: 1.5)),
                    const Spacer(),
                    Text(
                        '${(_estudiante!.confianza * 100).toStringAsFixed(1)}%',
                        style: const TextStyle(
                            color: Color(0xFF6C63FF),
                            fontWeight: FontWeight.bold)),
                  ]),
                  const SizedBox(height: 10),
                  Text(_estudiante!.nombre,
                      style: const TextStyle(
                          color: Colors.white,
                          fontSize: 20,
                          fontWeight: FontWeight.bold)),
                  const SizedBox(height: 4),
                  Text(_estudiante!.carrera,
                      style: const TextStyle(
                          color: Colors.white70, fontSize: 14)),
                  const SizedBox(height: 4),
                  Row(children: [
                    _chip('ID: ${_estudiante!.id}'),
                    const SizedBox(width: 8),
                    _chip('Semestre ${_estudiante!.semestre}'),
                  ]),
                ],
              ),
            ),
          ),

        if (_estudiante == null)
          Positioned(
            bottom: 24, left: 0, right: 0,
            child: Center(
              child: Container(
                padding: const EdgeInsets.symmetric(
                    horizontal: 16, vertical: 8),
                decoration: BoxDecoration(
                  color: Colors.black54,
                  borderRadius: BorderRadius.circular(20),
                ),
                child: const Text('Apunta la cámara a un estudiante',
                    style: TextStyle(color: Colors.white70)),
              ),
            ),
          ),

        Positioned(
          top: 48, right: 16,
          child: IconButton(
            icon: const Icon(Icons.logout, color: Colors.white70),
            onPressed: () async {
              await _authSvc.logout();
              if (mounted) Navigator.pushReplacementNamed(context, '/');
            },
          ),
        ),
      ]),
    );
  }

  Widget _chip(String text) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
      decoration: BoxDecoration(
        color: const Color(0xFF1E1E2E),
        borderRadius: BorderRadius.circular(6),
        border: Border.all(color: const Color(0xFF6C63FF), width: 0.5),
      ),
      child: Text(text,
          style: const TextStyle(color: Color(0xFF9D97FF), fontSize: 12)),
    );
  }
}