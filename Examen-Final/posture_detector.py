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
        
        # Umbrales para determinar mala postura
        self.HEAD_FORWARD_THRESHOLD = 15  # grados
        self.SHOULDER_SLOPE_THRESHOLD = 10  # grados
        self.SPINE_CURVE_THRESHOLD = 20  # grados
        
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
        Analiza si la cabeza está muy adelantada (texto neck)
        """
        # Puntos: nariz, cuello, hombro
        nose = [landmarks[self.mp_pose.PoseLandmark.NOSE.value].x,
                landmarks[self.mp_pose.PoseLandmark.NOSE.value].y]
        
        left_shoulder = [landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                        landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        
        right_shoulder = [landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                         landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
        
        # Punto medio de los hombros
        shoulder_midpoint = [(left_shoulder[0] + right_shoulder[0]) / 2,
                            (left_shoulder[1] + right_shoulder[1]) / 2]
        
        # Calcular desplazamiento horizontal de la cabeza
        head_offset = abs(nose[0] - shoulder_midpoint[0])
        
        # Si la cabeza está muy adelante, es mala postura
        return head_offset > 0.05  # Umbral ajustable
    
    def analyze_shoulder_alignment(self, landmarks):
        """
        Analiza si los hombros están desalineados
        """
        left_shoulder = [landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                        landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        
        right_shoulder = [landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                         landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
        
        # Calcular inclinación de los hombros
        slope = abs(left_shoulder[1] - right_shoulder[1])
        
        # Si hay mucha diferencia en altura, es mala postura
        return slope > 0.03  # Umbral ajustable
    
    def analyze_spine_curvature(self, landmarks):
        """
        Analiza la curvatura de la columna (básico)
        """
        # Puntos: hombros, caderas
        left_shoulder = [landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                        landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        
        right_shoulder = [landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                         landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
        
        left_hip = [landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value].x,
                   landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value].y]
        
        right_hip = [landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                    landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value].y]
        
        # Puntos medios
        shoulder_mid = [(left_shoulder[0] + right_shoulder[0]) / 2,
                       (left_shoulder[1] + right_shoulder[1]) / 2]
        
        hip_mid = [(left_hip[0] + right_hip[0]) / 2,
                  (left_hip[1] + right_hip[1]) / 2]
        
        # Verificar si el torso está muy inclinado
        torso_angle = abs(shoulder_mid[0] - hip_mid[0])
        
        return torso_angle > 0.04  # Umbral ajustable
    
    def detect_posture(self, image):
        """
        Detecta la postura en una imagen
        Args:
            image: Imagen de OpenCV (BGR)
        Returns:
            tuple: (image_with_pose, is_bad_posture, posture_issues)
        """
        # Convertir BGR a RGB
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Procesar con MediaPipe
        results = self.pose.process(rgb_image)
        
        # Dibujar pose en la imagen
        if results.pose_landmarks:
            self.mp_drawing.draw_landmarks(
                image, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)
            
            # Analizar postura
            landmarks = results.pose_landmarks.landmark
            
            posture_issues = []
            
            # Verificar diferentes aspectos de la postura
            if self.analyze_head_position(landmarks):
                posture_issues.append("Cabeza muy adelantada")
            
            if self.analyze_shoulder_alignment(landmarks):
                posture_issues.append("Hombros desalineados")
            
            if self.analyze_spine_curvature(landmarks):
                posture_issues.append("Columna encorvada")
            
            is_bad_posture = len(posture_issues) > 0
            
            return image, is_bad_posture, posture_issues
        
        return image, False, []
    
    def get_pose_landmarks(self, image):
        """
        Obtiene los landmarks de la pose para visualización 3D
        """
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.pose.process(rgb_image)
        
        if results.pose_landmarks:
            return results.pose_landmarks.landmark
        
        return None
