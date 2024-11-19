import cv2

cam = cv2.VideoCapture(0)
cv2.namedWindow("Capture Images")

img_counter = 0

while True:
    ret, frame = cam.read()
    if not ret:
        break
    cv2.imshow("Capture Images", frame)

    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        img_name = f"C:/Users/AbdulMajeed/Desktop/python/image/image_{img_counter}.jpg"
        cv2.imwrite(img_name, frame)
        print(f"{img_name} written!")
        img_counter += 1

cam.release()
cv2.destroyAllWindows()
