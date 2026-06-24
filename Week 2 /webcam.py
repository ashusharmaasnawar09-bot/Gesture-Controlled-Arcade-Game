import cv2 

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print('Webcam is not Working')
    exit()
frame_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
frame_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
choice = input('what action you want to perform')

if choice == "camera":
    while True:
        ret,frame = cap.read()
        if not ret:
            print('Frame is not captured')
            break
        cv2.imshow("Webcam Video" , frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print('Quitting')
            break

if choice == "capture":
     codec = cv2.VideoWriter_fourcc(*'XVID')
     recording = cv2.VideoWriter("recorded_video.avi" , codec , 20 , (int(frame_width), int(frame_height)))
     while True:
         ret , frame = cap.read()
         if not ret:
             print('Video Capturing is not Live')
             break
         recording.write(frame)
         cv2.imshow("Recording Live" , frame)
         if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Quitting")
                break
        
         
cap.release()    
cv2.destroyAllWindows()




    


