"""
📊 Dashboard Visual de Estadísticas de Postura
Interfaz gráfica simplificada para visualizar estadísticas en tiempo real
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import os

class PostureDashboard:
    """
    Dashboard visual para mostrar estadísticas de postura (versión simplificada)
    """
    
    def __init__(self, statistics, main_system=None):
        """
        Inicializa el dashboard
        
        Args:
            statistics (PostureStatistics): Instancia del sistema de estadísticas
            main_system: Referencia al sistema principal para control de cámara
        """
        self.statistics = statistics
        self.main_system = main_system
        self.window = None
        
        # Referencias a los gráficos
        self.figure = None
        self.ax1 = None  # Gráfico de barras (problemas)
        self.ax2 = None  # Gráfico circular (distribución tiempo)
        self.canvas = None
        
        # Variables de la interfaz
        self.session_time_var = None
        self.good_time_var = None
        self.bad_time_var = None
        self.alerts_var = None
    
    def show(self):
        """Muestra el dashboard en una nueva ventana (sin threading)"""
        print("🔍 DEBUG: Intentando mostrar dashboard...")
        
        if self.window and self._window_exists():
            # Si ya existe, traer al frente
            print("🔍 DEBUG: Ventana ya existe, trayendo al frente...")
            self.window.lift()
            self.window.focus()
            self._update_display()  # Actualizar datos
            return
        
        print("🔍 DEBUG: Creando nueva ventana...")
        self._create_window()
        print("📊 Dashboard de estadísticas abierto")
        
        # Mantener la ventana abierta
        print("🔍 DEBUG: Iniciando mainloop...")
        self.window.mainloop()
        print("🔍 DEBUG: Mainloop terminado")
    
    def _window_exists(self):
        """Verifica si la ventana existe de forma segura"""
        try:
            return self.window.winfo_exists()
        except:
            return False
    
    def _create_window(self):
        """Crea la ventana principal del dashboard"""
        print("🔍 DEBUG: Creando ventana Tkinter...")
        
        # Usar ventana principal en lugar de Toplevel
        self.window = tk.Tk()
        self.window.title("Estadísticas de Postura - Sesión Actual")
        self.window.geometry("900x600")
        self.window.configure(bg='#f0f0f0')
        
        print("🔍 DEBUG: Ventana creada, configurando...")
        
        # Configurar el cierre de ventana
        self.window.protocol("WM_DELETE_WINDOW", self.close)
        
        print("🔍 DEBUG: Creando layout...")
        
        # Crear el layout principal
        self._create_header()
        self._create_charts_section()
        self._create_buttons_section()
        
        print("🔍 DEBUG: Actualizando display...")
        
        # Actualizar una vez al inicio
        self._update_display()
        
        print("🔍 DEBUG: Ventana completamente configurada")
    
    def _create_header(self):
        """Crea la sección del header con estadísticas principales"""
        header_frame = tk.Frame(self.window, bg='#2c3e50', height=80)
        header_frame.pack(fill='x', padx=10, pady=5)
        header_frame.pack_propagate(False)
        
        # Título
        title_label = tk.Label(header_frame, text="Estadísticas de Postura - Sesión Actual",
                              font=('Arial', 16, 'bold'), fg='white', bg='#2c3e50')
        title_label.pack(pady=5)
        
        # Frame para estadísticas en línea
        stats_frame = tk.Frame(header_frame, bg='#2c3e50')
        stats_frame.pack(fill='x', padx=20)
        
        # Variables de texto
        self.session_time_var = tk.StringVar(value="Tiempo: 00:00")
        self.good_time_var = tk.StringVar(value="Buena: 0%")
        self.bad_time_var = tk.StringVar(value="Mala: 0%")
        self.alerts_var = tk.StringVar(value="Alertas: 0")
        
        # Labels de estadísticas
        stats_labels = [
            (self.session_time_var, '#3498db'),
            (self.good_time_var, '#27ae60'), 
            (self.bad_time_var, '#e74c3c'),
            (self.alerts_var, '#f39c12')
        ]
        
        for i, (var, color) in enumerate(stats_labels):
            label = tk.Label(stats_frame, textvariable=var, font=('Arial', 12, 'bold'),
                           fg=color, bg='#2c3e50')
            label.pack(side='left', padx=20, expand=True)
    
    def _create_charts_section(self):
        """Crea la sección de gráficos"""
        charts_frame = tk.Frame(self.window, bg='#f0f0f0')
        charts_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Crear figura de matplotlib
        self.figure = Figure(figsize=(12, 6), facecolor='#f0f0f0')
        
        # Crear subplots
        self.ax1 = self.figure.add_subplot(121)  # Gráfico de barras (izquierda)
        self.ax2 = self.figure.add_subplot(122)  # Gráfico circular (derecha)
        
        # Configurar el canvas
        self.canvas = FigureCanvasTkAgg(self.figure, charts_frame)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)
        
        # Inicializar gráficos vacíos
        self._update_charts()
    
    def _create_buttons_section(self):
        """Crea la sección de botones de control"""
        buttons_frame = tk.Frame(self.window, bg='#f0f0f0', height=60)
        buttons_frame.pack(fill='x', padx=10, pady=5)
        buttons_frame.pack_propagate(False)
        
        # Estilo para botones
        button_style = {
            'font': ('Arial', 10, 'bold'),
            'height': 2,
            'width': 15
        }
        
        # Botón de actualizar
        update_btn = tk.Button(buttons_frame, text="Actualizar", 
                              command=self._manual_update,
                              bg='#3498db', fg='white', **button_style)
        update_btn.pack(side='left', padx=10, pady=10)
        
        # Botón de exportar
        export_btn = tk.Button(buttons_frame, text="Exportar CSV", 
                              command=self._export_data,
                              bg='#27ae60', fg='white', **button_style)
        export_btn.pack(side='left', padx=10, pady=10)
        
        # Botón de reiniciar estadísticas
        reset_btn = tk.Button(buttons_frame, text="Reiniciar", 
                             command=self._reset_statistics,
                             bg='#f39c12', fg='white', **button_style)
        reset_btn.pack(side='left', padx=10, pady=10)
        
        # Botón para volver a la cámara (NUEVO)
        resume_btn = tk.Button(buttons_frame, text="Volver a Camara", 
                             command=self._resume_camera,
                             bg='#9b59b6', fg='white', **button_style)
        resume_btn.pack(side='left', padx=10, pady=10)
        
        # Botón de cerrar
        close_btn = tk.Button(buttons_frame, text="Cerrar", 
                             command=self.close,
                             bg='#e74c3c', fg='white', **button_style)
        close_btn.pack(side='right', padx=10, pady=10)
    
    def _update_display(self):
        """Actualiza todos los elementos de la interfaz"""
        try:
            stats = self.statistics.get_statistics_summary()
            
            # Actualizar variables de texto del header
            self.session_time_var.set(f"Tiempo: {stats['session_duration_formatted']}")
            self.good_time_var.set(f"Buena: {stats['good_percentage']:.1f}%")
            self.bad_time_var.set(f"Mala: {stats['bad_percentage']:.1f}%")
            self.alerts_var.set(f"Alertas: {stats['alert_count']}")
            
            # Actualizar gráficos
            self._update_charts()
            
        except Exception as e:
            print(f"Error actualizando display: {e}")
    
    def _update_charts(self):
        """Actualiza los gráficos con datos actuales"""
        try:
            stats = self.statistics.get_statistics_summary()
            
            # Limpiar gráficos
            self.ax1.clear()
            self.ax2.clear()
            
            # Gráfico de barras - Tipos de problemas
            self._create_problems_chart(stats)
            
            # Gráfico circular - Distribución de tiempo
            self._create_time_distribution_chart(stats)
            
            # Ajustar layout y actualizar
            self.figure.tight_layout()
            self.canvas.draw()
            
        except Exception as e:
            print(f"Error actualizando gráficos: {e}")
    
    def _create_problems_chart(self, stats):
        """Crea el gráfico de barras con tipos de problemas"""
        problem_counts = stats['problem_counts']
        
        if not problem_counts:
            # Si no hay datos, mostrar mensaje
            self.ax1.text(0.5, 0.5, 'Sin problemas detectados aún', 
                         ha='center', va='center', transform=self.ax1.transAxes,
                         fontsize=12, color='gray')
            self.ax1.set_title('Tipos de Problemas Detectados', fontsize=14, fontweight='bold')
            return
        
        # Traducir nombres y preparar datos
        problems = []
        counts = []
        colors = ['#e74c3c', '#f39c12', '#9b59b6', '#3498db', '#e67e22', '#1abc9c']
        
        for i, (problem, count) in enumerate(problem_counts.items()):
            problem_name = self._translate_problem_name(problem)
            problems.append(problem_name)
            counts.append(count)
        
        # Crear gráfico de barras
        bars = self.ax1.bar(problems, counts, color=colors[:len(problems)])
        
        # Configurar el gráfico
        self.ax1.set_title('Tipos de Problemas Detectados', fontsize=14, fontweight='bold')
        self.ax1.set_ylabel('Cantidad de Detecciones')
        
        # Rotar etiquetas si son muy largas
        if len(max(problems, key=len)) > 10:
            self.ax1.tick_params(axis='x', rotation=45)
        
        # Agregar valores encima de las barras
        for bar, count in zip(bars, counts):
            height = bar.get_height()
            self.ax1.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                         f'{count}', ha='center', va='bottom', fontweight='bold')
    
    def _create_time_distribution_chart(self, stats):
        """Crea el gráfico circular con distribución de tiempo"""
        good_time = stats['good_posture_time']
        bad_time = stats['bad_posture_time']
        
        if good_time == 0 and bad_time == 0:
            # Si no hay datos, mostrar mensaje
            self.ax2.text(0.5, 0.5, 'Sesión no iniciada', 
                         ha='center', va='center', transform=self.ax2.transAxes,
                         fontsize=12, color='gray')
            self.ax2.set_title('Distribución del Tiempo', fontsize=14, fontweight='bold')
            return
        
        # Preparar datos para el gráfico circular
        sizes = [good_time, bad_time]
        labels = ['Buena Postura', 'Mala Postura']
        colors = ['#27ae60', '#e74c3c']
        
        # Filtrar valores cero
        filtered_data = [(size, label, color) for size, label, color in zip(sizes, labels, colors) if size > 0]
        
        if not filtered_data:
            return
        
        sizes, labels, colors = zip(*filtered_data)
        
        # Crear gráfico circular
        wedges, texts, autotexts = self.ax2.pie(sizes, labels=labels, colors=colors, 
                                               autopct='%1.1f%%', startangle=90)
        
        # Configurar estilo
        self.ax2.set_title('Distribución del Tiempo', fontsize=14, fontweight='bold')
        
        # Mejorar apariencia del texto
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
    
    def _translate_problem_name(self, problem_key):
        """Traduce nombres técnicos a nombres legibles (versión corta para gráficos)"""
        translations = {
            'head_tilt_down': 'Cabeza Abajo',
            'forward_lean': 'Inclinación',
            'shoulder_elevation': 'Hombros Elevados',
            'head_tilt_side': 'Cabeza Lateral',
            'asymmetric_shoulders': 'Hombros Asimétricos',
            'excessive_forward_head': 'Cabeza Adelante'
        }
        return translations.get(problem_key, problem_key.replace('_', ' ').title())
    
    def _manual_update(self):
        """Actualización manual forzada"""
        self._update_display()
        print("🔄 Dashboard actualizado manualmente")
    
    def _export_data(self):
        """Exporta los datos a CSV"""
        try:
            # Permitir al usuario elegir la ubicación
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Guardar estadísticas como..."
            )
            
            if filename:
                # Exportar usando el método del statistics
                self.statistics.export_to_csv(os.path.basename(filename))
                
                # Copiar a la ubicación elegida si es diferente
                if not filename.endswith(os.path.basename(filename)):
                    import shutil
                    default_path = os.path.join("estadisticas", os.path.basename(filename))
                    if os.path.exists(default_path):
                        shutil.copy2(default_path, filename)
                
                messagebox.showinfo("Exportación Exitosa", 
                                  f"Estadísticas exportadas a:\n{filename}")
                print(f"💾 Datos exportados: {filename}")
            
        except Exception as e:
            messagebox.showerror("Error de Exportación", f"Error al exportar: {str(e)}")
            print(f"❌ Error exportando: {e}")
    
    def _reset_statistics(self):
        """Reinicia las estadísticas después de confirmación"""
        result = messagebox.askyesno("Confirmar Reinicio", 
                                   "¿Estás seguro de que quieres reiniciar todas las estadísticas?\n"
                                   "Esta acción no se puede deshacer.")
        
        if result:
            self.statistics.reset_session()
            self._update_display()
            print("🔄 Estadísticas reiniciadas por el usuario")
    
    def _resume_camera(self):
        """Cierra el dashboard y reanuda la detección con cámara"""
        print("📷 Reanudando detección con cámara...")
        
        # Reanudar el sistema principal si existe la referencia
        if self.main_system:
            self.main_system.resume_camera_detection()
        
        # Cerrar la ventana y salir del mainloop
        if self.window:
            self.window.quit()  # Salir del mainloop
            self.window.destroy()
            self.window = None
    
    def close(self):
        """Cierra el dashboard"""
        if self.window:
            self.window.quit()  # Salir del mainloop
            self.window.destroy()
            self.window = None
        
        print("❌ Dashboard cerrado")
    
    def is_open(self):
        """Verifica si el dashboard está abierto"""
        try:
            return self.window is not None and self._window_exists()
        except:
            return False
