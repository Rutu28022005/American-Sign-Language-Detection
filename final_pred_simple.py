# Importing Libraries
import numpy as np
import math
import cv2
import os, sys
import traceback
import pyttsx3
from keras.models import load_model
from cvzone.HandTrackingModule import HandDetector
from string import ascii_uppercase
import enchant
import tkinter as tk
from PIL import Image, ImageTk

ddd=enchant.Dict("en-US")
hd = HandDetector(maxHands=1)
hd2 = HandDetector(maxHands=1)

offset=29

os.environ["THEANO_FLAGS"] = "device=cuda, assert_no_cpu_op=True"

# Application :

class Application:

    def __init__(self):
        self.vs = cv2.VideoCapture(0)
        self.current_image = None
        self.model = load_model('cnn8grps_rad1_model.h5')
        self.speak_engine=pyttsx3.init()
        self.speak_engine.setProperty("rate",100)
        voices=self.speak_engine.getProperty("voices")
        self.speak_engine.setProperty("voice",voices[0].id)

        # Create white image for hand skeleton
        self.white_img = np.ones((400, 400, 3), np.uint8) * 255

        self.ct = {}
        self.ct['blank'] = 0
        self.blank_flag = 0
        self.space_flag=False
        self.next_flag=True
        self.prev_char=""
        self.count=-1
        self.ten_prev_char=[]
        for i in range(10):
            self.ten_prev_char.append(" ")

        # Add hand detection state variables
        self.hand_detected = False
        self.last_hand_char = ""
        self.hand_hold_time = 0
        self.char_added = False
        
        # Add gesture detection counters
        self.space_count = 0
        self.backspace_count = 0
        self.enter_count = 0

        for i in ascii_uppercase:
            self.ct[i] = 0
        print("Loaded model from disk")

        self.root = tk.Tk()
        self.root.title("Sign Language To Text Conversion")
        self.root.protocol('WM_DELETE_WINDOW', self.destructor)
        self.root.geometry("1300x850")

        self.panel = tk.Label(self.root)
        self.panel.place(x=100, y=3, width=480, height=640)

        self.panel2 = tk.Label(self.root)  # initialize image panel
        self.panel2.place(x=700, y=115, width=400, height=400)

        self.T = tk.Label(self.root)
        self.T.place(x=60, y=5)
        self.T.config(text="Sign Language To Text Conversion", font=("Courier", 30, "bold"))

        self.panel3 = tk.Label(self.root)  # Current Symbol
        self.panel3.place(x=280, y=585)

        self.T1 = tk.Label(self.root)
        self.T1.place(x=10, y=580)
        self.T1.config(text="Character :", font=("Courier", 30, "bold"))

        # Add status label
        self.status_label = tk.Label(self.root)
        self.status_label.place(x=10, y=720)
        self.status_label.config(text="Status: Ready", font=("Courier", 14), fg="green")

        self.panel5 = tk.Label(self.root)  # Sentence
        self.panel5.place(x=260, y=632)

        self.T3 = tk.Label(self.root)
        self.T3.place(x=10, y=632)
        self.T3.config(text="Sentence :", font=("Courier", 30, "bold"))

        self.T4 = tk.Label(self.root)
        self.T4.place(x=10, y=700)
        self.T4.config(text="Suggestions :", fg="red", font=("Courier", 30, "bold"))

        # Add instructions label
        self.instructions = tk.Label(self.root)
        self.instructions.place(x=10, y=750)
        self.instructions.config(text="Gestures: Show sign → Remove hand to add letter | Flat hand = Space | Fist = Backspace | Thumbs up = Enter", 
                               font=("Courier", 12), fg="blue", wraplength=1200)

        # Add gesture practice instructions
        self.practice_label = tk.Label(self.root)
        self.practice_label.place(x=10, y=780)
        self.practice_label.config(text="Practice: SPACE = Open palm | BACKSPACE = Tight fist | ENTER = Thumbs up only", 
                                 font=("Courier", 10), fg="green", wraplength=1200)

        # Add gesture statistics display
        self.stats_label = tk.Label(self.root)
        self.stats_label.place(x=10, y=810)
        self.stats_label.config(text="Gesture Stats: SPACE: 0 | BACKSPACE: 0 | ENTER: 0", 
                               font=("Courier", 10), fg="purple", wraplength=1200)

        self.b1=tk.Button(self.root)
        self.b1.place(x=390,y=700)

        self.b2 = tk.Button(self.root)
        self.b2.place(x=590, y=700)

        self.b3 = tk.Button(self.root)
        self.b3.place(x=790, y=700)

        self.b4 = tk.Button(self.root)
        self.b4.place(x=990, y=700)

        self.speak = tk.Button(self.root)
        self.speak.place(x=1305, y=630)
        self.speak.config(text="Speak", font=("Courier", 20), wraplength=100, command=self.speak_fun)

        self.clear = tk.Button(self.root)
        self.clear.place(x=1205, y=630)
        self.clear.config(text="Clear", font=("Courier", 20), wraplength=100, command=self.clear_fun)

        self.str = " "
        self.ccc=0
        self.word = " "
        self.current_symbol = "C"
        self.photo = "Empty"

        self.word1=" "
        self.word2 = " "
        self.word3 = " "
        self.word4 = " "

        self.video_loop()

    def video_loop(self):
        try:
            ok, frame = self.vs.read()
            if not ok:
                return
                
            cv2image = cv2.flip(frame, 1)
            hands, _ = hd.findHands(cv2image, draw=False, flipType=True)
            cv2image_copy = np.array(cv2image)
            cv2image = cv2.cvtColor(cv2image, cv2.COLOR_BGR2RGB)
            self.current_image = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=self.current_image)
            self.panel.imgtk = imgtk
            self.panel.config(image=imgtk)

            # Check if hand is currently detected
            current_hand_detected = len(hands) > 0
            
            # If hand was detected before but not now, add the character to sentence
            if self.hand_detected and not current_hand_detected and self.last_hand_char and not self.char_added:
                if self.add_character(self.last_hand_char):
                    self.char_added = True
                    self.status_label.config(text=f"Status: Added '{self.last_hand_char}' to sentence", fg="green")
            
            # Reset character added flag when hand is detected again
            if current_hand_detected:
                self.char_added = False
            else:
                self.status_label.config(text="Status: No hand detected - Show sign to begin", fg="orange")
            
            self.hand_detected = current_hand_detected

            if hands:
                try:
                    # Use the original working structure
                    hand = hands[0]
                    if hasattr(hand, '__getitem__') and 'bbox' in hand:
                        x, y, w, h = hand['bbox']
                        image = cv2image_copy[y - offset:y + h + offset, x - offset:x + w + offset]

                        # Check if image is valid
                        if image.size == 0 or w <= 0 or h <= 0:
                            return

                        # Use the created white image
                        white = self.white_img.copy()

                        handz, _ = hd2.findHands(image, draw=False, flipType=True)
                        self.ccc += 1
                        if handz and len(handz) > 0:
                            hand2 = handz[0]
                            if hasattr(hand2, '__getitem__') and 'lmList' in hand2:
                                self.pts = hand2['lmList']

                                os = ((400 - w) // 2) - 15
                                os1 = ((400 - h) // 2) - 15
                                
                                # Draw hand skeleton
                                for t in range(0, 4, 1):
                                    cv2.line(white, (self.pts[t][0] + os, self.pts[t][1] + os1), (self.pts[t + 1][0] + os, self.pts[t + 1][1] + os1),
                                             (0, 255, 0), 3)
                                for t in range(5, 8, 1):
                                    cv2.line(white, (self.pts[t][0] + os, self.pts[t][1] + os1), (self.pts[t + 1][0] + os, self.pts[t + 1][1] + os1),
                                             (0, 255, 0), 3)
                                for t in range(9, 12, 1):
                                    cv2.line(white, (self.pts[t][0] + os, self.pts[t][1] + os1), (self.pts[t + 1][0] + os, self.pts[t + 1][1] + os1),
                                             (0, 255, 0), 3)
                                for t in range(13, 16, 1):
                                    cv2.line(white, (self.pts[t][0] + os, self.pts[t][1] + os1), (self.pts[t + 1][0] + os, self.pts[t + 1][1] + os1),
                                             (0, 255, 0), 3)
                                for t in range(17, 20, 1):
                                    cv2.line(white, (self.pts[t][0] + os, self.pts[t][1] + os1), (self.pts[t + 1][0] + os, self.pts[t + 1][1] + os1),
                                             (0, 255, 0), 3)
                                cv2.line(white, (self.pts[5][0] + os, self.pts[5][1] + os1), (self.pts[9][0] + os, self.pts[9][1] + os1), (0, 255, 0), 3)
                                cv2.line(white, (self.pts[9][0] + os, self.pts[9][1] + os1), (self.pts[13][0] + os, self.pts[13][1] + os1), (0, 255, 0), 3)
                                cv2.line(white, (self.pts[13][0] + os, self.pts[13][1] + os1), (self.pts[17][0] + os, self.pts[17][1] + os1), (0, 255, 0), 3)
                                cv2.line(white, (self.pts[0][0] + os, self.pts[0][1] + os1), (self.pts[5][0] + os, self.pts[5][1] + os1), (0, 255, 0), 3)
                                cv2.line(white, (self.pts[0][0] + os, self.pts[0][1] + os1), (self.pts[17][0] + os, self.pts[17][1] + os1), (0, 255, 0), 3)

                                for i in range(21):
                                    cv2.circle(white, (self.pts[i][0] + os, self.pts[i][1] + os1), 2, (0, 0, 255), 1)

                                res = white
                                self.predict(res)
                                
                                # Store the current character for later use
                                self.last_hand_char = self.current_symbol
                                
                                # Handle special gestures immediately
                                if self.current_symbol == "SPACE":
                                    self.space_count += 1
                                    self.add_space()
                                    self.last_hand_char = ""  # Don't add SPACE as a character
                                    self.status_label.config(text=f"Status: SPACE ✓ (Count: {self.space_count}) - Added space", fg="blue")
                                    self.stats_label.config(text=f"Gesture Stats: SPACE: {self.space_count} | BACKSPACE: {self.backspace_count} | ENTER: {self.enter_count}", fg="purple")
                                    print(f"SPACE gesture detected! Total: {self.space_count}")
                                elif self.current_symbol == "BACKSPACE":
                                    self.backspace_count += 1
                                    if self.str.strip() and len(self.str) > 1:
                                        self.str = self.str[:-1]
                                        print("Backspace: Removed last character. Sentence:", self.str)
                                        self.status_label.config(text=f"Status: BACKSPACE ✓ (Count: {self.backspace_count}) - Removed character", fg="red")
                                    else:
                                        self.status_label.config(text=f"Status: BACKSPACE ✓ (Count: {self.backspace_count}) - Nothing to remove", fg="orange")
                                    self.last_hand_char = ""  # Don't add BACKSPACE as a character
                                    self.stats_label.config(text=f"Gesture Stats: SPACE: {self.space_count} | BACKSPACE: {self.backspace_count} | ENTER: {self.enter_count}", fg="purple")
                                    print(f"BACKSPACE gesture detected! Total: {self.backspace_count}")
                                elif self.current_symbol == "ENTER":
                                    self.enter_count += 1
                                    self.str += "\n"
                                    print("Enter: Added new line. Sentence:", self.str)
                                    self.last_hand_char = ""  # Don't add ENTER as a character
                                    self.status_label.config(text=f"Status: ENTER ✓ (Count: {self.enter_count}) - New line", fg="purple")
                                    self.stats_label.config(text=f"Gesture Stats: SPACE: {self.space_count} | BACKSPACE: {self.backspace_count} | ENTER: {self.enter_count}", fg="purple")
                                    print(f"ENTER gesture detected! Total: {self.enter_count}")
                                else:
                                    self.status_label.config(text=f"Status: Detected '{self.current_symbol}' - Remove hand to add", fg="green")

                                self.current_image2 = Image.fromarray(res)
                                imgtk = ImageTk.PhotoImage(image=self.current_image2)
                                self.panel2.imgtk = imgtk
                                self.panel2.config(image=imgtk)

                                self.panel3.config(text=self.current_symbol, font=("Courier", 30))

                                self.b1.config(text=self.word1, font=("Courier", 20), wraplength=825, command=self.action1)
                                self.b2.config(text=self.word2, font=("Courier", 20), wraplength=825,  command=self.action2)
                                self.b3.config(text=self.word3, font=("Courier", 20), wraplength=825,  command=self.action3)
                                self.b4.config(text=self.word4, font=("Courier", 20), wraplength=825,  command=self.action4)
                except Exception as e:
                    print(f"Error processing hand data: {e}")
                    # Continue without crashing

            self.panel5.config(text=self.str, font=("Courier", 30), wraplength=1025)
            
        except Exception as e:
            print("Error in video_loop:", str(e))
            traceback.print_exc()
        finally:
            self.root.after(10, self.video_loop)

    def add_character(self, char):
        """Add character to the sentence if it's valid"""
        if char and char != " " and char != "next" and char != "Backspace":
            self.str += char
            print(f"Added character '{char}' to sentence: {self.str}")
            return True
        return False

    def add_space(self):
        """Add space to the sentence"""
        if self.str.strip() and not self.str.endswith(" "):
            self.str += " "
            print("Added space to sentence:", self.str)

    def clear_fun(self):
        self.str=" "
        self.current_symbol=" "
        self.word=" "
        self.word1=" "
        self.word2=" "
        self.word3=" "
        self.word4=" "
        self.char_added = False
        self.last_hand_char = ""
        
        # Reset gesture counters
        self.space_count = 0
        self.backspace_count = 0
        self.enter_count = 0
        
        # Update stats display
        self.stats_label.config(text=f"Gesture Stats: SPACE: {self.space_count} | BACKSPACE: {self.backspace_count} | ENTER: {self.enter_count}", fg="purple")
        self.status_label.config(text="Status: Cleared - Ready to start", fg="green")

    def distance(self,x,y):
        return math.sqrt(((x[0] - y[0]) ** 2) + ((x[1] - y[1]) ** 2))

    def action1(self):
        idx_space = self.str.rfind(" ")
        idx_word = self.str.find(self.word, idx_space)
        last_idx = len(self.str)
        self.str = self.str[:idx_word]
        self.str = self.str + self.word1.upper()

    def action2(self):
        idx_space = self.str.rfind(" ")
        idx_word = self.str.find(self.word, idx_space)
        last_idx = len(self.str)
        self.str=self.str[:idx_word]
        self.str=self.str+self.word2.upper()

    def action3(self):
        idx_space = self.str.rfind(" ")
        idx_word = self.str.find(self.word, idx_space)
        last_idx = len(self.str)
        self.str = self.str[:idx_word]
        self.str = self.str + self.word3.upper()

    def action4(self):
        idx_space = self.str.rfind(" ")
        idx_word = self.str.find(self.word, idx_space)
        last_idx = len(self.str)
        self.str = self.str[:idx_word]
        self.str = self.str + self.word4.upper()

    def speak_fun(self):
        self.speak_engine.say(self.str)
        self.speak_engine.runAndWait()

    def destructor(self):
        print("Closing Application")
        self.root.quit()
        self.vs.release()

    # Copy the predict method from the original file
    def predict(self, test_image):
        white=test_image
        white = white.reshape(1, 400, 400, 3)
        prob = np.array(self.model.predict(white)[0], dtype='float32')
        ch1 = np.argmax(prob, axis=0)
        prob[ch1] = 0
        ch2 = np.argmax(prob, axis=0)
        prob[ch2] = 0
        ch3 = np.argmax(prob, axis=0)
        prob[ch3] = 0

        pl = [ch1, ch2]

        # condition for [Aemnst]
        l = [[5, 2], [5, 3], [3, 5], [3, 6], [3, 0], [3, 2], [6, 4], [6, 1], [6, 2], [6, 6], [6, 7], [6, 0], [6, 5],
             [4, 1], [1, 0], [1, 1], [6, 3], [1, 6], [5, 6], [5, 1], [4, 5], [1, 4], [1, 5], [2, 0], [2, 6], [4, 6],
             [1, 0], [5, 7], [1, 6], [6, 1], [7, 6], [2, 5], [7, 1], [5, 4], [7, 0], [7, 5], [7, 2]]
        if pl in l:
            if (self.pts[6][1] < self.pts[8][1] and self.pts[10][1] < self.pts[12][1] and self.pts[14][1] < self.pts[16][1] and self.pts[18][1] < self.pts[20][
                1]):
                ch1 = 0

        # condition for [o][s]
        l = [[2, 2], [2, 1]]
        if pl in l:
            if (self.pts[5][0] < self.pts[4][0]):
                ch1 = 0
                print("++++++++++++++++++")
                # print("00000")

        # condition for [c0][aemnst]
        l = [[0, 0], [0, 6], [0, 2], [0, 5], [0, 1], [0, 7], [5, 2], [7, 6], [7, 1]]
        pl = [ch1, ch2]
        if pl in l:
            if (self.pts[0][0] > self.pts[8][0] and self.pts[0][0] > self.pts[4][0] and self.pts[0][0] > self.pts[12][0] and self.pts[0][0] > self.pts[16][
                0] and self.pts[0][0] > self.pts[20][0]) and self.pts[5][0] > self.pts[4][0]:
                ch1 = 2

        # condition for [c0][aemnst]
        l = [[6, 0], [6, 6], [6, 2]]
        pl = [ch1, ch2]
        if pl in l:
            if self.distance(self.pts[8], self.pts[16]) < 52:
                ch1 = 2


        # condition for [gh][bdfikruvw]
        l = [[1, 4], [1, 5], [1, 6], [1, 3], [1, 0]]
        pl = [ch1, ch2]

        if pl in l:
            if self.pts[6][1] > self.pts[8][1] and self.pts[14][1] < self.pts[16][1] and self.pts[18][1] < self.pts[20][1] and self.pts[0][0] < self.pts[8][
                0] and self.pts[0][0] < self.pts[12][0] and self.pts[0][0] < self.pts[16][0] and self.pts[0][0] < self.pts[20][0]:
                ch1 = 3



        # con for [gh][l]
        l = [[4, 6], [4, 1], [4, 5], [4, 3], [4, 7]]
        pl = [ch1, ch2]
        if pl in l:
            if self.pts[4][0] > self.pts[0][0]:
                ch1 = 3

        # con for [gh][pqz]
        l = [[5, 3], [5, 0], [5, 7], [5, 4], [5, 2], [5, 1], [5, 5]]
        pl = [ch1, ch2]
        if pl in l:
            if self.pts[2][1] + 15 < self.pts[16][1]:
                ch1 = 3

        # con for [l][x]
        l = [[6, 4], [6, 1], [6, 2]]
        pl = [ch1, ch2]
        if pl in l:
            if self.distance(self.pts[4], self.pts[11]) > 55:
                ch1 = 4

        # con for [l][d]
        l = [[1, 4], [1, 6], [1, 1]]
        pl = [ch1, ch2]
        if pl in l:
            if (self.distance(self.pts[4], self.pts[11]) > 50) and (
                    self.pts[6][1] > self.pts[8][1] and self.pts[10][1] < self.pts[12][1] and self.pts[14][1] < self.pts[16][1] and self.pts[18][1] <
                    self.pts[20][1]):
                ch1 = 4

        # con for [l][gh]
        l = [[3, 6], [3, 4]]
        pl = [ch1, ch2]
        if pl in l:
            if (self.pts[4][0] < self.pts[0][0]):
                ch1 = 4

        # con for [l][c0]
        l = [[2, 2], [2, 5], [2, 4]]
        pl = [ch1, ch2]
        if pl in l:
            if (self.pts[1][0] < self.pts[12][0]):
                ch1 = 4

        # con for [l][c0]
        l = [[2, 2], [2, 5], [2, 4]]
        pl = [ch1, ch2]
        if pl in l:
            if (self.pts[1][0] < self.pts[12][0]):
                ch1 = 4

        # con for [gh][z]
        l = [[3, 6], [3, 5], [3, 4]]
        pl = [ch1, ch2]
        if pl in l:
            if (self.pts[6][1] > self.pts[8][1] and self.pts[10][1] < self.pts[12][1] and self.pts[14][1] < self.pts[16][1] and self.pts[18][1] < self.pts[20][
                1]) and self.pts[4][1] > self.pts[10][1]:
                ch1 = 5

        # con for [gh][pq]
        l = [[3, 2], [3, 1], [3, 6]]
        pl = [ch1, ch2]
        if pl in l:
            if self.pts[4][1] + 17 > self.pts[8][1] and self.pts[4][1] + 17 > self.pts[12][1] and self.pts[4][1] + 17 > self.pts[16][1] and self.pts[4][
                1] + 17 > self.pts[20][1]:
                ch1 = 5

        # con for [l][pqz]
        l = [[4, 4], [4, 5], [4, 2], [7, 5], [7, 6], [7, 0]]
        pl = [ch1, ch2]
        if pl in l:
            if self.pts[4][0] > self.pts[0][0]:
                ch1 = 5

        # con for [pqz][aemnst]
        l = [[0, 2], [0, 6], [0, 1], [0, 5], [0, 0], [0, 7], [0, 4], [0, 3], [2, 7]]
        pl = [ch1, ch2]
        if pl in l:
            if self.pts[0][0] < self.pts[8][0] and self.pts[0][0] < self.pts[12][0] and self.pts[0][0] < self.pts[16][0] and self.pts[0][0] < self.pts[20][0]:
                ch1 = 5

        # con for [pqz][yj]
        l = [[5, 7], [5, 2], [5, 6]]
        pl = [ch1, ch2]
        if pl in l:
            if self.pts[3][0] < self.pts[0][0]:
                ch1 = 7

        # con for [l][yj]
        l = [[4, 6], [4, 2], [4, 4], [4, 1], [4, 5], [4, 7]]
        pl = [ch1, ch2]
        if pl in l:
            if self.pts[6][1] < self.pts[8][1]:
                ch1 = 7

        # con for [x][yj]
        l = [[6, 7], [0, 7], [0, 1], [0, 0], [6, 4], [6, 6], [6, 5], [6, 1]]
        pl = [ch1, ch2]
        if pl in l:
            if self.pts[18][1] > self.pts[20][1]:
                ch1 = 7

        # condition for [x][aemnst]
        l = [[0, 4], [0, 2], [0, 3], [0, 1], [0, 6]]
        pl = [ch1, ch2]
        if pl in l:
            if self.pts[5][0] > self.pts[16][0]:
                ch1 = 6


        # condition for [yj][x]
        print("2222  ch1=+++++++++++++++++", ch1, ",", ch2)
        l = [[7, 2]]
        pl = [ch1, ch2]
        if pl in l:
            if self.pts[18][1] < self.pts[20][1] and self.pts[8][1] < self.pts[10][1]:
                ch1 = 6

        # condition for [c0][x]
        l = [[2, 1], [2, 2], [2, 6], [2, 7], [2, 0]]
        pl = [ch1, ch2]
        if pl in l:
            if self.distance(self.pts[8], self.pts[16]) > 50:
                ch1 = 6

        # con for [l][x]

        l = [[4, 6], [4, 2], [4, 1], [4, 4]]
        pl = [ch1, ch2]
        if pl in l:
            if self.distance(self.pts[4], self.pts[11]) < 60:
                ch1 = 6

        # con for [x][d]
        l = [[1, 4], [1, 6], [1, 0], [1, 2]]
        pl = [ch1, ch2]
        if pl in l:
            if self.pts[5][0] - self.pts[4][0] - 15 > 0:
                ch1 = 6

        # con for [b][pqz]
        l = [[5, 0], [5, 1], [5, 4], [5, 5], [5, 6], [6, 1], [7, 6], [0, 2], [7, 1], [7, 4], [6, 6], [7, 2], [5, 0],
             [6, 3], [6, 4], [7, 5], [7, 2]]
        pl = [ch1, ch2]
        if pl in l:
            if (self.pts[6][1] > self.pts[8][1] and self.pts[10][1] > self.pts[12][1] and self.pts[14][1] > self.pts[16][1] and self.pts[18][1] > self.pts[20][
                1]):
                ch1 = 1

        # con for [f][pqz]
        l = [[6, 1], [6, 0], [0, 3], [6, 4], [2, 2], [0, 6], [6, 2], [7, 6], [4, 6], [4, 1], [4, 2], [0, 2], [7, 1],
             [7, 4], [6, 6], [7, 2], [7, 5], [7, 2]]
        pl = [ch1, ch2]
        if pl in l:
            if (self.pts[6][1] < self.pts[8][1] and self.pts[10][1] > self.pts[12][1] and self.pts[14][1] > self.pts[16][1] and
                    self.pts[18][1] > self.pts[20][1]):
                ch1 = 1

        l = [[6, 1], [6, 0], [4, 2], [4, 1], [4, 6], [4, 4]]
        pl = [ch1, ch2]
        if pl in l:
            if (self.pts[10][1] > self.pts[12][1] and self.pts[14][1] > self.pts[16][1] and
                    self.pts[18][1] > self.pts[20][1]):
                ch1 = 1

        # con for [d][pqz]
        fg = 19
        # print("_________________ch1=",ch1," ch2=",ch2)
        l = [[5, 0], [3, 4], [3, 0], [3, 1], [3, 5], [5, 5], [5, 4], [5, 1], [7, 6]]
        pl = [ch1, ch2]
        if pl in l:
            if ((self.pts[6][1] > self.pts[8][1] and self.pts[10][1] < self.pts[12][1] and self.pts[14][1] < self.pts[16][1] and
                 self.pts[18][1] < self.pts[20][1]) and (self.pts[2][0] < self.pts[0][0]) and self.pts[4][1] > self.pts[14][1]):
                ch1 = 1

        l = [[4, 1], [4, 2], [4, 4]]
        pl = [ch1, ch2]
        if pl in l:
            if (self.distance(self.pts[4], self.pts[11]) < 50) and (
                    self.pts[6][1] > self.pts[8][1] and self.pts[10][1] < self.pts[12][1] and self.pts[14][1] < self.pts[16][1] and self.pts[18][1] <
                    self.pts[20][1]):
                ch1 = 1

        l = [[3, 4], [3, 0], [3, 1], [3, 5], [3, 6]]
        pl = [ch1, ch2]
        if pl in l:
            if ((self.pts[6][1] > self.pts[8][1] and self.pts[10][1] < self.pts[12][1] and self.pts[14][1] < self.pts[16][1] and
                 self.pts[18][1] < self.pts[20][1]) and (self.pts[2][0] < self.pts[0][0]) and self.pts[14][1] < self.pts[4][1]):
                ch1 = 1

        l = [[6, 6], [6, 4], [6, 1], [6, 2]]
        pl = [ch1, ch2]
        if pl in l:
            if self.pts[5][0] - self.pts[4][0] - 15 < 0:
                ch1 = 1

        # con for [i][pqz]
        l = [[5, 4], [5, 5], [5, 1], [0, 3], [0, 7], [5, 0], [0, 2], [6, 2], [7, 5], [7, 1], [7, 6], [7, 7]]
        pl = [ch1, ch2]
        if pl in l:
            if ((self.pts[6][1] < self.pts[8][1] and self.pts[10][1] < self.pts[12][1] and self.pts[14][1] < self.pts[16][1] and
                 self.pts[18][1] > self.pts[20][1])):
                ch1 = 1

        # con for [yj][bfdi]
        l = [[1, 5], [1, 7], [1, 1], [1, 6], [1, 3], [1, 0]]
        pl = [ch1, ch2]
        if pl in l:
            if (self.pts[4][0] < self.pts[5][0] + 15) and (
            (self.pts[6][1] < self.pts[8][1] and self.pts[10][1] < self.pts[12][1] and self.pts[14][1] < self.pts[16][1] and
             self.pts[18][1] > self.pts[20][1])):
                ch1 = 7

        # con for [uvr]
        l = [[5, 5], [5, 0], [5, 4], [5, 1], [4, 6], [4, 1], [7, 6], [3, 0], [3, 5]]
        pl = [ch1, ch2]
        if pl in l:
            if ((self.pts[6][1] > self.pts[8][1] and self.pts[10][1] > self.pts[12][1] and self.pts[14][1] < self.pts[16][1] and
                 self.pts[18][1] < self.pts[20][1])) and self.pts[4][1] > self.pts[14][1]:
                ch1 = 1

        # con for [w]
        fg = 13
        l = [[3, 5], [3, 0], [3, 6], [5, 1], [4, 1], [2, 0], [5, 0], [5, 5]]
        pl = [ch1, ch2]
        if pl in l:
            if not (self.pts[0][0] + fg < self.pts[8][0] and self.pts[0][0] + fg < self.pts[12][0] and self.pts[0][0] + fg < self.pts[16][0] and
                    self.pts[0][0] + fg < self.pts[20][0]) and not (
                    self.pts[0][0] > self.pts[8][0] and self.pts[0][0] > self.pts[12][0] and self.pts[0][0] > self.pts[16][0] and self.pts[0][0] > self.pts[20][
                0]) and self.distance(self.pts[4], self.pts[11]) < 50:
                ch1 = 1

        # con for [w]

        l = [[5, 0], [5, 5], [0, 1]]
        pl = [ch1, ch2]
        if pl in l:
            if self.pts[6][1] > self.pts[8][1] and self.pts[10][1] > self.pts[12][1] and self.pts[14][1] > self.pts[16][1]:
                ch1 = 1

        # -------------------------condn for 8 groups  ends

        # -------------------------condn for subgroups  starts
        #
        if ch1 == 0:
            ch1 = 'S'
            if self.pts[4][0] < self.pts[6][0] and self.pts[4][0] < self.pts[10][0] and self.pts[4][0] < self.pts[14][0] and self.pts[4][0] < self.pts[18][0]:
                ch1 = 'A'
            if self.pts[4][0] > self.pts[6][0] and self.pts[4][0] < self.pts[10][0] and self.pts[4][0] < self.pts[14][0] and self.pts[4][0] < self.pts[18][
                0] and self.pts[4][1] < self.pts[14][1] and self.pts[4][1] < self.pts[18][1]:
                ch1 = 'T'
            if self.pts[4][1] > self.pts[8][1] and self.pts[4][1] > self.pts[12][1] and self.pts[4][1] > self.pts[16][1] and self.pts[4][1] > self.pts[20][1]:
                ch1 = 'E'
            if self.pts[4][0] > self.pts[6][0] and self.pts[4][0] > self.pts[10][0] and self.pts[4][0] > self.pts[14][0] and self.pts[4][1] < self.pts[18][1]:
                ch1 = 'M'
            if self.pts[4][0] > self.pts[6][0] and self.pts[4][0] > self.pts[10][0] and self.pts[4][1] < self.pts[18][1] and self.pts[4][1] < self.pts[14][1]:
                ch1 = 'N'

        if ch1 == 2:
            if self.distance(self.pts[12], self.pts[4]) > 42:
                ch1 = 'C'
            else:
                ch1 = 'O'

        if ch1 == 3:
            if (self.distance(self.pts[8], self.pts[12])) > 72:
                ch1 = 'G'
            else:
                ch1 = 'H'

        if ch1 == 7:
            if self.distance(self.pts[8], self.pts[4]) > 42:
                ch1 = 'Y'
            else:
                ch1 = 'J'

        if ch1 == 4:
            ch1 = 'L'

        if ch1 == 6:
            ch1 = 'X'

        if ch1 == 5:
            if self.pts[4][0] > self.pts[12][0] and self.pts[4][0] > self.pts[16][0] and self.pts[4][0] > self.pts[20][0]:
                if self.pts[8][1] < self.pts[5][1]:
                    ch1 = 'Z'
                else:
                    ch1 = 'Q'
            else:
                ch1 = 'P'

        if ch1 == 1:
            if (self.pts[6][1] > self.pts[8][1] and self.pts[10][1] > self.pts[12][1] and self.pts[14][1] > self.pts[16][1] and self.pts[18][1] > self.pts[20][
                1]):
                ch1 = 'B'
            if (self.pts[6][1] > self.pts[8][1] and self.pts[10][1] < self.pts[12][1] and self.pts[14][1] < self.pts[16][1] and self.pts[18][1] < self.pts[20][
                1]):
                ch1 = 'D'
            if (self.pts[6][1] < self.pts[8][1] and self.pts[10][1] > self.pts[12][1] and self.pts[14][1] > self.pts[16][1] and self.pts[18][1] > self.pts[20][
                1]):
                ch1 = 'F'
            if (self.pts[6][1] < self.pts[8][1] and self.pts[10][1] < self.pts[12][1] and self.pts[14][1] < self.pts[16][1] and self.pts[18][1] > self.pts[20][
                1]):
                ch1 = 'I'
            if (self.pts[6][1] > self.pts[8][1] and self.pts[10][1] > self.pts[12][1] and self.pts[14][1] > self.pts[16][1] and self.pts[18][1] < self.pts[20][
                1]):
                ch1 = 'W'
            if (self.pts[6][1] > self.pts[8][1] and self.pts[10][1] > self.pts[12][1] and self.pts[14][1] < self.pts[16][1] and self.pts[18][1] < self.pts[20][
                1]) and self.pts[4][1] < self.pts[9][1]:
                ch1 = 'K'
            if ((self.distance(self.pts[8], self.pts[12]) - self.distance(self.pts[6], self.pts[10])) < 8) and (
                    self.pts[6][1] > self.pts[8][1] and self.pts[10][1] > self.pts[12][1] and self.pts[14][1] < self.pts[16][1] and self.pts[18][1] <
                    self.pts[20][1]):
                ch1 = 'U'
            if ((self.distance(self.pts[8], self.pts[12]) - self.distance(self.pts[6], self.pts[10])) >= 8) and (
                    self.pts[6][1] > self.pts[8][1] and self.pts[10][1] > self.pts[12][1] and self.pts[14][1] < self.pts[16][1] and self.pts[18][1] <
                    self.pts[20][1]) and (self.pts[4][1] > self.pts[9][1]):
                ch1 = 'V'

            if (self.pts[8][0] > self.pts[12][0]) and (
                    self.pts[6][1] > self.pts[8][1] and self.pts[10][1] > self.pts[12][1] and self.pts[14][1] < self.pts[16][1] and self.pts[18][1] <
                    self.pts[20][1]):
                ch1 = 'R'

        if ch1 == 1 or ch1 =='E' or ch1 =='S' or ch1 =='X' or ch1 =='Y' or ch1 =='B':
            if (self.pts[6][1] > self.pts[8][1] and self.pts[10][1] < self.pts[12][1] and self.pts[14][1] < self.pts[16][1] and self.pts[18][1] > self.pts[20][1]):
                ch1=" "

        # Detect space gesture (flat hand with all fingers extended)
        if (self.pts[6][1] < self.pts[8][1] and self.pts[10][1] < self.pts[12][1] and 
            self.pts[14][1] < self.pts[16][1] and self.pts[18][1] < self.pts[20][1] and
            self.pts[4][1] < self.pts[8][1] and self.pts[4][1] < self.pts[12][1] and
            self.pts[4][1] < self.pts[16][1] and self.pts[4][1] < self.pts[20][1]):
            ch1 = "SPACE"

        # Detect backspace gesture (closed fist - all fingers curled)
        if (self.pts[6][1] > self.pts[8][1] and self.pts[10][1] > self.pts[12][1] and 
            self.pts[14][1] > self.pts[16][1] and self.pts[18][1] > self.pts[20][1] and
            self.pts[4][1] > self.pts[8][1] and self.pts[4][1] > self.pts[12][1] and
            self.pts[4][1] > self.pts[16][1] and self.pts[4][1] > self.pts[20][1]):
            ch1 = "BACKSPACE"

        # Detect enter gesture (thumbs up - only thumb extended)
        if (self.pts[6][1] > self.pts[8][1] and self.pts[10][1] > self.pts[12][1] and 
            self.pts[14][1] > self.pts[16][1] and self.pts[18][1] > self.pts[20][1] and
            self.pts[4][1] < self.pts[8][1] and self.pts[4][1] < self.pts[12][1] and
            self.pts[4][1] < self.pts[16][1] and self.pts[4][1] < self.pts[20][1]):
            ch1 = "ENTER"

        # IMPROVED GESTURE RECOGNITION - More reliable detection
        
        # Improved SPACE gesture (flat hand - more flexible detection)
        if (self.pts[6][1] < self.pts[8][1] + 10 and self.pts[10][1] < self.pts[12][1] + 10 and 
            self.pts[14][1] < self.pts[16][1] + 10 and self.pts[18][1] < self.pts[20][1] + 10 and
            self.pts[4][1] < self.pts[8][1] + 15 and self.pts[4][1] < self.pts[12][1] + 15 and
            self.pts[4][1] < self.pts[16][1] + 15 and self.pts[4][1] < self.pts[20][1] + 15):
            ch1 = "SPACE"

        # Improved BACKSPACE gesture (closed fist - more flexible detection)
        if (self.pts[6][1] > self.pts[8][1] - 10 and self.pts[10][1] > self.pts[12][1] - 10 and 
            self.pts[14][1] > self.pts[16][1] - 10 and self.pts[18][1] > self.pts[20][1] - 10 and
            self.pts[4][1] > self.pts[8][1] - 15 and self.pts[4][1] > self.pts[12][1] - 15 and
            self.pts[4][1] > self.pts[16][1] - 15 and self.pts[4][1] > self.pts[20][1] - 15):
            ch1 = "BACKSPACE"

        # Improved ENTER gesture (thumbs up - more flexible detection)
        if (self.pts[6][1] > self.pts[8][1] - 10 and self.pts[10][1] > self.pts[12][1] - 10 and 
            self.pts[14][1] > self.pts[16][1] - 10 and self.pts[18][1] > self.pts[20][1] - 10 and
            self.pts[4][1] < self.pts[8][1] + 15 and self.pts[4][1] < self.pts[12][1] + 15 and
            self.pts[4][1] < self.pts[16][1] + 15 and self.pts[4][1] < self.pts[20][1] + 15):
            ch1 = "ENTER"

        # Alternative SPACE gesture (open palm facing camera)
        if (self.pts[6][1] < self.pts[8][1] + 20 and self.pts[10][1] < self.pts[12][1] + 20 and 
            self.pts[14][1] < self.pts[16][1] + 20 and self.pts[18][1] < self.pts[20][1] + 20 and
            self.pts[4][1] < self.pts[8][1] + 25 and self.pts[4][1] < self.pts[12][1] + 25 and
            self.pts[4][1] < self.pts[16][1] + 25 and self.pts[4][1] < self.pts[20][1] + 25 and
            self.distance(self.pts[4], self.pts[8]) > 30 and self.distance(self.pts[4], self.pts[12]) > 30):
            ch1 = "SPACE"

        # Alternative BACKSPACE gesture (tight fist)
        if (self.pts[6][1] > self.pts[8][1] - 20 and self.pts[10][1] > self.pts[12][1] - 20 and 
            self.pts[14][1] > self.pts[16][1] - 20 and self.pts[18][1] > self.pts[20][1] - 20 and
            self.pts[4][1] > self.pts[8][1] - 25 and self.pts[4][1] > self.pts[12][1] - 25 and
            self.pts[4][1] > self.pts[16][1] - 25 and self.pts[4][1] > self.pts[20][1] - 25 and
            self.distance(self.pts[4], self.pts[8]) < 20 and self.distance(self.pts[4], self.pts[12]) < 20):
            ch1 = "BACKSPACE"

        # Alternative ENTER gesture (thumbs up with relaxed fingers)
        if (self.pts[6][1] > self.pts[8][1] - 20 and self.pts[10][1] > self.pts[12][1] - 20 and 
            self.pts[14][1] > self.pts[16][1] - 20 and self.pts[18][1] > self.pts[20][1] - 20 and
            self.pts[4][1] < self.pts[8][1] + 25 and self.pts[4][1] < self.pts[12][1] + 25 and
            self.pts[4][1] < self.pts[16][1] + 25 and self.pts[4][1] < self.pts[20][1] + 25 and
            self.distance(self.pts[4], self.pts[8]) > 25):
            ch1 = "ENTER"


        print(self.pts[4][0] < self.pts[5][0])
        if ch1 == 'E' or ch1=='Y' or ch1=='B':
            if (self.pts[4][0] < self.pts[5][0]) and (self.pts[6][1] > self.pts[8][1] and self.pts[10][1] > self.pts[12][1] and self.pts[14][1] > self.pts[16][1] and self.pts[18][1] > self.pts[20][1]):
                ch1="next"


        if ch1 == 'Next' or 'B' or 'C' or 'H' or 'F' or 'X':
            if (self.pts[0][0] > self.pts[8][0] and self.pts[0][0] > self.pts[12][0] and self.pts[0][0] > self.pts[16][0] and self.pts[0][0] > self.pts[20][0]) and (self.pts[4][1] < self.pts[8][1] and self.pts[4][1] < self.pts[12][1] and self.pts[4][1] < self.pts[16][1] and self.pts[4][1] < self.pts[20][1]) and (self.pts[4][1] < self.pts[6][1] and self.pts[4][1] < self.pts[10][1] and self.pts[4][1] < self.pts[14][1] and self.pts[4][1] < self.pts[18][1]):
                ch1 = 'Backspace'


        if ch1=="next" and self.prev_char!="next":
            if self.ten_prev_char[(self.count-2)%10]!="next":
                if self.ten_prev_char[(self.count-2)%10]=="Backspace":
                    self.str=self.str[0:-1]
                else:
                    if self.ten_prev_char[(self.count - 2) % 10] != "Backspace":
                        self.str = self.str + self.ten_prev_char[(self.count-2)%10]
            else:
                if self.ten_prev_char[(self.count - 0) % 10] != "Backspace":
                    self.str = self.str + self.ten_prev_char[(self.count - 0) % 10]


        if ch1=="  " and self.prev_char!="  ":
            self.str = self.str + "  "

        self.prev_char=ch1
        self.current_symbol=ch1
        self.count += 1
        self.ten_prev_char[self.count%10]=ch1


        if len(self.str.strip())!=0:
            st=self.str.rfind(" ")
            ed=len(self.str)
            word=self.str[st+1:ed]
            self.word=word
            if len(word.strip())!=0:
                ddd.check(word)
                lenn = len(ddd.suggest(word))
                if lenn >= 4:
                    self.word4 = ddd.suggest(word)[3]

                if lenn >= 3:
                    self.word3 = ddd.suggest(word)[2]

                if lenn >= 2:
                    self.word2 = ddd.suggest(word)[1]

                if lenn >= 1:
                    self.word1 = ddd.suggest(word)[0]

        else:
            self.word1 = " "
            self.word2 = " "
            self.word3 = " "
            self.word4 = " " 

if __name__ == "__main__":
    app = Application()
    app.root.mainloop() 