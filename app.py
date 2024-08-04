import cv2
import imutils
import pytesseract
import mysql.connector
from mailjet_rest import Client
from datetime import datetime

# Get the current time
now = datetime.now()
current_time = now.strftime("%H:%M")

# Mailjet API credentials
api_key = 'ENTER YOUR MAILJET API KEY'
api_secret = 'ENTER YOUR MAILJET SECRET KEY'
mailjet = Client(auth=(api_key, api_secret), version='v3.1')

# Database connection
db = mysql.connector.connect(
    host="127.0.0.1",
    user="anpr",
    passwd="anpr1234",
    database="lost_vehicle"
)
mycursor = db.cursor()

# Uncomment if using live camera feed
# camera = cv2.VideoCapture(0)
# while True:
#     _, image = camera.read()
#     cv2.imshow('Text Detection', image)
#     if cv2.waitKey(1) & 0xFF == ord('s'):
#         cv2.imwrite('test1.jpg', image)
#         break
# camera.release()
# cv2.destroyAllWindows()

# Read the image file
image = cv2.imread("car2.jpg")
image = imutils.resize(image, width=500)  # Resize image
cv2.imshow("Original Image", image)
cv2.waitKey(0)

# Convert to grayscale and smoothen the image
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.bilateralFilter(gray, 11, 17, 17)

# Detect edges
edged = cv2.Canny(gray, 170, 200)
cv2.imshow("Canny Image", edged)
cv2.waitKey(0)

# Find contours
cnts, _ = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
image1 = image.copy()
cv2.drawContours(image1, cnts, -1, (0, 255, 0), 3)
#cv2.imshow("Canny after Contouring", image1)
#cv2.waitKey(0)

# Sort contours based on area and keep the top 30
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:30]
NumberPlateCount = None

for i in cnts:
    perimeter = cv2.arcLength(i, True)
    approx = cv2.approxPolyDP(i, 0.02 * perimeter, True)
    if len(approx) == 4:
        NumberPlateCount = approx
        x, y, w, h = cv2.boundingRect(i)
        crp_img = image[y:y + h, x:x + w]
        cv2.imwrite('1.png', crp_img)
        break

cv2.drawContours(image, [NumberPlateCount], -1, (0, 255, 0), 3)
cv2.imshow("Final Image", image)
cv2.waitKey(0)

crop_img_loc = '1.png'
cv2.imshow("Cropped Image", cv2.imread(crop_img_loc))

# Remove unwanted characters from the text
def remove(text):
    return "".join(text.split())

# Extract text from the image
text = pytesseract.image_to_string(crop_img_loc, lang='eng')
space_removed = remove(text)
filtered_text = ''.join(filter(lambda char: char.isalnum(), space_removed))

print("")
print('The number is: ', filtered_text)
cv2.waitKey(0)

# Fetch registered license numbers from the database
mycursor.execute("SELECT reg_no FROM user_info")
license_no = [x[0] for x in mycursor.fetchall()]
print("")
print(license_no)

if filtered_text in license_no:
    # Fetch owner's email and name
    mycursor.execute(f"SELECT email, name FROM user_info WHERE reg_no = '{filtered_text}'")
    owner_info = mycursor.fetchone()
    email, name = owner_info

    print("")
    print("Vehicle reported as lost!")
    print("")
    print("Sending email to owner...")

    data = {
        'Messages': [
            {
                "From": {
                    "Email": "FROM E-MAIL",
                    "Name": "Vehicle Found Report"
                },
                "To": [
                    {
                        "Email": email,
                        "Name": name
                    }
                ],
                "Subject": "Important Message, Vehicle Found.",
                "TextPart": f"Dear {name}, your vehicle with registration number: {filtered_text}, was found at {current_time}. Thank you!",
                "CustomID": "VehicleFound"
            }
        ]
    }
    result = mailjet.send.create(data=data)
    print(result.status_code)
    print(result.json())
    print('Owner notified!')

    # Remove the entry from the database
    mycursor.execute(f"DELETE FROM user_info WHERE reg_no = '{filtered_text}'")
    db.commit()
else:
    print("No data found.")
