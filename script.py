import cv2, time, pandas, os
from datetime import datetime

# initialization
first_frame = None
status_list = [None, None]
motion_times = []
data = pandas.DataFrame(columns = ["Start", "Stop"])

# capture video
video = cv2.VideoCapture(0)

# read video, make gray copy, compare video to gray first frame to
# detect motion, find edges of motion and draw square
while True:
    check, frame = video.read()

    status = 0

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    if first_frame is None:
        first_frame = gray_frame
        continue

    delta_frame = cv2.absdiff(first_frame, gray_frame)

    thresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
    thresh_frame = cv2.dilate(thresh_frame, None, iterations = 2)

    (cnts, _) = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnts:
        if cv2.contourArea(contour) < 10000:
            continue
        status = 1

        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

    status_list.append(status)

    status_list = status_list[-2:]

    if status_list[-1] == 1 and status_list[-2] == 0:
        motion_times.append(datetime.now())
    if status_list[-1] == 0 and status_list[-2] == 1:
        motion_times.append(datetime.now())

    cv2.imshow("Base Frame", gray_frame)
    cv2.imshow("Delta Frame", delta_frame)
    cv2.imshow("Binary Frame", thresh_frame)
    cv2.imshow("Colorized Frame", frame)

    key = cv2.waitKey(1)

    if key == ord("q"):
        if status == 1:
            motion_times.append(datetime.now())
        break

for i in range(0, len(motion_times), 2):
    data = data.append({"Start": motion_times[i], "Stop": motion_times[i + 1]},
    ignore_index = True)

#if os.path.exists("Motion_Times.csv"):
    #data.to_csv("Motion_Times.csv", mode = 'a', index = True, header = False)
#else:
data.to_csv("Motion_Times.csv")

video.release()
cv2.destroyAllWindows()
