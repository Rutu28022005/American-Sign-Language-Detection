import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import numpy as np
import os, os.path
from keras.models import load_model
import traceback
import time



#model = load_model('cnn8grps_rad1_model.h5')

capture = cv2.VideoCapture(0)
# Lower resolution for speed
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

hd = HandDetector(maxHands=1, detectionCon=0.3)
# #training data
# count = len(os.listdir("D://sign2text_dataset_2.0/Binary_imgs//A"))

#testing data
# count = len(os.listdir("D://test_data_2.0//Gray_imgs//A"))
count = 0  # Initialize count to 0 for now


p_dir = "A"
c_dir = "a"

offset = 30
step = 1
flag=False
suv=0

# Remove disk I/O of white image file (no separate skeleton window)

# FPS tracking
fps = 0.0
_last_time = time.perf_counter()


while True:
    try:
        _, frame = capture.read()
        frame = cv2.flip(frame, 1)
        hands= hd.findHands(frame, draw=False, flipType=True)
        img_final=img_final1=img_final2=0

        processed_this_frame = False
        if hands:
            hand = hands[0]
            x, y, w, h = hand['bbox']
            # Clamp ROI within frame bounds
            x1 = max(x - offset, 0)
            y1 = max(y - offset, 0)
            x2 = min(x + w + offset, frame.shape[1])
            y2 = min(y + h + offset, frame.shape[0])
            if x2 <= x1 or y2 <= y1:
                image = None
            else:
                image = frame[y1:y2, x1:x2]
            #image1 = imgg[y - offset:y + h + offset, x - offset:x + w + offset]



            if image is not None:
                roi = image     #rgb image without drawing
           # roi1 = image1   #rdb image with drawing



            # #for simple gray image without draw
                gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
                blur = cv2.GaussianBlur(gray, (1, 1), 2)
            #

            # #for binary image
                gray2 = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
                blur2 = cv2.GaussianBlur(gray2, (5, 5), 2)
                th3 = cv2.adaptiveThreshold(blur2, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
                ret, test_image = cv2.threshold(th3, 27, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
            #
            #
                test_image1=blur
                img_final1 = np.ones((400, 400), np.uint8) * 148
                h = test_image1.shape[0]
                w = test_image1.shape[1]
                img_final1[((400 - h) // 2):((400 - h) // 2) + h, ((400 - w) // 2):((400 - w) // 2) + w] = test_image1

                img_final = np.ones((400, 400), np.uint8) * 255
                h = test_image.shape[0]
                w = test_image.shape[1]
                img_final[((400 - h) // 2):((400 - h) // 2) + h, ((400 - w) // 2):((400 - w) // 2) + w] = test_image
                processed_this_frame = True


        if hands and processed_this_frame:
            # #print(" --------- lmlist=",hands[1])
            hand = hands[0]
            x, y, w, h = hand['bbox']
            # Do not render skeleton on a separate window for stability/perf

            #for gray image with drawings
            gray1 = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            blur1 = cv2.GaussianBlur(gray1, (1, 1), 2)


            test_image2= blur1
            img_final2= np.ones((400, 400), np.uint8) * 148
            h = test_image2.shape[0]
            w = test_image2.shape[1]
            img_final2[((400 - h) // 2):((400 - h) // 2) + h, ((400 - w) // 2):((400 - w) // 2) + w] = test_image2


            #cv2.imshow("aaa",white)
            # cv2.imshow("gray",img_final2)
            cv2.imshow("binary", img_final)
        else:
            # Visual feedback when no hands detected
            cv2.putText(frame, "No hand detected", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)
            # cv2.imshow("gray w/o draw", img_final1)



            # img = img_final.reshape(1, 400, 400, 1)
            # # print(model.predict(img))
            # prob = np.array(model.predict(img)[0], dtype='float32')
            # ch1 = np.argmax(prob, axis=0)
            # prob[ch1] = 0
            # ch2 = np.argmax(prob, axis=0)
            # prob[ch2] = 0
            # ch3 = np.argmax(prob, axis=0)
            # prob[ch3] = 0
            # ch1 = chr(ch1 + 65)
            # ch2 = chr(ch2 + 65)
            # ch3 = chr(ch3 + 65)
            # frame = cv2.putText(frame, "Predicted " + ch1 + " " + ch2 + " " + ch3, (x - offset - 150, y - offset - 10),
            #                     cv2.FONT_HERSHEY_SIMPLEX,
            #                     1, (255, 0, 0), 1, cv2.LINE_AA)

            #cv2.rectangle(frame, (x - offset, y - offset), (x + w, y + h), (3, 255, 25), 3)
        # FPS overlay
        now = time.perf_counter()
        dt = now - _last_time
        if dt > 0:
            fps = 0.9 * fps + 0.1 * (1.0 / dt)
        _last_time = now

        cv2.putText(frame, f"FPS: {fps:.1f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2, cv2.LINE_AA)
        # frame = cv2.putText(frame, "dir=" + c_dir + "  count=" + str(count), (50,50),
        #                     cv2.FONT_HERSHEY_SIMPLEX,
        #                     1, (255, 0, 0), 1, cv2.LINE_AA)
        cv2.imshow("frame", frame)
        interrupt = cv2.waitKey(1)
        if interrupt & 0xFF == 27:
            # esc key
            break
        if interrupt & 0xFF == ord('n'):
            p_dir = chr(ord(p_dir) + 1)
            c_dir = chr(ord(c_dir) + 1)
            if ord(p_dir)==ord('Z')+1:
                p_dir="A"
                c_dir="a"
            flag = False
            # #training data
            # count = len(os.listdir("D://sign2text_dataset_2.0/Binary_imgs//" + p_dir + "//"))

            # test data
            # count = len(os.listdir("D://test_data_2.0/Gray_imgs//" + p_dir + "//"))
            count = 0  # Reset count for new directory

        if interrupt & 0xFF == ord('a'):
            if flag:
                flag=False
            else:
                suv=0
                flag=True

        # reduce console spam
        # print("=====",flag)
        if flag==True:

            if suv==50:
                flag=False
            if step%2==0:
                # #this is for training data collection
                # cv2.imwrite("D:\\sign2text_dataset_2.0\\Binary_imgs\\" + p_dir + "\\" + c_dir + str(count) + ".jpg", img_final)
                # cv2.imwrite("D:\\sign2text_dataset_2.0\\Gray_imgs\\" + p_dir + "\\" + c_dir + str(count) + ".jpg", img_final1)
                # cv2.imwrite("D:\\sign2text_dataset_2.0\\Gray_imgs_with_drawing\\" + p_dir + "\\" + c_dir + str(count) + ".jpg", img_final2)

                # this is for testing data collection
                # cv2.imwrite("D:\\test_data_2.0\\Binary_imgs\\" + p_dir + "\\" + c_dir + str(count) + ".jpg",
                #             img_final)
                # cv2.imwrite("D:\\test_data_2.0\\Gray_imgs\\" + p_dir + "\\" + c_dir + str(count) + ".jpg",
                #             img_final1)
                # cv2.imwrite(
                #     "D:\\test_data_2.0\\Gray_imgs_with_drawing\\" + p_dir + "\\" + c_dir + str(count) + ".jpg",
                #     img_final2)
                print(f"Would save image {count} for letter {p_dir}")

                count += 1
                suv += 1
            step+=1
    except Exception:
        print("==",traceback.format_exc() )

capture.release()
cv2.destroyAllWindows()






















































# img_final=cv2.resize(img_final,(224,224));
# img_finalf=np.ones((400,400,3),np.uint8)*255;
# print("img final shape= ", img_final)
#  for i in range(400):
#      for j in range(400):
#          if(img_final[i][j]==255):
#              img_finalf[i][j]=[255,255,255]
#          else:
#              img_finalf[i][j]=[0,0,0];
# print("img final f shape= ", img_finalf)
# image = cv2.medianBlur(test_image, 5)
# kernel = np.ones((3, 3), np.uint8)
# kernel1 = np.ones((1, 1), np.uint8)
# dilate = cv2.dilate(image, kernel, iterations=1)
# dilate = cv2.erode(dilate, kernel1, iterations=1)

# cv2.imshow("gray",gray)
# cv2.imshow("blurr",blur)
# cv2.imshow("adapt threshold",th3)
# cv2.imshow("roi",test_image)

# white increase

# if flag:
#     if step % 2 == 0:
#         cv2.imwrite("D:\\sign_data\\B\\b" + str(count) + ".jpg", img_final)
#         print(count)
#         count += 1
#     step += 1