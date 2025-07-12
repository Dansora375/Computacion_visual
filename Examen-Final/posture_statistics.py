"""
🧮 Sistema de Estadísticas de Postura
Recolecta y almacena datos de la sesión actual en memoria
"""

import time
from datetime import datetime, timedelta
from collections import defaultdict

class PostureStatistics:
    """
    Maneja las estadísticas de postura durante la sesión actual
    """
    
    def __init__(self):
        """Inicializa el sistema de estadísticas"""
        self.reset_session()
    
    def reset_session(self):
        """Reinicia todas las estadísticas para una nueva sesión"""
        self.session_start_time = None
        self.session_end_time = None
        
        # Contadores de tiempo
        self.good_posture_time = 0.0  # Segundos en buena postura
        self.bad_posture_time = 0.0   # Segundos en mala postura
        
        # Estado actual
        self.current_posture_state = None  # 'good' o 'bad'
        self.current_state_start_time = None
        
        # Contadores de eventos
        self.problem_counts = defaultdict(int)  # {'head_tilt': 5, 'forward_lean': 3}
        self.alert_count = 0  # Número de alertas (ventanas abiertas)
        
        # Historial para gráficos (últimos 20 puntos)
        self.posture_history = []  # [(timestamp, 'good'/'bad')]
        
        print("📊 Estadísticas de postura reiniciadas")
    
    def start_session(self):
        """Marca el inicio de una nueva sesión"""
        self.session_start_time = time.time()
        print(f"🚀 Sesión iniciada: {datetime.now().strftime('%H:%M:%S')}")
    
    def end_session(self):
        """Marca el final de la sesión actual"""
        if self.session_start_time:
            self.session_end_time = time.time()
            self._update_current_state_time()
            print(f"🛑 Sesión finalizada: {datetime.now().strftime('%H:%M:%S')}")
    
    def update_posture_state(self, is_good_posture, problem_types=None):
        """
        Actualiza el estado actual de la postura
        
        Args:
            is_good_posture (bool): True si la postura es buena
            problem_types (list): Lista de problemas detectados ['head_tilt', 'forward_lean']
        """
        if not self.session_start_time:
            self.start_session()
        
        current_time = time.time()
        new_state = 'good' if is_good_posture else 'bad'
        
        # Si cambió el estado, actualizar tiempos
        if self.current_posture_state != new_state:
            self._update_current_state_time()
            self.current_posture_state = new_state
            self.current_state_start_time = current_time
            
            # Agregar al historial (máximo 20 puntos)
            self.posture_history.append((current_time, new_state))
            if len(self.posture_history) > 20:
                self.posture_history.pop(0)
        
        # Si es mala postura, contar los tipos de problemas
        if not is_good_posture and problem_types:
            for problem in problem_types:
                self.problem_counts[problem] += 1
    
    def log_alert_opened(self):
        """Registra que se abrió una ventana de alerta"""
        self.alert_count += 1
        print(f"🚨 Alerta #{self.alert_count} registrada")
    
    def _update_current_state_time(self):
        """Actualiza el tiempo acumulado del estado actual"""
        if self.current_state_start_time and self.current_posture_state:
            elapsed = time.time() - self.current_state_start_time
            
            if self.current_posture_state == 'good':
                self.good_posture_time += elapsed
            else:
                self.bad_posture_time += elapsed
    
    def get_session_duration(self):
        """Retorna la duración total de la sesión en segundos"""
        if not self.session_start_time:
            return 0
        
        end_time = self.session_end_time or time.time()
        return end_time - self.session_start_time
    
    def get_statistics_summary(self):
        """
        Retorna un resumen completo de las estadísticas
        
        Returns:
            dict: Diccionario con todas las estadísticas
        """
        self._update_current_state_time()
        
        total_duration = self.get_session_duration()
        
        # Calcular porcentajes
        if total_duration > 0:
            good_percentage = (self.good_posture_time / total_duration) * 100
            bad_percentage = (self.bad_posture_time / total_duration) * 100
        else:
            good_percentage = bad_percentage = 0
        
        return {
            'session_duration': total_duration,
            'session_duration_formatted': self._format_duration(total_duration),
            'good_posture_time': self.good_posture_time,
            'good_posture_formatted': self._format_duration(self.good_posture_time),
            'bad_posture_time': self.bad_posture_time,
            'bad_posture_formatted': self._format_duration(self.bad_posture_time),
            'good_percentage': good_percentage,
            'bad_percentage': bad_percentage,
            'problem_counts': dict(self.problem_counts),
            'alert_count': self.alert_count,
            'posture_history': self.posture_history.copy(),
            'session_start': datetime.fromtimestamp(self.session_start_time) if self.session_start_time else None
        }
    
    def _format_duration(self, seconds):
        """Formatea duración en segundos a formato legible MM:SS"""
        if seconds < 60:
            return f"{int(seconds)}s"
        else:
            minutes = int(seconds // 60)
            secs = int(seconds % 60)
            return f"{minutes}:{secs:02d}min"
    
    def export_to_csv(self, filename=None):
        """
        Exporta las estadísticas a un archivo CSV
        
        Args:
            filename (str): Nombre del archivo (opcional)
            
        Returns:
            str: Ruta del archivo creado
        """
        import csv
        import os
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"posture_stats_{timestamp}.csv"
        
        # Crear directorio si no existe
        os.makedirs("estadisticas", exist_ok=True)
        filepath = os.path.join("estadisticas", filename)
        
        stats = self.get_statistics_summary()
        
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Escribir resumen general
            writer.writerow(['RESUMEN DE SESIÓN'])
            writer.writerow(['Métrica', 'Valor'])
            writer.writerow(['Duración Total', stats['session_duration_formatted']])
            writer.writerow(['Tiempo Buena Postura', stats['good_posture_formatted']])
            writer.writerow(['Tiempo Mala Postura', stats['bad_posture_formatted']])
            writer.writerow(['Porcentaje Buena Postura', f"{stats['good_percentage']:.1f}%"])
            writer.writerow(['Porcentaje Mala Postura', f"{stats['bad_percentage']:.1f}%"])
            writer.writerow(['Total de Alertas', stats['alert_count']])
            writer.writerow([])
            
            # Escribir problemas específicos
            writer.writerow(['TIPOS DE PROBLEMAS DETECTADOS'])
            writer.writerow(['Tipo de Problema', 'Cantidad'])
            for problem, count in stats['problem_counts'].items():
                problem_name = self._translate_problem_name(problem)
                writer.writerow([problem_name, count])
        
        print(f"📄 Estadísticas exportadas: {filepath}")
        return filepath
    
    def _translate_problem_name(self, problem_key):
        """Traduce los nombres técnicos de problemas a nombres legibles"""
        translations = {
            'head_tilt_down': 'Cabeza Inclinada Hacia Abajo',
            'forward_lean': 'Inclinación Hacia Adelante', 
            'shoulder_elevation': 'Elevación de Hombros',
            'head_tilt_side': 'Cabeza Inclinada Lateral',
            'asymmetric_shoulders': 'Hombros Asimétricos',
            'excessive_forward_head': 'Cabeza Muy Adelantada'
        }
        return translations.get(problem_key, problem_key.replace('_', ' ').title())

    def print_summary(self):
        """Imprime un resumen de las estadísticas en consola"""
        stats = self.get_statistics_summary()
        
        print("\n" + "="*50)
        print("📊 RESUMEN DE ESTADÍSTICAS DE POSTURA")
        print("="*50)
        print(f"⏱️  Duración de Sesión: {stats['session_duration_formatted']}")
        print(f"✅ Tiempo Buena Postura: {stats['good_posture_formatted']} ({stats['good_percentage']:.1f}%)")
        print(f"❌ Tiempo Mala Postura: {stats['bad_posture_formatted']} ({stats['bad_percentage']:.1f}%)")
        print(f"🚨 Alertas Generadas: {stats['alert_count']}")
        
        if stats['problem_counts']:
            print("\n🔍 Problemas más frecuentes:")
            for problem, count in sorted(stats['problem_counts'].items(), 
                                       key=lambda x: x[1], reverse=True):
                problem_name = self._translate_problem_name(problem)
                print(f"   • {problem_name}: {count} veces")
        
        print("="*50)
