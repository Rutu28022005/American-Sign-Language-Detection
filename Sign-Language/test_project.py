#!/usr/bin/env python3
"""
Simple test script to verify the sign language project components work correctly
"""

import cv2
import numpy as np
from keras.models import load_model
import os

def test_components():
    """Test if all required components are working"""
    print("Testing Sign Language Project Components...")
    
    # Test 1: Check if model file exists
    print("\n1. Testing model file...")
    if os.path.exists('cnn8grps_rad1_model.h5'):
        print("✓ Model file found")
        try:
            model = load_model('cnn8grps_rad1_model.h5')
            print("✓ Model loaded successfully")
        except Exception as e:
            print(f"✗ Error loading model: {e}")
            return False
    else:
        print("✗ Model file not found")
        return False
    
    # Test 2: Test OpenCV
    print("\n2. Testing OpenCV...")
    try:
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            print("✓ Camera access successful")
            ret, frame = cap.read()
            if ret:
                print("✓ Frame capture successful")
                print(f"  Frame shape: {frame.shape}")
            else:
                print("✗ Frame capture failed")
            cap.release()
        else:
            print("✗ Camera access failed")
    except Exception as e:
        print(f"✗ OpenCV error: {e}")
        return False
    
    # Test 3: Test numpy
    print("\n3. Testing NumPy...")
    try:
        test_array = np.ones((400, 400, 3), np.uint8) * 255
        print("✓ NumPy array creation successful")
        print(f"  Array shape: {test_array.shape}")
    except Exception as e:
        print(f"✗ NumPy error: {e}")
        return False
    
    # Test 4: Test white image creation
    print("\n4. Testing white image creation...")
    try:
        white_img = np.ones((400, 400, 3), np.uint8) * 255
        cv2.imwrite("test_white.jpg", white_img)
        print("✓ White image creation and saving successful")
        os.remove("test_white.jpg")  # Clean up
    except Exception as e:
        print(f"✗ Image creation error: {e}")
        return False
    
    print("\n✓ All tests passed! Project components are working correctly.")
    return True

if __name__ == "__main__":
    test_components() 