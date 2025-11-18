#!/usr/bin/env python3
"""
Test script to verify improved gesture recognition
"""

import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np

def test_gesture_recognition():
    """Test the improved gesture recognition"""
    print("Testing Improved Gesture Recognition...")
    
    # Initialize hand detector
    detector = HandDetector(maxHands=1)
    
    # Create test images for different gestures
    test_gestures = {
        "SPACE": "flat_hand.jpg",
        "BACKSPACE": "closed_fist.jpg", 
        "ENTER": "thumbs_up.jpg"
    }
    
    print("\nGesture Recognition Test:")
    print("1. SPACE: Show flat hand with all fingers extended")
    print("2. BACKSPACE: Make tight fist with all fingers curled")
    print("3. ENTER: Show thumbs up (only thumb extended)")
    print("\nPress 'q' to quit, 's' to test SPACE, 'b' to test BACKSPACE, 'e' to test ENTER")
    
    # Start camera
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Could not access camera")
        return
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        # Flip frame for mirror effect
        frame = cv2.flip(frame, 1)
        
        # Detect hands
        hands = detector.findHands(frame, draw=True, flipType=True)
        
        # Add instructions on frame
        cv2.putText(frame, "SPACE: Flat hand | BACKSPACE: Fist | ENTER: Thumbs up", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, "Press 'q' to quit, 's'/'b'/'e' to test gestures", (10, 60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
        
        # Show frame
        cv2.imshow("Gesture Test", frame)
        
        # Handle key presses
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q'):
            break
        elif key == ord('s'):
            print("Testing SPACE gesture - Show flat hand")
        elif key == ord('b'):
            print("Testing BACKSPACE gesture - Make fist")
        elif key == ord('e'):
            print("Testing ENTER gesture - Show thumbs up")
    
    cap.release()
    cv2.destroyAllWindows()
    print("Gesture test completed!")

if __name__ == "__main__":
    test_gesture_recognition() 