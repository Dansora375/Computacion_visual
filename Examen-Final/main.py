"""
Sistema de Detección de Postura Corporal en Tiempo Real
Integra detección de postura con visualización 3D interactiva y estadísticas

Autor: Sistema de Análisis Postural
Fecha: Julio 2025
"""

import cv2
import time
import threading
from posture_detector import PostureDetector
from pose_3d_visualizer import Pose3DVisualizer
from posture_statistics import PostureStatistics
from dashboard import PostureDashboard

class PostureAnalysisSystem:
    def __init__(self):
        """
        Inicializa el sistema completo de análisis postural
        """
        self.detector = PostureDetector()
        self.visualizer = Pose3DVisualizer()
        self.statistics = PostureStatistics()
        self.dashboard = PostureDashboard(self.statistics, self)  # Pasar referencia de self
        self.camera = None
        self.running = False
        self.camera_paused = False  # Nuevo estado para pausar cámara
        
        # Variables de estado
        self.bad_posture_detected = False
        self.bad_posture_start_time = None
        self.warning_delay = 3.0  # segundos antes de mostrar advertencia
        
    def setup_camera(self, camera_index=0):
        """
        Configura la cámara
        Args:
            camera_index: Índice de la cámara (0 para cámara por defecto)
        """
        self.camera = cv2.VideoCapture(camera_index)
        
        if not self.camera.isOpened():
            raise Exception("No se pudo abrir la cámara")
        
        # Configurar resolución
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        print("Cámara configurada correctamente")
    
    def draw_posture_info(self, image, is_bad_posture, posture_issues, calibration_status):
        """
        Dibuja información de postura en la imagen incluyendo estado de calibración
        """
        height, width = image.shape[:2]
        
        # === CALIBRACIÓN ===
        if calibration_status['calibrating']:
            color = (0, 255, 255)  # Amarillo
            status = f"CALIBRANDO... {calibration_status['progress']:.0f}%"
            
            # Dibujar barra de progreso
            bar_width = 280
            bar_height = 10
            progress_width = int((calibration_status['progress'] / 100) * bar_width)
            
            # Fondo de la barra
            cv2.rectangle(image, (10, 60), (10 + bar_width, 60 + bar_height), (100, 100, 100), -1)
            # Progreso
            cv2.rectangle(image, (10, 60), (10 + progress_width, 60 + bar_height), color, -1)
            
            # Instrucciones de calibración
            cv2.putText(image, "Mantén POSTURA CORRECTA por 2 segundos", (10, 90), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            cv2.putText(image, "• Espalda recta • Hombros relajados", (10, 115), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
            cv2.putText(image, "• Cabeza alineada • Sin encorvarse", (10, 135), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        
        # === ANÁLISIS DE POSTURA ===
        else:
            # Determinar color y mensaje
            if is_bad_posture:
                color = (0, 0, 255)  # Rojo
                status = "MALA POSTURA"
                
                # Mostrar problemas específicos
                y_offset = 60
                for issue in posture_issues:
                    cv2.putText(image, f"• {issue}", (10, y_offset), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
                    y_offset += 25
                    
            else:
                color = (0, 255, 0)  # Verde
                status = "POSTURA CORRECTA"
        
        # Dibujar rectángulo de estado principal
        cv2.rectangle(image, (10, 10), (300, 50), color, -1)
        cv2.putText(image, status, (20, 35), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        
        # Agregar información de estadísticas (solo si no está calibrando)
        if not calibration_status['calibrating']:
            stats = self.statistics.get_statistics_summary()
            
            # Mostrar estadísticas básicas en la esquina superior derecha
            stats_y = 20
            cv2.putText(image, f"Sesion: {stats['session_duration_formatted']}", 
                       (width - 200, stats_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            cv2.putText(image, f"Buena: {stats['good_percentage']:.1f}%", 
                       (width - 200, stats_y + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            cv2.putText(image, f"Mala: {stats['bad_percentage']:.1f}%", 
                       (width - 200, stats_y + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
            cv2.putText(image, f"Alertas: {stats['alert_count']}", 
                       (width - 200, stats_y + 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
        
        # Instrucciones generales
        cv2.putText(image, "Presiona 'q' para salir, 's' para estadisticas", (10, height - 40), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(image, "Presiona 'r' para reiniciar estadisticas", (10, height - 20), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        return image
    
    def handle_bad_posture(self):
        """
        Maneja la detección de mala postura con control de ventana mejorado
        """
        current_time = time.time()
        
        if self.bad_posture_start_time is None:
            self.bad_posture_start_time = current_time
        
        # Si ha pasado el tiempo de espera
        if (current_time - self.bad_posture_start_time) > self.warning_delay:
            # Si la ventana no está abierta Y se permite apertura automática
            if not self.visualizer.is_open() and self.visualizer.allow_auto_open:
                print("⚠️  Mala postura detectada por más de 3 segundos")
                print("🔄 Abriendo visualización 3D de postura correcta...")
                self.visualizer.show_in_thread()
                # Registrar alerta en estadísticas
                self.statistics.log_alert_opened()
    
    def handle_good_posture(self):
        """
        Maneja la detección de buena postura y reinicia temporizador si fue cerrada manualmente
        """
        # Si había mala postura antes y ahora está bien, permitir reapertura
        if self.bad_posture_start_time is not None:
            self.visualizer.allow_reopen()
        
        self.bad_posture_start_time = None
    
    def pause_camera_and_show_stats(self):
        """Pausa la cámara y muestra las estadísticas"""
        self.camera_paused = True
        
        # Cerrar la ventana de OpenCV
        cv2.destroyAllWindows()
        
        # Abrir dashboard
        self.dashboard.show()
        print("📊 Cámara pausada, dashboard abierto")
    
    def resume_camera_detection(self):
        """Reanuda la detección con cámara"""
        self.camera_paused = False
        print("📷 Cámara reanudada, continuando detección...")
    
    def run(self):
        """
        Ejecuta el bucle principal del sistema con calibración inicial
        """
        print("🚀 Iniciando Sistema de Análisis Postural MEJORADO")
        print("📷 Configurando cámara...")
        
        try:
            self.setup_camera()
        except Exception as e:
            print(f"❌ Error configurando cámara: {e}")
            return
        
        print("✅ Sistema listo!")
        print("💡 Siéntate frente a la cámara en POSTURA CORRECTA")
        print("📏 Mantén una distancia de 60-100cm de la cámara")
        print("🎯 El sistema se calibrará automáticamente en 2 segundos")
        print("⚠️  Después, detectará cambios en tu postura")
        print("=" * 60)
        
        # Iniciar calibración
        self.detector.start_calibration()
        
        # Iniciar estadísticas
        self.statistics.start_session()
        
        self.running = True
        frame_count = 0
        
        try:
            while self.running:
                # Si la cámara está pausada, esperar
                if self.camera_paused:
                    cv2.waitKey(100)  # Esperar 100ms y verificar de nuevo
                    continue
                
                # Capturar frame
                ret, frame = self.camera.read()
                if not ret:
                    print("❌ Error capturando frame")
                    break
                
                # Espejo horizontal para mayor naturalidad
                frame = cv2.flip(frame, 1)
                
                # Detectar postura con nuevo sistema
                processed_frame, is_bad_posture, posture_issues, calibration_status = self.detector.detect_posture(frame)
                
                # Actualizar estadísticas (solo si no está calibrando)
                if not calibration_status['calibrating']:
                    self.statistics.update_posture_state(not is_bad_posture, posture_issues)
                
                # Dibujar información en la imagen
                display_frame = self.draw_posture_info(processed_frame, is_bad_posture, posture_issues, calibration_status)
                
                # Solo manejar postura si ya está calibrado
                if not calibration_status['calibrating']:
                    if is_bad_posture:
                        self.handle_bad_posture()
                    else:
                        self.handle_good_posture()
                
                # Mostrar frame
                cv2.imshow('Análisis de Postura Corporal - SISTEMA MEJORADO', display_frame)
                
                # Control de FPS y salida
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    print("👋 Saliendo del sistema...")
                    break
                elif key == ord('s'):
                    print("📊 Pausando cámara y abriendo estadísticas...")
                    self.pause_camera_and_show_stats()
                elif key == ord('r'):
                    print("🔄 Reiniciando estadísticas...")
                    self.statistics.reset_session()
                    self.statistics.start_session()
                
                frame_count += 1
                
                # Debug info solo después de calibración
                if frame_count % 30 == 0 and not calibration_status['calibrating']:
                    status = "❌ MALA" if is_bad_posture else "✅ BUENA"
                    print(f"Frame {frame_count}: Postura {status}")
                    if posture_issues:
                        for issue in posture_issues:
                            print(f"  - {issue}")
                
                # Mostrar cuando calibración se complete
                if calibration_status['complete'] and frame_count == 1:
                    print("🎉 ¡Calibración completada! Ahora detectando cambios de postura...")
        
        except KeyboardInterrupt:
            print("\n🛑 Interrumpido por usuario")
        
        except Exception as e:
            print(f"❌ Error durante ejecución: {e}")
        
        finally:
            self.cleanup()
    
    def cleanup(self):
        """
        Limpia recursos al finalizar
        """
        print("🧹 Limpiando recursos...")
        
        self.running = False
        
        # Finalizar sesión de estadísticas y mostrar resumen
        if self.statistics:
            self.statistics.end_session()
            self.statistics.print_summary()
            
            # Exportar automáticamente
            try:
                export_path = self.statistics.export_to_csv()
                print(f"📄 Estadísticas exportadas automáticamente: {export_path}")
            except Exception as e:
                print(f"⚠️ Error exportando estadísticas: {e}")
        
        if self.camera:
            self.camera.release()
        
        cv2.destroyAllWindows()
        
        if self.visualizer:
            self.visualizer.close()
        
        if self.dashboard:
            self.dashboard.close()
        
        print("✅ Limpieza completada")

def main():
    """
    Función principal
    """
    print("=" * 70)
    print("🎯 SISTEMA DE DETECCIÓN DE POSTURA CORPORAL - VERSIÓN MEJORADA")
    print("=" * 70)
    print("📋 FUNCIONALIDADES:")
    print("   • 🎯 Calibración automática de postura correcta personal")
    print("   • 📐 Análisis avanzado con ángulos y coordenadas 3D")
    print("   • 🔍 Detección precisa de múltiples problemas posturales")
    print("   • 🕒 Filtrado temporal para evitar falsos positivos")
    print("   • 📊 Sistema de estadísticas y dashboard interactivo")
    print("   • � Exportación automática de datos en CSV")
    print("=" * 70)
    print("📖 INSTRUCCIONES:")
    print("   1. Siéntate con POSTURA CORRECTA al iniciar")
    print("   2. El sistema se calibrará automáticamente (2 segundos)")
    print("   3. Después detectará cambios en tu postura")
    print("   4. Mantén espalda recta, hombros relajados, cabeza alineada")
    print("=" * 70)
    print("🎮 CONTROLES:")
    print("   • 'q' - Salir del sistema")
    print("   • 's' - Pausar cámara y abrir estadísticas")
    print("   • 'r' - Reiniciar estadísticas de la sesión")
    print("   • En estadísticas: 'Volver a Camara' - Reanudar detección")
    print("=" * 70)
    
    # Crear y ejecutar sistema
    system = PostureAnalysisSystem()
    
    try:
        system.run()
    except Exception as e:
        print(f"❌ Error crítico: {e}")
    
    print("🏁 Programa terminado")

if __name__ == "__main__":
    main()
