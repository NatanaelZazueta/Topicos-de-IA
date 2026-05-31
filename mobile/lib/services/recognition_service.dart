import 'dart:convert';
import 'dart:typed_data';
import 'package:http/http.dart' as http;
import 'package:image/image.dart' as img;
import '../core/constants.dart';
import '../models/estudiante.dart';

class RecognitionService {
  // Ya no necesitamos ONNX en el celular
  Future<void> initialize() async {}

  Future<Estudiante?> identificarDesdeImagen(
      img.Image imagen, String token) async {
    try {
      // Codificar imagen como JPEG
      final jpegBytes = img.encodeJpg(imagen, quality: 85);

      final request = http.MultipartRequest(
        'POST',
        Uri.parse('${AppConstants.apiUrl}${AppConstants.identificarEndpoint}'),
      );

      request.headers['Authorization'] = 'Bearer $token';
      request.files.add(http.MultipartFile.fromBytes(
        'file',
        jpegBytes,
        filename: 'frame.jpg',
      ));

      final response = await request.send().timeout(const Duration(seconds: 5));
      final body     = await response.stream.bytesToString();

      if (response.statusCode == 200) {
        final data = jsonDecode(body);
        if (data['status'] == 'IDENTIFICADO') {
          return Estudiante.fromJson(data);
        }
      }
      return null;
    } catch (e) {
      return null;
    }
  }
}