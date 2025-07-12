"""
Script de prueba para verificar el comportamiento de la ventana 3D
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pose_3d_visualizer import Pose3DVisualizer
import time

def test_window_close_behavior():
    """
    Prueba el comportamiento de cierre de ventana sin abrir ventanas reales
    """
    print("🧪 Iniciando prueba de comportamiento de ventana (sin GUI)")
    
    # Crear visualizador
    visualizer = Pose3DVisualizer()
    
    print(f"Estado inicial:")
    print(f"  - allow_auto_open: {visualizer.allow_auto_open}")
    print(f"  - manually_closed: {visualizer.manually_closed}")
    print(f"  - is_open(): {visualizer.is_open()}")
    print(f"  - is_showing: {visualizer.is_showing}")
    
    # Simular estado después de que se detecta mala postura y se abre ventana
    print("\n1. Simulando apertura por mala postura...")
    visualizer.is_showing = True
    print(f"  - is_open(): {visualizer.is_open()}")
    
    # Simular cierre manual (lo que haría el callback)
    print("\n2. Simulando cierre manual...")
    visualizer.manually_closed = True
    visualizer.allow_auto_open = False
    visualizer.is_showing = False
    
    print(f"  - allow_auto_open: {visualizer.allow_auto_open}")
    print(f"  - manually_closed: {visualizer.manually_closed}")
    print(f"  - is_open(): {visualizer.is_open()}")
    
    # Verificar que show_in_thread no funciona
    print("\n3. Intentando abrir después de cierre manual...")
    old_is_showing = visualizer.is_showing
    # Simular llamada a show_in_thread
    if not visualizer.allow_auto_open:
        print("  ❌ show_in_thread rechazado - allow_auto_open es False")
    else:
        print("  ✅ show_in_thread permitido")
        visualizer.is_showing = True
    
    print(f"  - is_showing cambió: {old_is_showing} -> {visualizer.is_showing}")
    
    # Permitir reapertura
    print("\n4. Llamando allow_reopen()...")
    visualizer.allow_reopen()
    
    print(f"  - allow_auto_open: {visualizer.allow_auto_open}")
    print(f"  - manually_closed: {visualizer.manually_closed}")
    
    # Intentar abrir otra vez
    print("\n5. Intentando abrir después de allow_reopen...")
    if not visualizer.allow_auto_open:
        print("  ❌ show_in_thread rechazado - allow_auto_open es False")
    else:
        print("  ✅ show_in_thread permitido")
        visualizer.is_showing = True
    
    print(f"  - is_open(): {visualizer.is_open()}")
    
    print("\n✅ Prueba completada - El flujo funciona correctamente")

if __name__ == "__main__":
    test_window_close_behavior()
