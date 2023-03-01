import cv2

## Other Options
#tracker = cv2.TrackerBoosting_create()
#tracker = cv2.TrackerMIL_create()
#tracker = cv2.TrackerKCF_create()
#tracker = cv2.TrackerTLD_create()
#tracker = cv2.TrackerMedianFlow_create()
#tracker = cv2.legacy.TrackerMOSSE_create()

tracker = cv2.TrackerCSRT_create()

cap = cv2.VideoCapture(0)
sw = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
sh = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
# Init tracker
success, frame = cap.read()
bbox = cv2.selectROI("Takip edilecek hedefi seciniz",frame, False)
tracker.init(frame, bbox)


def drawBox(img,bbox):
    # Drwaing a box around the object
    x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
    cv2.rectangle(img, (x, y), ((x + w), (y + h)), (0, 0, 255), 3, 3)
    
    # Visual reference for humans
    cv2.line(img, (x, y), ((x + w), (y + h)), (0, 0, 255), 3,)
    cv2.line(img, ((x + w), y), (x, (y + h)), (0, 0, 255), 3,)

    # Dot for the center of object 
    cv2.circle(img, (int(x+w/2), int(y+h/2)), 6, (0,0,0), -1)

    # Center-to-center line
    cv2.line(img, (int(sw/2), int(sh/2)), (int(x+w/2), int(y+h/2)), (255,150,0), 3)

    # Dot for the center of screen
    cv2.circle(img, (int(sw/2), int(sh/2)), 8, (0,0,0), -1)

    # An information for humans
    cv2.putText(img, "Takip ediliyor", (100, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)


while True:

    timer = cv2.getTickCount()
    success, img = cap.read()
    success, bbox = tracker.update(img)

    if success:
        drawBox(img,bbox)
    else:
        cv2.putText(img, "Hedef Gorus Disinda", (100, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # Informations about tracking system
    cv2.putText(img, "Fps:", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,0), 2)
    cv2.putText(img, "Durum:", (20, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)


    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
    if fps>60: myColor = (20,230,20)
    elif fps>20: myColor = (230,20,20)
    else: myColor = (20,20,230)
    cv2.putText(img,str(int(fps)), (75, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, myColor, 2);

    cv2.imshow("Takip Ediliyor", img)
    if cv2.waitKey(1) & 0xff == ord('q'):
       break
