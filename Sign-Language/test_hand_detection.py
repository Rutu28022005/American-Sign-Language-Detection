#!/usr/bin/env python3
"""
Test script to check cvzone hand detection structure
"""

import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np

def test_hand_structure():
    """Test the structure of hand detection data"""
    print("Testing cvzone hand detection structure...")
    
    # Initialize hand detector
    detector = HandDetector(maxHands=1)
    
    # Create a test image (black image)
    test_image = np.zeros((480, 640, 3), dtype=np.uint8)
    
    # Try to detect hands in the test image
    hands = detector.findHands(test_image, draw=False, flipType=True)
    
    print(f"Hands detected: {len(hands)}")
    print(f"Hands type: {type(hands)}")
    
    if hands:
        print(f"First hand type: {type(hands[0])}")
        print(f"First hand content: {hands[0]}")
        
        if isinstance(hands[0], dict):
            print(f"Hand keys: {list(hands[0].keys())}")
        elif isinstance(hands[0], list):
            print(f"Hand list length: {len(hands[0])}")
            if hands[0]:
                print(f"First element: {hands[0][0]}")
                if isinstance(hands[0][0], dict):
                    print(f"First element keys: {list(hands[0][0].keys())}")
    
    # Test with a real camera
    print("\nTesting with real camera...")
    cap = cv2.VideoCapture(0)
    
    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            print("Frame captured successfully")
            
            # Detect hands in real frame
            hands_real = detector.findHands(frame, draw=False, flipType=True)
            print(f"Real hands detected: {len(hands_real)}")
            
            if hands_real:
                print(f"Real hand type: {type(hands_real[0])}")
                print(f"Real hand content: {hands_real[0]}")
                
                if isinstance(hands_real[0], dict):
                    print(f"Real hand keys: {list(hands_real[0].keys())}")
                elif isinstance(hands_real[0], list):
                    print(f"Real hand list length: {len(hands_real[0])}")
                    if hands_real[0]:
                        print(f"Real first element: {hands_real[0][0]}")
                        if isinstance(hands_real[0][0], dict):
                            print(f"Real first element keys: {list(hands_real[0][0].keys())}")
        
        cap.release()
    else:
        print("Could not access camera")

if __name__ == "__main__":
    test_hand_structure() 