import cv2
import datetime
from twilio.rest import Client

# Twilio setup (replace with your real credentials)
TWILIO_SID = "*****************"
TWILIO_AUTH = "****************"
TWILIO_FROM = "*************"  # your Twilio number
TWILIO_TO = "**************"  # your phone number (removed trailing space)

client = Client(TWILIO_SID, TWILIO_AUTH)

# Load MobileNet SSD model
net = cv2.dnn.readNetFromCaffe(
    r"C:/Users/HP/Downloads/MobileNetSSD_deploy.prototxt",
    r"C:/Users/HP/Downloads/archive/MobileNetSSD_deploy.caffemodel"
)

# Classes MobileNetSSD can detect
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
           "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
           "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
           "sofa", "train", "tvmonitor"]

# Video stream
cap = cv2.VideoCapture(0)
alert_sent = False

while True:
    ret, frame = cap.read()
    if not ret:
        break

    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)
    net.setInput(blob)
    detections = net.forward()

    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.5:
            idx = int(detections[0, 0, i, 1])
            if CLASSES[idx] == "person":
                label = f"Person detected: {confidence * 100:.2f}%"
                cv2.putText(frame, label, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

                # Send SMS and Call only once when detection happens
                if not alert_sent:
                    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    # Send SMS
                    message = client.messages.create(
                        body=f"[THREAT ALERT] {now} - Intruder detected on camera!",
                        from_=TWILIO_FROM,
                        to=TWILIO_TO
                    )
                    print("[ALERT] SMS sent:", message.sid)

                    # Make Call with custom alert message
                    call = client.calls.create(
                        twiml='<Response><Say voice="alice">Warning! Threat detected. A person has been spotted on your camera. Please check immediately.</Say></Response>',
                        from_=TWILIO_FROM,
                        to=TWILIO_TO
                    )
                    print("[ALERT] Call initiated:", call.sid)

                    alert_sent = True

    cv2.imshow("Frame", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()




DY1PC875W3UQWS47TB5QFQH7, recovery code
