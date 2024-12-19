# BMI Tracker

#### BMI Calculator Web Application

## Video Demo
[youtube video](https://youtu.be/A-1wXYqKbcM) 

## Description

This project is a **BMI (Body Mass Index) Calculator** web application built using **FastAPI** for the backend and a simple HTML frontend. The app allows users to input their weight and height, calculate their BMI, and view their BMI category. It also includes a history feature to track previous BMI calculations along with their percentage changes.

The application features:
- **BMI Calculation**: Users input their weight and height, and the app calculates their BMI and categorizes it.
- **History**: Users can view their BMI calculation history, including the percentage change in BMI from previous records.
- **CORS-enabled**: The app allows communication between the frontend and backend even when hosted on different origins, thanks to FastAPI’s CORS middleware.


### Files

- **app.py**: This is the FastAPI backend. It handles the POST request to calculate BMI and the GET request to retrieve the BMI history.
- **index.html**: This HTML file contains the frontend interface for the user to input their weight and height, see BMI calculations, and view the history.
- **requirements.txt**: Lists the Python dependencies required for the project.

## Features

- **BMI Calculation**: 
   - The app calculates BMI using the formula:  
     \[
     \text{BMI} = \frac{\text{weight (kg)}}{\text{height (m)}^2}
     \]
   - It classifies BMI into categories (Underweight, Normal, Overweight, Obese).

- **History Feature**:
   - Users can track their previous BMI calculations along with the percentage change between them.
   - The app saves BMI history in an SQLite database.

- **Responsive Design**: 
   - The app uses Bootstrap to make the frontend responsive and user-friendly across different devices.

## Setup and Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/wklp/bmi_calculator.git
   cd bmi_calculator

2. **Create a virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```
3. **Install dependencies**:
```
pip install -r requirements.txt
```
4. **Run the FastAPI application**:
```
uvicorn app:app --reload
```
you can add */docs* to the url to get to the swaggar ui

5. **Access the frontend**:
   - Open the `index.html` file in your browser, or serve it using a local HTTP server (e.g., `python -m http.server`).

6. **Test the application**:
   - Enter your weight and height on the frontend.
   - Click "Calculate BMI" to get your BMI result.
   - Click "Load History" to view your previous BMI records.

