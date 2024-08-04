# ANPR-Vehicle-Finder
Stolen-Vehicle-Detection-ANPR is a proof-of-concept project using OpenCV and Tesseract to detect stolen vehicles via ANPR. It captures vehicle images, extracts license plates, and matches them against a database of stolen vehicles, sending email alerts to owners if a match is found.


<div align="center">
  <img src="https://github.com/guyoverclocked/ANPR-Vehicle-Finder/blob/main/ANPR.gif" alt="ANPR System in Action">
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

## License
This project is licensed under the MIT License.

