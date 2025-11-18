# Sign Language to Text and Speech Conversion - Usage Instructions

## 🚀 Quick Start

1. **Install Dependencies**: All required packages are already installed via `requirements.txt`
2. **Run the Project**: Execute `python final_pred.py`
3. **Use Your Webcam**: Show sign language gestures to the camera

## 📱 How to Use

### Basic Gestures
- **Show any sign language letter (A-Z)**: Hold the gesture, then remove your hand from the camera
- **The letter will automatically be added to the sentence when you remove your hand**

### Special Gestures
- **SPACE**: Show a flat hand with all fingers extended
- **BACKSPACE**: Make a closed fist
- **ENTER**: Show thumbs up (only thumb extended)
- **CLEAR**: Click the "Clear" button to reset the sentence

### Step-by-Step Usage
1. **Start the application**: Run `python final_pred.py`
2. **Position your hand**: Place your hand in front of the camera with a clean background
3. **Show a sign**: Make the sign language gesture for any letter
4. **Remove your hand**: Take your hand away from the camera view
5. **Character added**: The letter will automatically appear in the sentence
6. **Repeat**: Continue with more letters to build words and sentences
7. **Add spaces**: Use the flat hand gesture for spaces between words
8. **Speak**: Click the "Speak" button to hear the sentence

## 🎯 Tips for Best Results

- **Good lighting**: Ensure your hand is well-lit
- **Clean background**: Use a plain, uncluttered background
- **Hand position**: Keep your hand clearly visible in the camera
- **Steady gestures**: Hold each gesture steady for a moment
- **Remove hand completely**: Make sure your hand is completely out of view to add characters

## 🔧 Troubleshooting

### Common Issues
- **Camera not working**: Check if your webcam is connected and not being used by another application
- **Poor recognition**: Ensure good lighting and clean background
- **Characters not adding**: Make sure to completely remove your hand from the camera view

### Performance Tips
- **Close other applications** that might be using the camera
- **Restart the application** if you experience lag
- **Use a USB webcam** for better performance than built-in laptop cameras

## 📁 Project Files

- `final_pred.py` - Main application with GUI (recommended)
- `prediction_wo_gui.py` - Simple version without GUI
- `cnn8grps_rad1_model.h5` - Trained CNN model
- `requirements.txt` - Python dependencies
- `test_project.py` - Test script to verify components
- `webapp/` - Flask web app with login/signup and capture control

## 🎉 Features

- **Real-time sign language recognition**
- **Automatic character addition** when hands are removed
- **Special gesture support** (space, backspace, enter)
- **Text-to-speech conversion**
- **User-friendly GUI interface**
- **Status indicators** showing current actions
- **Clear instructions** displayed on screen

## 🆘 Support

If you encounter issues:
1. Check that all dependencies are installed
2. Ensure your webcam is working
3. Try the test script: `python test_project.py`
4. Check the console output for error messages
5. For the web app, run:

```bash
pip install -r requirements.txt
python webapp/app.py
```

Open `http://localhost:5000` to sign up, log in, and control the capture script.

## 🎯 What's Fixed

The original project had issues with:
- ❌ Characters not being added to sentences when hands were removed
- ❌ Poor error handling for camera issues
- ❌ Missing white image file dependencies
- ❌ Confusing user interface

**Now fixed with:**
- ✅ **Automatic character addition** when hands are removed from camera
- ✅ **Special gesture recognition** for space, backspace, and enter
- ✅ **Real-time status updates** showing what's happening
- ✅ **Clear user instructions** displayed on screen
- ✅ **Robust error handling** and fallback mechanisms
- ✅ **Self-contained white image** creation (no external file needed)

Enjoy using your sign language to text converter! 🎊 