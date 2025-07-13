"""
Módulo de detección de postura corporal usando MediaPipe
Analiza la postura del usuario y determina si es correcta o incorrecta
"""

import cv2
import mediapipe as mp
import numpy as np
import math

class PostureDetector:
    def __init__(self):
        """
        Inicializa el detector de postura usando MediaPipe Pose
        """
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            enable_segmentation=False,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils
        
        # === SISTEMA DE CALIBRACIÓN ===
        self.is_calibrated = False
        self.calibration_data = None
        self.calibration_frames = []
        self.calibration_frame_count = 0
        self.CALIBRATION_FRAMES_NEEDED = 90  # 3 segundos a 30 FPS para mejor calibración
        
        # === FILTRADO TEMPORAL MÁS TOLERANTE ===
        self.posture_history = []
        self.HISTORY_SIZE = 8  # Más frames para suavizar
        self.BAD_POSTURE_THRESHOLD = 0.6  # Más tolerante (60% en lugar de 40%)
        
        # === UMBRALES ADAPTATIVOS RELAJADOS ===
        self.head_forward_threshold = 0.08  # Menos estricto
        self.shoulder_height_threshold = 0.04  # Menos estricto
        self.shoulder_elevation_threshold = 15  # Menos estricto
        self.spine_angle_threshold = 20  # Menos estricto
        self.neck_angle_threshold = 25  # Menos estricto
        
    def calculate_angle(self, point1, point2, point3):
        """
        Calcula el ángulo entre tres puntos
        Args:
            point1, point2, point3: Puntos en formato [x, y]
        Returns:
            Ángulo en grados
        """
        # Vectores
        vector1 = np.array(point1) - np.array(point2)
        vector2 = np.array(point3) - np.array(point2)
        
        # Calcular ángulo
        cosine_angle = np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2))
        cosine_angle = np.clip(cosine_angle, -1.0, 1.0)
        angle = np.arccos(cosine_angle)
        
        return np.degrees(angle)
    
    def analyze_head_position(self, landmarks):
        """
        Analiza si la cabeza está muy adelantada usando coordenadas Z y ángulo del cuello
        Más tolerante con valores de calibración
        """
        if not self.is_calibrated:
            return False
        
        points = self.extract_key_points(landmarks)
        measurements = self.calculate_posture_measurements(points)
        
        # Comparar con valores de calibración de manera más tolerante
        head_forward_distance = measurements['head_forward_distance']
        neck_angle = abs(measurements['neck_angle'])
        
        # Usar los valores de calibración como referencia base
        calibrated_head_distance = self.calibration_data['head_forward_distance']
        calibrated_neck_angle = abs(self.calibration_data['neck_angle'])
        
        # Detectar cabeza adelantada solo si excede significativamente los valores calibrados
        head_forward_exceeded = head_forward_distance > (calibrated_head_distance + self.head_forward_threshold)
        neck_angle_exceeded = neck_angle > (calibrated_neck_angle + self.neck_angle_threshold)
        
        # Solo reportar problema si ambos indicadores están mal O uno está muy mal
        is_head_forward = (head_forward_exceeded and neck_angle_exceeded) or \
                         (head_forward_distance > calibrated_head_distance * 2.0) or \
                         (neck_angle > calibrated_neck_angle * 2.0)
        
        return is_head_forward
    
    def analyze_shoulder_alignment(self, landmarks):
        """
        Analiza desalineación de hombros (altura) y elevación excesiva
        Más tolerante con valores de calibración
        """
        if not self.is_calibrated:
            return False
        
        points = self.extract_key_points(landmarks)
        measurements = self.calculate_posture_measurements(points)
        
        # Usar valores de calibración como referencia
        height_diff = measurements['shoulder_height_diff']
        calibrated_height_diff = self.calibration_data['shoulder_height_diff']
        
        # Solo reportar problema si la diferencia es significativamente mayor que en calibración
        is_height_misaligned = height_diff > (calibrated_height_diff + self.shoulder_height_threshold)
        
        # Verificar elevación excesiva (hombros muy levantados)
        elevation_angle = abs(measurements['shoulder_elevation_angle'])
        calibrated_elevation = abs(self.calibration_data['shoulder_elevation_angle'])
        
        # Solo reportar si la elevación excede significativamente la calibración
        is_elevated = elevation_angle > (calibrated_elevation + self.shoulder_elevation_threshold)
        
        # Ambos problemas deben ser evidentes para reportar
        return is_height_misaligned and is_elevated
    
    def analyze_spine_curvature(self, landmarks):
        """
        Analiza la curvatura excesiva de la columna
        Más tolerante con valores de calibración
        """
        if not self.is_calibrated:
            return False
        
        points = self.extract_key_points(landmarks)
        measurements = self.calculate_posture_measurements(points)
        
        # Usar valor de calibración como referencia
        spine_angle = abs(measurements['spine_angle'])
        calibrated_spine_angle = abs(self.calibration_data['spine_angle'])
        
        # Solo reportar si el ángulo excede significativamente el valor calibrado
        is_spine_curved = spine_angle > (calibrated_spine_angle + self.spine_angle_threshold)
        
        return is_spine_curved
    
    def analyze_shoulder_elevation(self, landmarks):
        """
        Analiza específicamente si los hombros están muy levantados
        """
        if not self.is_calibrated:
            return False
        
        points = self.extract_key_points(landmarks)
        
        # Calcular altura de hombros relativa a las caderas
        shoulder_mid_y = (points['left_shoulder'][1] + points['right_shoulder'][1]) / 2
        hip_mid_y = (points['left_hip'][1] + points['right_hip'][1]) / 2
        
        # En calibración, calcular la distancia normal hombro-cadera
        calibration_shoulder_hip_distance = None
        if hasattr(self, 'calibration_data') and self.calibration_data:
            # Calcular distancia promedio durante calibración
            distances = []
            for frame in self.calibration_frames:
                frame_shoulder_y = (frame['left_shoulder'][1] + frame['right_shoulder'][1]) / 2
                frame_hip_y = (frame['left_hip'][1] + frame['right_hip'][1]) / 2
                distances.append(abs(frame_hip_y - frame_shoulder_y))
            calibration_shoulder_hip_distance = np.mean(distances)
        
        # Comparar distancia actual vs calibración
        current_distance = abs(hip_mid_y - shoulder_mid_y)
        
        if calibration_shoulder_hip_distance:
            # Si la distancia es significativamente menor, los hombros están levantados
            distance_reduction = calibration_shoulder_hip_distance - current_distance
            threshold = calibration_shoulder_hip_distance * 0.15  # 15% de reducción
            return distance_reduction > threshold
        
        return False
    
    def detect_posture(self, image):
        """
        Detecta la postura en una imagen con sistema de calibración y filtrado temporal
        Args:
            image: Imagen de OpenCV (BGR)
        Returns:
            tuple: (image_with_pose, is_bad_posture, posture_issues, calibration_status)
        """
        # Convertir BGR a RGB
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Procesar con MediaPipe
        results = self.pose.process(rgb_image)
        
        # Dibujar pose en la imagen
        if results.pose_landmarks:
            self.mp_drawing.draw_landmarks(
                image, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)
            
            landmarks = results.pose_landmarks.landmark
            
            # Si no está calibrado, continuar con calibración
            if not self.is_calibrated:
                calibration_complete = self.add_calibration_frame(landmarks)
                progress = (self.calibration_frame_count / self.CALIBRATION_FRAMES_NEEDED) * 100
                return image, False, [], {'calibrating': True, 'progress': progress, 'complete': calibration_complete}
            
            # Análisis de postura con nuevos métodos mejorados
            posture_issues = []
            
            # Verificar diferentes aspectos de la postura
            if self.analyze_head_position(landmarks):
                posture_issues.append("Cabeza muy adelantada")
            
            if self.analyze_head_tilt_down(landmarks):
                posture_issues.append("Cabeza inclinada hacia abajo")
            
            if self.analyze_shoulder_alignment(landmarks):
                posture_issues.append("Hombros desalineados/elevados")
            
            if self.analyze_spine_curvature(landmarks):
                posture_issues.append("Columna encorvada")
            
            if self.analyze_shoulder_elevation(landmarks):
                posture_issues.append("Hombros muy levantados")
            
            if self.analyze_forward_lean(landmarks):
                posture_issues.append("Cuerpo inclinado hacia adelante")
            
            # Aplicar filtrado temporal
            current_bad_posture = len(posture_issues) > 0
            self.posture_history.append(current_bad_posture)
            
            # Mantener historial de tamaño fijo
            if len(self.posture_history) > self.HISTORY_SIZE:
                self.posture_history.pop(0)
            
            # Determinar postura final basada en historial
            if len(self.posture_history) >= self.HISTORY_SIZE:
                bad_posture_ratio = sum(self.posture_history) / len(self.posture_history)
                final_bad_posture = bad_posture_ratio >= self.BAD_POSTURE_THRESHOLD
            else:
                # Si no hay suficiente historial, usar detección actual
                final_bad_posture = current_bad_posture
            
            return image, final_bad_posture, posture_issues, {'calibrating': False, 'progress': 100, 'complete': True}
        
        # Si no se detecta pose
        return image, False, [], {'calibrating': not self.is_calibrated, 'progress': 0, 'complete': False}
    def start_calibration(self):
        """
        Inicia el proceso de calibración
        """
        self.is_calibrated = False
        self.calibration_frames = []
        self.calibration_frame_count = 0
        print("🎯 Iniciando calibración de postura correcta...")
        print("📏 Mantén una postura CORRECTA durante 3 segundos")
    
    def add_calibration_frame(self, landmarks):
        """
        Añade un frame a la calibración
        """
        if self.calibration_frame_count < self.CALIBRATION_FRAMES_NEEDED:
            # Extraer puntos clave para calibración
            calibration_points = self.extract_key_points(landmarks)
            self.calibration_frames.append(calibration_points)
            self.calibration_frame_count += 1
            
            # Mostrar progreso
            progress = (self.calibration_frame_count / self.CALIBRATION_FRAMES_NEEDED) * 100
            if self.calibration_frame_count % 10 == 0:
                print(f"📊 Calibración: {progress:.0f}%")
            
            return False  # Aún no terminado
        else:
            self.complete_calibration()
            return True  # Calibración completada
    
    def extract_key_points(self, landmarks):
        """
        Extrae puntos clave para análisis de postura
        """
        points = {}
        
        # Cabeza y cuello
        points['nose'] = [landmarks[self.mp_pose.PoseLandmark.NOSE.value].x,
                         landmarks[self.mp_pose.PoseLandmark.NOSE.value].y,
                         landmarks[self.mp_pose.PoseLandmark.NOSE.value].z]
        
        points['left_ear'] = [landmarks[self.mp_pose.PoseLandmark.LEFT_EAR.value].x,
                             landmarks[self.mp_pose.PoseLandmark.LEFT_EAR.value].y,
                             landmarks[self.mp_pose.PoseLandmark.LEFT_EAR.value].z]
        
        points['right_ear'] = [landmarks[self.mp_pose.PoseLandmark.RIGHT_EAR.value].x,
                              landmarks[self.mp_pose.PoseLandmark.RIGHT_EAR.value].y,
                              landmarks[self.mp_pose.PoseLandmark.RIGHT_EAR.value].z]
        
        # Hombros
        points['left_shoulder'] = [landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                                  landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].y,
                                  landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].z]
        
        points['right_shoulder'] = [landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                                   landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y,
                                   landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].z]
        
        # Caderas
        points['left_hip'] = [landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value].x,
                             landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value].y,
                             landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value].z]
        
        points['right_hip'] = [landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                              landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value].y,
                              landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value].z]
        
        return points
    
    def complete_calibration(self):
        """
        Completa la calibración calculando valores de referencia
        """
        if len(self.calibration_frames) < self.CALIBRATION_FRAMES_NEEDED:
            print("❌ Error: No hay suficientes frames para calibración")
            return
        
        # Calcular promedios de postura correcta
        self.calibration_data = {}
        
        # Promediar todas las mediciones
        all_measurements = []
        for frame in self.calibration_frames:
            measurements = self.calculate_posture_measurements(frame)
            all_measurements.append(measurements)
        
        # Calcular valores de referencia (promedios)
        self.calibration_data = {
            'head_forward_distance': np.mean([m['head_forward_distance'] for m in all_measurements]),
            'shoulder_height_diff': np.mean([m['shoulder_height_diff'] for m in all_measurements]),
            'neck_angle': np.mean([m['neck_angle'] for m in all_measurements]),
            'spine_angle': np.mean([m['spine_angle'] for m in all_measurements]),
            'shoulder_elevation_angle': np.mean([m['shoulder_elevation_angle'] for m in all_measurements])
        }
        
        # Calcular umbrales adaptativos basados en desviación estándar
        std_multiplier = 2.5  # Más tolerante que antes (era 1.5)
        base_tolerance = 1.3  # Factor adicional para mayor tolerancia
        
        self.head_forward_threshold = (self.calibration_data['head_forward_distance'] + (
            std_multiplier * np.std([m['head_forward_distance'] for m in all_measurements]))) * base_tolerance
        
        self.shoulder_height_threshold = (self.calibration_data['shoulder_height_diff'] + (
            std_multiplier * np.std([m['shoulder_height_diff'] for m in all_measurements]))) * base_tolerance
        
        self.neck_angle_threshold = (abs(self.calibration_data['neck_angle']) + (
            std_multiplier * np.std([m['neck_angle'] for m in all_measurements]))) * base_tolerance
        
        self.spine_angle_threshold = (abs(self.calibration_data['spine_angle']) + (
            std_multiplier * np.std([m['spine_angle'] for m in all_measurements]))) * base_tolerance
        
        self.shoulder_elevation_threshold = (abs(self.calibration_data['shoulder_elevation_angle']) + (
            std_multiplier * np.std([m['shoulder_elevation_angle'] for m in all_measurements]))) * base_tolerance
        
        self.is_calibrated = True
        print("✅ Calibración completada exitosamente!")
        print(f"📊 Umbrales adaptativos calculados:")
        print(f"   • Cabeza adelantada: {self.head_forward_threshold:.3f}")
        print(f"   • Diferencia hombros: {self.shoulder_height_threshold:.3f}")
        print(f"   • Ángulo cuello: {self.neck_angle_threshold:.1f}°")
        print(f"   • Ángulo columna: {self.spine_angle_threshold:.1f}°")
        print(f"   • Elevación hombros: {self.shoulder_elevation_threshold:.1f}°")
    
    def calculate_posture_measurements(self, points):
        """
        Calcula todas las mediciones de postura para un conjunto de puntos
        """
        measurements = {}
        
        # 1. Distancia de cabeza adelantada (usando coordenadas Z)
        nose_z = points['nose'][2]
        shoulder_mid_z = (points['left_shoulder'][2] + points['right_shoulder'][2]) / 2
        measurements['head_forward_distance'] = abs(nose_z - shoulder_mid_z)
        
        # 2. Diferencia de altura entre hombros
        measurements['shoulder_height_diff'] = abs(points['left_shoulder'][1] - points['right_shoulder'][1])
        
        # 3. Ángulo del cuello (usando oreja, hombro y vertical)
        ear_mid = [(points['left_ear'][0] + points['right_ear'][0]) / 2,
                   (points['left_ear'][1] + points['right_ear'][1]) / 2]
        shoulder_mid = [(points['left_shoulder'][0] + points['right_shoulder'][0]) / 2,
                       (points['left_shoulder'][1] + points['right_shoulder'][1]) / 2]
        
        # Ángulo entre línea oreja-hombro y vertical
        neck_vector = [ear_mid[0] - shoulder_mid[0], ear_mid[1] - shoulder_mid[1]]
        vertical_vector = [0, -1]  # Hacia arriba
        measurements['neck_angle'] = self.calculate_angle_between_vectors(neck_vector, vertical_vector)
        
        # 4. Ángulo de la columna (hombros a caderas)
        hip_mid = [(points['left_hip'][0] + points['right_hip'][0]) / 2,
                   (points['left_hip'][1] + points['right_hip'][1]) / 2]
        
        spine_vector = [shoulder_mid[0] - hip_mid[0], shoulder_mid[1] - hip_mid[1]]
        measurements['spine_angle'] = self.calculate_angle_between_vectors(spine_vector, vertical_vector)
        
        # 5. Ángulo de elevación de hombros
        shoulder_vector = [points['right_shoulder'][0] - points['left_shoulder'][0],
                          points['right_shoulder'][1] - points['left_shoulder'][1]]
        horizontal_vector = [1, 0]
        measurements['shoulder_elevation_angle'] = self.calculate_angle_between_vectors(shoulder_vector, horizontal_vector)
        
        return measurements
    
    def calculate_angle_between_vectors(self, vector1, vector2):
        """
        Calcula el ángulo entre dos vectores en grados
        """
        v1 = np.array(vector1)
        v2 = np.array(vector2)
        
        # Normalizar vectores
        v1_norm = v1 / np.linalg.norm(v1)
        v2_norm = v2 / np.linalg.norm(v2)
        
        # Calcular ángulo
        dot_product = np.dot(v1_norm, v2_norm)
        dot_product = np.clip(dot_product, -1.0, 1.0)
        angle = np.arccos(dot_product)
        
        return np.degrees(angle)
    def analyze_head_tilt_down(self, landmarks):
        """
        Detecta específicamente cuando la cabeza está inclinada hacia abajo (mirando pantalla)
        """
        if not self.is_calibrated:
            return False
        
        # Usar orejas y nariz para detectar inclinación hacia abajo
        nose = landmarks[self.mp_pose.PoseLandmark.NOSE.value]
        left_ear = landmarks[self.mp_pose.PoseLandmark.LEFT_EAR.value]
        right_ear = landmarks[self.mp_pose.PoseLandmark.RIGHT_EAR.value]
        
        # Calcular la inclinación de la cabeza
        ear_mid_y = (left_ear.y + right_ear.y) / 2
        nose_y = nose.y
        
        # Si la nariz está significativamente más abajo que las orejas, la cabeza está caída
        head_tilt = nose_y - ear_mid_y
        
        # Comparar con calibración
        if hasattr(self, 'calibration_data'):
            # Durante calibración, calcular inclinación normal
            calibration_tilts = []
            for frame in self.calibration_frames:
                frame_ear_y = (frame['left_ear'][1] + frame['right_ear'][1]) / 2
                frame_nose_y = frame['nose'][1]
                calibration_tilts.append(frame_nose_y - frame_ear_y)
            
            normal_tilt = np.mean(calibration_tilts)
            tilt_threshold = normal_tilt + 0.02  # Umbral de 2cm hacia abajo
            
            return head_tilt > tilt_threshold
        
        return False
    
    def analyze_forward_lean(self, landmarks):
        """
        Detecta inclinación del cuerpo hacia adelante (encorvamiento)
        """
        if not self.is_calibrated:
            return False
        
        # Usar hombros y caderas para detectar inclinación frontal
        left_shoulder = landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        left_hip = landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value]
        right_hip = landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value]
        
        # Calcular coordenadas Z promedio
        shoulder_z = (left_shoulder.z + right_shoulder.z) / 2
        hip_z = (left_hip.z + right_hip.z) / 2
        
        # Inclinación hacia adelante: hombros más cerca de la cámara que caderas
        forward_lean = hip_z - shoulder_z
        
        # Comparar con calibración
        if hasattr(self, 'calibration_data'):
            calibration_leans = []
            for frame in self.calibration_frames:
                frame_shoulder_z = (frame['left_shoulder'][2] + frame['right_shoulder'][2]) / 2
                frame_hip_z = (frame['left_hip'][2] + frame['right_hip'][2]) / 2
                calibration_leans.append(frame_hip_z - frame_shoulder_z)
            
            normal_lean = np.mean(calibration_leans)
            lean_threshold = normal_lean - 0.03  # Umbral de inclinación hacia adelante
            
            return forward_lean < lean_threshold
        
        return False
