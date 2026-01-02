"""
Demo Script for Mirror Clone System
Includes system checks and guided demonstration
"""

import cv2
import sys
import platform

def check_system_requirements():
    """Check if system meets requirements"""
    print("=== System Requirements Check ===")
    
    # Check Python version
    python_version = sys.version_info
    print(f"Python Version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print("❌ Python 3.8+ required")
        return False
    else:
        print("✅ Python version OK")
    
    # Check platform
    print(f"Platform: {platform.system()}")
    
    # Check OpenCV
    try:
        import cv2
        print(f"✅ OpenCV Version: {cv2.__version__}")
    except ImportError:
        print("❌ OpenCV not installed")
        return False
    
    # Check MediaPipe
    try:
        import mediapipe as mp
        print(f"✅ MediaPipe Version: {mp.__version__}")
    except ImportError:
        print("❌ MediaPipe not installed")
        return False
    
    # Check NumPy
    try:
        import numpy as np
        print(f"✅ NumPy Version: {np.__version__}")
    except ImportError:
        print("❌ NumPy not installed")
        return False
    
    return True

def check_webcam():
    """Check webcam availability"""
    print("\n=== Webcam Check ===")
    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ No webcam detected")
        return False
    
    ret, frame = cap.read()
    if not ret:
        print("❌ Cannot read from webcam")
        cap.release()
        return False
    
    height, width = frame.shape[:2]
    print(f"✅ Webcam detected - Resolution: {width}x{height}")
    
    cap.release()
    return True

def run_demo():
    """Run the demo application"""
    print("\n=== Starting Demo ===")
    print("Choose demo mode:")
    print("1. Basic Mirror Clone")
    print("2. Enhanced Mirror Clone")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        print("Starting Basic Mirror Clone...")
        try:
            from mirror_clone_system import MirrorCloneSystem
            system = MirrorCloneSystem()
            system.run()
        except ImportError as e:
            print(f"❌ Error importing basic system: {e}")
    elif choice == "2":
        print("Starting Enhanced Mirror Clone...")
        try:
            from enhanced_mirror_clone import EnhancedMirrorCloneSystem
            system = EnhancedMirrorCloneSystem()
            system.run()
        except ImportError as e:
            print(f"❌ Error importing enhanced system: {e}")
    else:
        print("Invalid choice")

def main():
    """Main demo function"""
    print("🪞 Mirror Clone System Demo")
    print("=" * 40)
    
    # Check requirements
    if not check_system_requirements():
        print("\n❌ System requirements not met")
        print("Please install required packages: pip install -r requirements.txt")
        return
    
    # Check webcam
    if not check_webcam():
        print("\n❌ Webcam not available")
        print("Please ensure webcam is connected and not in use by other applications")
        return
    
    print("\n✅ All checks passed!")
    
    # Run demo
    try:
        run_demo()
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo error: {e}")

if __name__ == "__main__":
    main()