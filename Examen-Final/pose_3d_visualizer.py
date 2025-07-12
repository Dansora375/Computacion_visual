"""
Módulo de visualización 3D de postura correcta usando Vedo
Muestra un modelo 3D interactivo de la postura ideal
"""

import vedo
import numpy as np
import os
from threading import Thread
import time

class Pose3DVisualizer:
    def __init__(self, models_dir="models"):
        """
        Inicializa el visualizador 3D
        Args:
            models_dir: Directorio donde buscar modelos 3D personalizados
        """
        self.models_dir = models_dir
        self.plotter = None
        self.is_showing = False
        self.thread = None
        self.manually_closed = False  # Nueva variable para detectar cierre manual
        self.allow_auto_open = True  # Permite apertura automática
        self.last_show_time = 0  # Para evitar spam de ventanas
        
        # Variables para manejo de modelos
        self.custom_models = []
        
        # Cargar modelos disponibles al inicializar
        self.load_all_models()
        
    def create_correct_posture_model(self):
        """
        Crea un modelo 3D detallado de postura correcta usando primitivas de Vedo
        Muestra un esqueleto humano sentado con postura ergonómica ideal
        """
        models = []
        
        # === CABEZA ===
        head_center = [0, 0, 1.7]
        head = vedo.Sphere(head_center, r=0.08, c='lightblue', alpha=0.8)
        head.name = "Cabeza"
        models.append(head)
        
        # Ojos para orientación
        eye_left = vedo.Sphere([-0.03, -0.06, 1.72], r=0.015, c='white')
        eye_right = vedo.Sphere([0.03, -0.06, 1.72], r=0.015, c='white')
        models.extend([eye_left, eye_right])
        
        # === PUNTOS CLAVE DEL ESQUELETO ===
        neck = [0, 0, 1.6]
        shoulder_left = [-0.2, 0, 1.5]
        shoulder_right = [0.2, 0, 1.5]
        spine_upper = [0, 0.02, 1.35]  # Ligera curvatura natural
        spine_mid = [0, 0.05, 1.2]
        spine_lower = [0, 0.08, 1.05]
        hip_left = [-0.1, 0.1, 0.9]
        hip_right = [0.1, 0.1, 0.9]
        
        # Brazos - posición relajada
        elbow_left = [-0.35, 0.25, 1.25]
        elbow_right = [0.35, 0.25, 1.25]
        wrist_left = [-0.4, 0.4, 1.0]
        wrist_right = [0.4, 0.4, 1.0]
        
        # Piernas - posición sentada 90°
        knee_left = [-0.1, 0.45, 0.5]
        knee_right = [0.1, 0.45, 0.5]
        ankle_left = [-0.1, 0.45, 0.05]
        ankle_right = [0.1, 0.45, 0.05]
        
        # === COLUMNA VERTEBRAL (ROJA - PRIORITARIA) ===
        spine_points = [neck, spine_upper, spine_mid, spine_lower, 
                       [(hip_left[0] + hip_right[0])/2, (hip_left[1] + hip_right[1])/2, (hip_left[2] + hip_right[2])/2]]
        spine_line = vedo.Line(spine_points, c='red', lw=4)
        spine_line.name = "Columna Vertebral"
        models.append(spine_line)
        
        # === ESTRUCTURA DEL TORSO (ROJA) ===
        # Línea de hombros
        shoulder_line = vedo.Line([shoulder_left, shoulder_right], c='red', lw=3)
        models.append(shoulder_line)
        
        # Línea de caderas
        hip_line = vedo.Line([hip_left, hip_right], c='red', lw=3)
        models.append(hip_line)
        
        # Cuello
        neck_line = vedo.Line([neck, head_center], c='red', lw=3)
        models.append(neck_line)
        
        # Conectores torso
        left_torso = vedo.Line([shoulder_left, hip_left], c='red', lw=2, alpha=0.7)
        right_torso = vedo.Line([shoulder_right, hip_right], c='red', lw=2, alpha=0.7)
        models.extend([left_torso, right_torso])
        
        # === BRAZOS (AZUL) ===
        # Brazo izquierdo
        arm_left_upper = vedo.Line([shoulder_left, elbow_left], c='blue', lw=2.5)
        arm_left_lower = vedo.Line([elbow_left, wrist_left], c='blue', lw=2.5)
        
        # Brazo derecho
        arm_right_upper = vedo.Line([shoulder_right, elbow_right], c='blue', lw=2.5)
        arm_right_lower = vedo.Line([elbow_right, wrist_right], c='blue', lw=2.5)
        
        models.extend([arm_left_upper, arm_left_lower, arm_right_upper, arm_right_lower])
        
        # === PIERNAS (VERDE) ===
        # Pierna izquierda
        leg_left_upper = vedo.Line([hip_left, knee_left], c='green', lw=2.5)
        leg_left_lower = vedo.Line([knee_left, ankle_left], c='green', lw=2.5)
        
        # Pierna derecha
        leg_right_upper = vedo.Line([hip_right, knee_right], c='green', lw=2.5)
        leg_right_lower = vedo.Line([knee_right, ankle_right], c='green', lw=2.5)
        
        models.extend([leg_left_upper, leg_left_lower, leg_right_upper, leg_right_lower])
        
        # === ARTICULACIONES (AMARILLO) ===
        joint_positions = [
            (neck, "Cuello"), (shoulder_left, "Hombro Izq"), (shoulder_right, "Hombro Der"),
            (spine_upper, "Columna Superior"), (spine_mid, "Columna Media"), (spine_lower, "Columna Inferior"),
            (hip_left, "Cadera Izq"), (hip_right, "Cadera Der"),
            (elbow_left, "Codo Izq"), (elbow_right, "Codo Der"),
            (wrist_left, "Muñeca Izq"), (wrist_right, "Muñeca Der"),
            (knee_left, "Rodilla Izq"), (knee_right, "Rodilla Der"),
            (ankle_left, "Tobillo Izq"), (ankle_right, "Tobillo Der")
        ]
        
        for pos, name in joint_positions:
            joint = vedo.Sphere(pos, r=0.025, c='yellow')
            joint.name = name
            models.append(joint)
        
        # === SILLA ERGONÓMICA (MARRÓN) ===
        # Asiento
        chair_seat = vedo.Box([0, 0.25, 0.45], length=0.45, width=0.4, height=0.06, c='brown', alpha=0.8)
        chair_seat.name = "Asiento"
        
        # Respaldo con curvatura lumbar
        chair_back_lower = vedo.Box([0, 0.1, 0.7], length=0.4, width=0.08, height=0.3, c='brown', alpha=0.8)
        chair_back_upper = vedo.Box([0, 0.05, 1.0], length=0.4, width=0.06, height=0.4, c='brown', alpha=0.8)
        
        # Patas de la silla
        leg_positions = [[-0.15, 0.15, 0.2], [0.15, 0.15, 0.2], [-0.15, 0.35, 0.2], [0.15, 0.35, 0.2]]
        chair_legs = []
        for pos in leg_positions:
            leg = vedo.Cylinder(pos, r=0.02, height=0.4, c='darkbrown')
            chair_legs.append(leg)
        
        models.extend([chair_seat, chair_back_lower, chair_back_upper] + chair_legs)
        
        # === SUPERFICIE DEL SUELO ===
        floor = vedo.Box([0, 0.5, -0.1], length=1.0, width=1.0, height=0.02, c='lightgray', alpha=0.3)
        floor.name = "Suelo"
        models.append(floor)
        
        # === INDICADORES DE ÁNGULOS CORRECTOS ===
        # Ángulo de 90° en rodillas (verde claro)
        angle_knee_left = vedo.Line([hip_left, knee_left, ankle_left], c='lightgreen', lw=1, alpha=0.5)
        angle_knee_right = vedo.Line([hip_right, knee_right, ankle_right], c='lightgreen', lw=1, alpha=0.5)
        
        # Ángulo de 90° en codos
        angle_elbow_left = vedo.Line([shoulder_left, elbow_left, wrist_left], c='lightblue', lw=1, alpha=0.5)
        angle_elbow_right = vedo.Line([shoulder_right, elbow_right, wrist_right], c='lightblue', lw=1, alpha=0.5)
        
        models.extend([angle_knee_left, angle_knee_right, angle_elbow_left, angle_elbow_right])
        
        return models
    
    def load_all_models(self):
        """
        Carga todos los modelos 3D disponibles en la carpeta models y subcarpetas
        """
        self.custom_models = []
        
        if not os.path.exists(self.models_dir):
            print(f"📁 Carpeta {self.models_dir}/ no encontrada, usando modelo generado por código")
            return
            
        # Buscar archivos de modelo comunes
        model_extensions = ['.obj', '.ply', '.stl', '.vtk']
        model_files = []
        
        # Buscar en la carpeta principal
        for file in os.listdir(self.models_dir):
            file_path = os.path.join(self.models_dir, file)
            
            if os.path.isfile(file_path):
                # Archivo en carpeta principal
                for ext in model_extensions:
                    if file.lower().endswith(ext):
                        model_files.append((file_path, file))
                        break
            elif os.path.isdir(file_path):
                # Buscar en subcarpetas
                try:
                    for subfile in os.listdir(file_path):
                        for ext in model_extensions:
                            if subfile.lower().endswith(ext):
                                subfile_path = os.path.join(file_path, subfile)
                                display_name = f"{file}/{subfile}"
                                model_files.append((subfile_path, display_name))
                                break
                except PermissionError:
                    print(f"⚠️  No se puede acceder a la carpeta {file_path}")
        
        if not model_files:
            print(f"📁 No se encontraron modelos en {self.models_dir}/, usando modelo generado")
            return
        
        # Ordenar archivos para consistencia
        model_files.sort(key=lambda x: x[1])
        
        # Cargar cada modelo
        for model_path, display_name in model_files:
            try:
                print(f"🔄 Cargando modelo: {display_name}")
                
                # Buscar archivo de textura asociado
                texture_path = None
                model_dir = os.path.dirname(model_path)
                base_name = os.path.splitext(os.path.basename(model_path))[0]
                
                # Buscar texturas con nombres similares
                for ext in ['.png', '.jpg', '.jpeg', '.bmp', '.tga']:
                    potential_texture = os.path.join(model_dir, base_name + ext)
                    if os.path.exists(potential_texture):
                        texture_path = potential_texture
                        break
                    # También buscar archivos que contengan "texture" en el nombre
                    texture_files = [f for f in os.listdir(model_dir) if 'texture' in f.lower() and f.lower().endswith(ext)]
                    if texture_files:
                        texture_path = os.path.join(model_dir, texture_files[0])
                        break
                
                # Cargar modelo
                model = vedo.load(model_path)
                
                # Aplicar textura si se encuentra
                if texture_path and os.path.exists(texture_path):
                    print(f"🎨 Aplicando textura: {os.path.basename(texture_path)}")
                    model.texture(texture_path)
                else:
                    print(f"⚠️  No se encontró textura para {display_name}")
                
                # Verificar que el modelo se cargó correctamente
                if model is not None:
                    # Optimizar modelo (centrado y escalado)
                    model = self.optimize_model(model, display_name)
                    
                    self.custom_models.append({
                        'model': model,
                        'filename': display_name,
                        'path': model_path,
                        'texture_path': texture_path
                    })
                    print(f"✅ Modelo cargado y optimizado: {display_name}")
                else:
                    print(f"❌ Modelo vacío o inválido: {display_name}")
                    
            except Exception as e:
                print(f"❌ Error cargando {display_name}: {e}")
                print(f"   Ruta: {model_path}")
        
        if self.custom_models:
            print(f"🎯 {len(self.custom_models)} modelos disponibles")
            for i, model_info in enumerate(self.custom_models):
                print(f"   {i+1}. {model_info['filename']}")
            if len(self.custom_models) >= 2:
                print(f"📱 Se mostrarán los primeros 2 modelos lado a lado")
        else:
            print("⚠️  No se pudieron cargar modelos, usando generado por código")
    
    def optimize_model(self, model, name):
        """
        Optimiza un modelo 3D: centrado, escalado y posicionamiento
        """
        try:
            # Centrar el modelo en el origen
            model.center()
            
            # Obtener dimensiones del modelo
            bounds = model.bounds()
            width = bounds[1] - bounds[0]   # x
            depth = bounds[3] - bounds[2]   # y  
            height = bounds[5] - bounds[4]  # z
            
            print(f"📏 Dimensiones de {name}: {width:.2f} x {depth:.2f} x {height:.2f}")
            
            # Escalar modelo si es muy grande o muy pequeño
            max_dimension = max(width, depth, height)
            
            if max_dimension > 5.0:
                # Modelo muy grande, reducir
                scale_factor = 2.0 / max_dimension
                model.scale(scale_factor)
                print(f"🔽 Escalando {name} por factor {scale_factor:.2f} (muy grande)")
                
            elif max_dimension < 0.5:
                # Modelo muy pequeño, aumentar
                scale_factor = 1.5 / max_dimension
                model.scale(scale_factor)
                print(f"🔼 Escalando {name} por factor {scale_factor:.2f} (muy pequeño)")
            
            # Mover modelo para que esté en una posición adecuada
            # Asumiendo que el modelo debe estar "sentado" cerca del origen
            model.pos(0, 0, 0)
            
            return model
            
        except Exception as e:
            print(f"⚠️  Error optimizando modelo {name}: {e}")
            return model
    
    def get_current_model(self):
        """
        Obtiene los modelos para mostrar lado a lado con orientación y tamaño optimizados
        Posicionados exactamente como en la imagen de referencia
        """
        if not self.custom_models:
            # Usar modelo generado por código si no hay modelos personalizados
            return self.create_correct_posture_model(), "Modelo Generado por Código"
        
        if len(self.custom_models) == 1:
            # Solo un modelo disponible, centrarlo
            current = self.custom_models[0]
            model_copy = current['model'].clone()
            
            # Configurar orientación y tamaño para modelo único
            model_copy.pos(0, 0, -0.2)  # Centrar, ligeramente hacia atrás
            model_copy.scale(1.0)       # Tamaño normal
            model_copy.rotate(90, axis=[1, 0, 0])   # Rotar 90° en X para enderezar
            
            return [model_copy], current['filename']
        
        # Dos o más modelos: mostrar los primeros dos lado a lado
        model1 = self.custom_models[0]['model'].clone()
        model2 = self.custom_models[1]['model'].clone()
        
        # === CONFIGURACIÓN MODELO IZQUIERDO - Orientado hacia el usuario ===
        model1.pos(-0.8, 0, -0.2)   # Posición izquierda, más cerca y ligeramente hacia atrás
        model1.scale(1.0)           # Tamaño normal para mejor visibilidad
        model1.rotate(90, axis=[1, 0, 0])   # Rotar para que esté sentado
        model1.rotate(170, axis=[0, 0, 1])  # Rotar menos para orientación más natural
        
        # === CONFIGURACIÓN MODELO DERECHO - Orientado hacia el usuario ===
        model2.pos(0.8, 0, -0.2)    # Posición derecha, más cerca y ligeramente hacia atrás
        model2.scale(1.0)           # Tamaño normal para mejor visibilidad
        model2.rotate(90, axis=[1, 0, 0])   # Rotar para que esté sentado
        model2.rotate(170, axis=[0, 0, 1])  # Rotar menos para orientación más natural
        
        filename = f"{self.custom_models[0]['filename']} | {self.custom_models[1]['filename']}"
        return [model1, model2], filename
    
    def load_custom_model(self):
        """
        Método mantenido por compatibilidad - ahora usa get_current_model()
        """
        models, filename = self.get_current_model()
        return models if models != self.create_correct_posture_model() else None
    
    def show_correct_posture(self):
        """
        Muestra la ventana 3D con la postura correcta con soporte para múltiples modelos
        """
        if self.is_showing:
            return
            
        self.is_showing = True
        
        # Obtener modelo(s) actual(es)
        models, current_filename = self.get_current_model()
        
        # Determinar tipo de visualización
        if self.custom_models:
            print(f"🎯 Mostrando modelo(s): {current_filename}")
        else:
            print("🎯 Mostrando modelo generado por código")
        
        # Crear el plotter con configuración mejorada
        self.plotter = vedo.Plotter(
            title=f"🎯 Postura Correcta - {current_filename}",
            size=(1000, 700),
            bg='#f0f0f0'  # Gris claro
        )
        
        # === CALLBACK PARA DETECTAR CIERRE MANUAL ===
        def on_close(evt):
            """Detecta cuando el usuario cierra manualmente la ventana"""
            print("🔒 Ventana 3D cerrada por el usuario")
            print("⏳ Necesitas 3 segundos continuos de mala postura para reabrir")
            self.manually_closed = True
            self.allow_auto_open = False  # Desactivar apertura automática
            self.is_showing = False
        
        # Agregar callback de cierre usando el evento correcto
        self.plotter.add_callback('ExitEvent', on_close)
        
        # === TEXTOS INFORMATIVOS ACTUALIZADOS ===
        # Título principal
        title = vedo.Text2D("POSTURA CORRECTA ERGONÓMICA", pos="top-center", s=1.4, c='darkred', bold=True)
        
        # Información del modelo actual
        model_info = [
            vedo.Text2D("📱 Modelos 3D: Postura Correcta y Postura Incorrecta", pos=(0.02, 0.95), s=1.0, c='purple', bold=True),
            vedo.Text2D("💡 Al cerrar esta ventana, necesitarás 3 segundos", pos=(0.02, 0.90), s=0.8, c='orange', bold=True),
            vedo.Text2D("   continuos de mala postura para que se reabra", pos=(0.02, 0.87), s=0.8, c='orange', bold=True),
        ]
        
        # Controles simplificados - solo mouse
        controls_y_start = 0.79
        instructions = [
            vedo.Text2D("🖱️  CONTROLES:", pos=(0.02, controls_y_start), s=1.0, c='darkblue', bold=True),
            vedo.Text2D("• Arrastrar: Rotar vista", pos=(0.02, controls_y_start - 0.03), s=0.8, c='black'),
            vedo.Text2D("• Rueda: Zoom in/out", pos=(0.02, controls_y_start - 0.06), s=0.8, c='black'),
        ]
        
        # Puntos clave de postura - movidos hacia arriba
        posture_y_start = controls_y_start - 0.15
        posture_tips = [
            vedo.Text2D("✅ PUNTOS CLAVE:", pos=(0.02, posture_y_start), s=1.0, c='darkgreen', bold=True),
            vedo.Text2D("• Cabeza alineada", pos=(0.02, posture_y_start - 0.03), s=0.8, c='green'),
            vedo.Text2D("• Hombros relajados", pos=(0.02, posture_y_start - 0.06), s=0.8, c='green'),
            vedo.Text2D("• Espalda recta", pos=(0.02, posture_y_start - 0.09), s=0.8, c='red'),
            vedo.Text2D("• Ángulos 90°", pos=(0.02, posture_y_start - 0.12), s=0.8, c='blue'),
        ]
        
        # Información del sistema
        system_info = [
            vedo.Text2D("🔧 Sistema:", pos=(0.02, 0.08), s=0.8, c='gray'),
            vedo.Text2D("Detección: MediaPipe Pose", pos=(0.02, 0.05), s=0.7, c='gray'),
            vedo.Text2D("Visualización: Vedo 3D", pos=(0.02, 0.02), s=0.7, c='gray'),
        ]
        
        # Combinar todos los textos
        all_texts = (model_info + instructions + posture_tips + system_info)
        
        # Deshabilitar controles de usuario para cambiar modelos manualmente
        def on_key_press(evt):
            pass  # No se realiza ninguna acción al presionar teclas
        
        # Agregar todos los elementos
        all_objects = models + all_texts
        
        # Mostrar con configuración de teclas
        self.plotter.add_callback('KeyPress', on_key_press)
        
        # Ajustar orientación inicial y zoom en la visualización
        self.plotter.show(*all_objects, 
                         camera=dict(pos=(0, 4.0, 2.0),       # Cámara frontal, más centrada
                                   focalpoint=(0, 0, 0),      # Punto focal en el centro
                                   viewup=(0, 0, 1)),         # Vector "arriba"
                         interactive=True,
                         zoom=0.8)  # Zoom reducido para ver ambos modelos completos
        
        self.is_showing = False
    
    def show_in_thread(self):
        """
        Muestra la visualización 3D en un hilo separado, respetando cierre manual
        """
        import time
        
        # Si fue cerrada manualmente y no se permite apertura automática, no mostrar
        if not self.allow_auto_open:
            return
        
        if self.thread is None or not self.thread.is_alive():
            self.last_show_time = time.time()
            self.thread = Thread(target=self.show_correct_posture, daemon=True)
            self.thread.start()
    
    def allow_reopen(self):
        """
        Permite que la ventana se pueda reabrir después de cierre manual
        """
        print("🔓 Permitiendo reapertura de ventana")
        self.manually_closed = False
        self.allow_auto_open = True
    
    def close(self):
        """
        Cierra la ventana 3D programáticamente
        """
        if self.plotter is not None:
            self.plotter.close()
        self.is_showing = False
    
    def is_open(self):
        """
        Verifica si la ventana 3D está abierta
        """
        return self.is_showing
