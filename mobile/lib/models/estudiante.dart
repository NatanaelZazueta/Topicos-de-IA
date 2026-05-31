class Estudiante {
  final String id;
  final String nombre;
  final String carrera;
  final int semestre;
  final double confianza;

  Estudiante({
    required this.id,
    required this.nombre,
    required this.carrera,
    required this.semestre,
    required this.confianza,
  });

  factory Estudiante.fromJson(Map<String, dynamic> json) {
    return Estudiante(
      id:        json['id'] ?? '',
      nombre:    json['nombre'] ?? '',
      carrera:   json['carrera'] ?? '',
      semestre:  json['semestre'] ?? 0,
      confianza: (json['confianza'] ?? 0).toDouble(),
    );
  }
}