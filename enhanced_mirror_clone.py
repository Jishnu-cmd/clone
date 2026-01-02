"""
Enhanced Mirror Clone System with additional effects
Includes multiple clone modes and visual enhancements
"""

import cv2
import mediapipe as mp
import numpy as np
import time

class EnhancedMirrorCloneSystem:
    def __init__(self):
        # Initialize MediaPipe
        self.mp_selfie_segmentation = mp.solutions.selfie_segmentation
        self.selfie_segmentation = self.mp_selfie_segmentation.SelfieSegmentation(
            model_selection=1
        )
        
        # Initialize webcam
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        # Clone modes
        self.clone_modes = ['mirror', 'double', 'quad']
        self.current_mode = 0
        
        # Background options
        self.backgrounds = ['black', 'white', 'blur']
        self.current_bg = 0
        
        # Performance tracking
        self.fps_counter = 0
        self.start_time = time.time()
        
    def create_background(self, frame, bg_type):
        """Create different background types"""
        height, width = frame.shape[:2]
        
        if bg_type == 'black':
            return np.zeros((height, width, 3), dtype=np.uint8)
        elif bg_type == 'white':
            return np.ones((height, width, 3), dtype=np.uint8) * 255
        elif bg_type == 'blur':
            return cv2.GaussianBlur(frame, (21, 21), 0)
        
        return np.zeros((height, width, 3), dtype=np.uint8)
    
    def process_frame(self, frame):
        """Enhanced frame processing with multiple effects"""
        # Convert BGR to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Perform segmentation
        results = self.selfie_segmentation.process(rgb_frame)
        mask = results.segmentation_mask
        condition = mask > 0.5
        
        # Create background
        background = self.create_background(frame, self.backgrounds[self.current_bg])
        
        # Extract person with background
        person_frame = np.where(condition[..., None], frame, background)
        
        return person_frame, mask, condition
    
    def create_mirror_display(self, person_frame):
        """Create mirror clone display"""
        mirror_clone = cv2.flip(person_frame, 1)
        return np.hstack([person_frame, mirror_clone])
    
    def create_double_display(self, person_frame):
        """Create double clone display"""
        clone1 = person_frame.copy()
        clone2 = person_frame.copy()
        return np.hstack([clone1, clone2])
    
    def create_quad_display(self, person_frame):
        """Create quad clone display"""
        # Resize for quad view
        height, width = person_frame.shape[:2]
        small_frame = cv2.resize(person_frame, (width//2, height//2))
        
        # Create variations
        normal = small_frame
        mirror = cv2.flip(small_frame, 1)
        inverted = cv2.flip(small_frame, 0)
        both = cv2.flip(small_frame, -1)
        
        # Combine into quad
        top_row = np.hstack([normal, mirror])
        bottom_row = np.hstack([inverted, both])
        return np.vstack([top_row, bottom_row])
    
    def add_info_overlay(self, frame):
        """Add information overlay"""
        mode_text = f"Mode: {self.clone_modes[self.current_mode].upper()}"
        bg_text = f"Background: {self.backgrounds[self.current_bg].upper()}"
        
        cv2.putText(frame, mode_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, bg_text, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, "Press 'M' for mode, 'B' for background, 'ESC' to exit", 
                   (10, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        return frame
    
    def run(self):
        """Enhanced main execution loop"""
        print("Enhanced Mirror Clone System Started")
        print("Controls:")
        print("- 'M': Change clone mode")
        print("- 'B': Change background")
        print("- 'ESC': Exit")
        
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            
            # Process frame
            person_frame, mask, condition = self.process_frame(frame)
            
            # Create display based on current mode
            if self.clone_modes[self.current_mode] == 'mirror':
                display = self.create_mirror_display(person_frame)
            elif self.clone_modes[self.current_mode] == 'double':
                display = self.create_double_display(person_frame)
            elif self.clone_modes[self.current_mode] == 'quad':
                display = self.create_quad_display(person_frame)
            
            # Add information overlay
            display = self.add_info_overlay(display)
            
            # Calculate and display FPS
            self.fps_counter += 1
            elapsed_time = time.time() - self.start_time
            if elapsed_time >= 1.0:
                fps = self.fps_counter / elapsed_time
                cv2.putText(display, f"FPS: {fps:.1f}", (display.shape[1] - 120, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                self.fps_counter = 0
                self.start_time = time.time()
            
            # Display result
            cv2.imshow('Enhanced Mirror Clone System', display)
            
            # Handle key presses
            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # ESC
                break
            elif key == ord('m') or key == ord('M'):
                self.current_mode = (self.current_mode + 1) % len(self.clone_modes)
                print(f"Mode changed to: {self.clone_modes[self.current_mode]}")
            elif key == ord('b') or key == ord('B'):
                self.current_bg = (self.current_bg + 1) % len(self.backgrounds)
                print(f"Background changed to: {self.backgrounds[self.current_bg]}")
        
        self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        self.cap.release()
        cv2.destroyAllWindows()
        print("Enhanced Mirror Clone System Stopped")

if __name__ == "__main__":
    system = EnhancedMirrorCloneSystem()
    system.run()