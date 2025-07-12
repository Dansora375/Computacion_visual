#!/usr/bin/env python3
"""
Script de prueba rápida para verificar que todas las dependencias están instaladas
"""

def test_imports():
    """Prueba la importación de todas las librerías necesarias"""
    
    print("🧪 Probando importaciones...")
    
    try:
        import cv2
        print("✅ OpenCV importado correctamente")
        print(f"   Versión: {cv2.__version__}")
    except ImportError as e:
        print(f"❌ Error importando OpenCV: {e}")
        return False
    
    try:
        import mediapipe as mp
        print("✅ MediaPipe importado correctamente")
        print(f"   Versión: {mp.__version__}")
    except ImportError as e:
        print(f"❌ Error importando MediaPipe: {e}")
        return False
    
    try:
        import vedo
        print("✅ Vedo importado correctamente")
        print(f"   Versión: {vedo.__version__}")
    except ImportError as e:
        print(f"❌ Error importando Vedo: {e}")
        return False
    
    try:
        import numpy as np
        print("✅ NumPy importado correctamente")
        print(f"   Versión: {np.__version__}")
    except ImportError as e:
        print(f"❌ Error importando NumPy: {e}")
        return False
    
    return True

def test_camera():
    """Prueba el acceso a la cámara"""
    
    print("\n📷 Probando acceso a cámara...")
    
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        
        if cap.isOpened():
            print("✅ Cámara accesible")
            cap.release()
            return True
        else:
            print("❌ No se puede acceder a la cámara")
            return False
            
    except Exception as e:
        print(f"❌ Error probando cámara: {e}")
        return False

def main():
    print("=" * 50)
    print("🔧 PRUEBA DEL SISTEMA DE POSTURA")
    print("=" * 50)
    
    imports_ok = test_imports()
    camera_ok = test_camera()
    
    print("\n" + "=" * 50)
    
    if imports_ok and camera_ok:
        print("🎉 ¡Todo listo! El sistema debería funcionar correctamente")
        print("🚀 Ejecuta: python main.py")
    else:
        print("⚠️  Hay problemas que resolver:")
        if not imports_ok:
            print("   - Instalar dependencias: pip install -r requirements.txt")
        if not camera_ok:
            print("   - Verificar que la cámara no esté siendo usada por otra app")
            print("   - Comprobar permisos de cámara")
    
    print("=" * 50)

if __name__ == "__main__":
    main()
