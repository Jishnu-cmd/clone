"""
Mirror Clone System using MediaPipe & OpenCV
Real-time human segmentation and mirror clone generation
"""

import cv2
import mediapipe as mp
import numpy as np
import time

class MirrorCloneSystem:
    def __init__(self):
        # Initialize MediaPipe selfie segmentation
        self.mp_selfie_segmentation = mp.solutions.selfie_segmentation
        self.selfie_segmentation = self.mp_selfie_segmentation.SelfieSegmentation(
            model_selection=1  # 0 for general, 1 for landscape
        )
        
        # Initialize webcam
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        # Performance tracking
        self.fps_counter = 0
        self.start_time = time.time()
        
    def process_frame(self, frame):
        """Process frame for human segmentation and mirror cloning"""
        # Convert BGR to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Perform segmentation
        results = self.selfie_segmentation.process(rgb_frame)
        
        # Create binary mask
        mask = results.segmentation_mask
        condition = mask > 0.5  # Threshold for segmentation
        
        # Extract person pixels
        person_frame = np.where(condition[..., None], frame, 0)
        
        # Create mirror clone (horizontal flip)
        mirror_clone = cv2.flip(person_frame, 1)
        
        return person_frame, mirror_clone, mask
    
    def create_display(self, original, person, mirror_clone):
        """Create combined display with original and mirror clone"""
        height, width = original.shape[:2]
        
        # Create side-by-side display
        combined = np.zeros((height, width * 2, 3), dtype=np.uint8)
        
        # Place original person on left
        combined[:, :width] = person
        
        # Place mirror clone on right
        combined[:, width:] = mirror_clone
        
        return combined
    
    def run(self):
        """Main execution loop"""
        print("Mirror Clone System Started")
        print("Press 'ESC' to exit")
        
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to capture frame")
                break
            
            # Process frame
            person_frame, mirror_clone, mask = self.process_frame(frame)
            
            # Create display
            display = self.create_display(frame, person_frame, mirror_clone)
            
            # Calculate FPS
            self.fps_counter += 1
            elapsed_time = time.time() - self.start_time
            if elapsed_time >= 1.0:
                fps = self.fps_counter / elapsed_time
                print(f"FPS: {fps:.1f}")
                self.fps_counter = 0
                self.start_time = time.time()
            
            # Display result
            cv2.imshow('Mirror Clone System', display)
            
            # Exit on ESC key
            if cv2.waitKey(1) & 0xFF == 27:  # ESC key
                break
        
        self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        self.cap.release()
        cv2.destroyAllWindows()
        print("Mirror Clone System Stopped")

if __name__ == "__main__":
    system = MirrorCloneSystem()
    system.run()