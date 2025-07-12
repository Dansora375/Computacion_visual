#!/usr/bin/env python3
"""
Script de prueba para verificar que los modelos 3D se cargan correctamente
"""

import os
import sys

def test_models():
    """Prueba la carga de modelos 3D"""
    
    print("🧪 PRUEBA DE MODELOS 3D")
    print("=" * 50)
    
    models_dir = "models"
    
    if not os.path.exists(models_dir):
        print(f"❌ Carpeta {models_dir}/ no existe")
        return False
    
    print(f"📁 Explorando carpeta {models_dir}/...")
    
    # Listar contenido
    items = os.listdir(models_dir)
    print(f"📂 Contenido encontrado: {len(items)} elementos")
    
    for item in items:
        item_path = os.path.join(models_dir, item)
        if os.path.isdir(item_path):
            print(f"📁 Carpeta: {item}")
            try:
                subfiles = os.listdir(item_path)
                for subfile in subfiles:
                    print(f"   📄 {subfile}")
            except PermissionError:
                print(f"   ❌ Sin permisos de acceso")
        else:
            print(f"📄 Archivo: {item}")
    
    # Intentar importar Vedo
    print("\n🔧 Probando importación de Vedo...")
    try:
        import vedo
        print(f"✅ Vedo importado correctamente (versión: {vedo.__version__})")
    except ImportError as e:
        print(f"❌ Error importando Vedo: {e}")
        return False
    
    # Probar carga de modelos con el visualizador
    print("\n🎯 Probando carga con el visualizador...")
    try:
        from pose_3d_visualizer import Pose3DVisualizer
        
        visualizer = Pose3DVisualizer()
        
        if visualizer.custom_models:
            print(f"✅ {len(visualizer.custom_models)} modelos cargados exitosamente:")
            for i, model_info in enumerate(visualizer.custom_models):
                print(f"   {i+1}. {model_info['filename']}")
            return True
        else:
            print("⚠️  No se cargaron modelos personalizados")
            print("   Se usará el modelo generado por código")
            return True
            
    except Exception as e:
        print(f"❌ Error en el visualizador: {e}")
        return False

def main():
    success = test_models()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 PRUEBA COMPLETADA")
        print("🚀 El sistema está listo para ejecutar:")
        print("   python main.py")
    else:
        print("⚠️  PROBLEMAS DETECTADOS")
        print("   Revisa los errores anteriores")
    print("=" * 50)

if __name__ == "__main__":
    main()
