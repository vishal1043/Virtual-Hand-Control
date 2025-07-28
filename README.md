# Virtual-Hand-Control
Controls system virtually with hand gestures.
A Python-based real-time Hand Gesture Recognition System that allows users to control system functions — like volume, scrolling, and mouse movement — using just hand gestures. Built using OpenCV, MediaPipe, and PyAutoGUI, this tool transforms your webcam into a touchless virtual controller.

# Features

- Scroll pages up/down with two fingers
- Adjust system volume using thumb–index pinch
- Control mouse cursor with your index finger
- Left-click and right-click using intuitive hand gestures
- Real-time hand tracking using **MediaPipe**
- Works with a regular webcam


# Technologies Used

- Python 3.x
- OpenCV
- MediaPipe
- NumPy
- PyAutoGUI
- Pycaw (volume control)
- comtypes (for audio endpoint access)



# File Structure

| File Name              | Description                                       |
|------------------------|---------------------------------------------------|
| `Main.py`              | Main application to start webcam & detect gestures |
| `HandTrackingModule.py`| Custom module to detect hand landmarks            |
| `tempCodeRunnerFile.py`| (Optional) Temporary test file used in IDE        |
| `README.md`            | Project documentation (this file)                |



# How to Run
  Step 1: Clone the Repository (or Download as ZIP)
  
    git clone https://github.com/vishal1043/Virtual-Hand-Control.git
    cd Virtual-Hand-Control
   ~🔹If you downloaded the ZIP file, just extract it and open the folder in your terminal.

  Step 2: Install Required Libraries
    You need Python 3 installed. Then run:
    
    pip install opencv-python mediapipe numpy pyautogui pycaw comtypes
  If you face any permission issues, add --user:
  
        pip install --user opencv-python mediapipe numpy pyautogui pycaw comtypes
  Step 3: Run the App
    Make sure your webcam is connected and working.
    Then launch the program:
     
        python Main.py
   
   🔹The webcam will turn on, and your hand gestures will begin to control your system functions like volume, scrolling, and cursor movement.

# Gesture Mapping
  |  Gesture                  | Mode / Action         |
  |---------------------------|-----------------------|
  | ✊ Fist                  | Neutral (Reset mode)  |
  | ☝️ Index Finger          | Enter Scroll mode     |
  | 🤘 Index + Middle Finger | Scroll Up / Down      |
  | 👍 Thumb + Index         | Volume Control Mode   |
  | ✋ All fingers extended  | Cursor Control Mode   |
  | 👆 Thumb near palm       | Left Click            |
  | 👉 Pinky near palm       | Right Click           |

