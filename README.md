# KCDetector

A mobile application developed to detect creatinine levels, supporting early diagnosis of kidney diseases. The app is designed for resource-limited healthcare settings and leverages machine learning and computer vision for efficient and accessible testing.

## Collaboration

- **Dr. Sudip Chattopadhyay** | AIIMS Kalyani
- **Oishila Bandyopadhyay** | IIIT Kalyani

## Features

- **Creatinine Level Detection**: Uses advanced image processing to assess creatinine levels from captured images.
- **Accessibility**: A lightweight Android app optimized for resource-limited environments.
- **User-Friendly Interface**: Built with Flet for a simple, intuitive experience.
- **Machine Learning Model**: Developed using TensorFlow and OpenCV for real-time, accurate predictions.
  
## Tech Stack

- **Backend**: Flask
- **Frontend**: Flet (for Android)
- **ML Model**: TensorFlow, OpenCV

## Project Structure

The project has two main folders:

- **`backend`**: Contains the Flask application serving API endpoints.
- **`frontend`**: Flet-based interface for Android, handling user interaction and displaying predictions.

## Installation

To run the project locally, follow these steps:

### Backend Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/ProPython007/KCDetector.git
    cd KCDetector
    ```

2. Set up a virtual environment and install dependencies:

    ```bash
    cd backend
    python -m venv env
    source env/bin/activate
    pip install -r requirements.txt
    ```

3. Run the Flask server:

    ```bash
    python app.py
    ```

### Frontend Setup

1. Navigate to the frontend directory:

    ```bash
    cd frontend
    ```

2. Install required Flet packages:

    ```bash
    pip install -r requirements.txt
    ```

3. Run the frontend application on an Android device (instructions available in the app or project documentation).

## Usage

1. Launch the backend server.
2. Start the frontend app on an Android device.
3. Capture an image for creatinine level assessment, and receive a real-time result from the model.

## Preview

![pp8](https://github.com/user-attachments/assets/4b65b00d-4201-4412-8f54-0b00c6bbb72e)
