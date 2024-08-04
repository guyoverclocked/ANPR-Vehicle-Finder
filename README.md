# ANPR-Vehicle-Finder
Stolen-Vehicle-Detection-ANPR is a proof-of-concept project using OpenCV and Tesseract to detect stolen vehicles via ANPR. It captures vehicle images, extracts license plates, and matches them against a database of stolen vehicles, sending email alerts to owners if a match is found.


<div align="center">
  <img src="https://github.com/guyoverclocked/ANPR-Vehicle-Finder/blob/main/Contents/ANPR.gif" alt="ANPR System in Action">
</div>

## Features
- Detects vehicle license plates from images.
- Matches detected license plates against a database of reported stolen vehicles.
- Sends email notifications to the vehicle owners if a match is found.

## Requirements
- Python 3.x
- OpenCV
- Imutils
- Pytesseract
- Mysql-connector-python
- Mailjet-rest
- Tesseract-OCR

## Setup

1. **Install Tesseract-OCR**:
   - Download and install Tesseract-OCR from [here](https://github.com/tesseract-ocr/tesseract).

2. **Clone the repository**:
   ```bash
   git clone https://github.com/your-repo/ANPR-Vehicle-Finder.git
   cd stolen-vehicle-detection
   ```
   
3. **Install Python dependencies**:
   ```bash
    pip install opencv-python imutils pytesseract mysql-connector-python mailjet-rest
   ```
   
4. **Configure database**:
-  Create a MySQL database named lost_vehicle.
-  Create a table user_info with columns reg_no (VARCHAR), email (VARCHAR), and name (VARCHAR).
  
5. **Update API keys and database credentials**:
-  Replace ENTER YOUR MAILJET API KEY and ENTER YOUR MAILJET SECRET KEY with your Mailjet API credentials.
_  Update the database connection details in the script.

## Usage
1. **Run the script**:
```bash
python anpr_script.py
```
2. **Add lost vehicles**:
-  Use a web interface or directly insert into the user_info table to add reported stolen vehicles with their registration numbers and owner details.
   
3. **Capture or upload images**:
-  The script can process both live camera feed and uploaded images to detect license plates.
  
4. **Receive notifications**:
-  Owners will receive an email notification if their vehicle is detected.

### Image Preprocessing
1. **Resizing**: The input image is resized for better handling and processing.
2. **Grayscale Conversion**: The resized image is converted to grayscale to simplify the processing, as color information is not needed for edge detection.
3. **Noise Reduction**: A bilateral filter is applied to the grayscale image to reduce noise while preserving edges, making it easier to detect the contours of the license plate.

### Edge Detection
1. **Canny Edge Detection**: The smoothed grayscale image undergoes Canny edge detection, which highlights the edges in the image, making it easier to identify potential license plate regions.

### Contour Detection
1. **Finding Contours**: Contours are detected in the edged image. Contours are simply the curves joining all continuous points along a boundary having the same color or intensity.
2. **Filtering Contours**: The detected contours are sorted based on their area, and the largest contours are kept for further processing. This helps in isolating the license plate from other objects in the image.

### License Plate Identification
1. **Approximating Contours**: The algorithm approximates each contour to a polygon. If a contour has four sides, it is considered a potential license plate.
2. **Cropping the License Plate**: Once a potential license plate is identified, the region is cropped from the original image.

### Optical Character Recognition (OCR)
1. **Text Extraction**: Tesseract OCR is used to extract text from the cropped license plate image. The extracted text is then cleaned by removing unwanted characters.

### Database Matching and Notification
1. **Database Matching**: The extracted license plate number is checked against a database of reported stolen vehicles.
2. **Email Notification**: If a match is found, the system sends an email notification to the vehicle owner with the relevant details.

## Code in Action!
Input image:
![Input image](https://github.com/guyoverclocked/ANPR-Vehicle-Finder/blob/main/Contents/car2.jpg)

Cropped image using openCV:
![Output image](https://github.com/guyoverclocked/ANPR-Vehicle-Finder/blob/main/Contents/1.png)

## License
This project is licensed under the MIT License.

