# Weather Dashboard Application

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Project Structure](#project-structure)
- [Usage](#usage)

## Introduction

The Weather Dashboard Application is a web-based tool that provides users with current weather conditions, 5-day forecasts, air quality information, and allows users to submit support requests. It uses the OpenWeatherMap API to fetch weather data and displays it in an accessible, user-friendly interface.

## Features

- Current weather conditions including temperature, humidity, wind speed, and more.
- 5-day weather forecast with daily details.
- Air quality index for the user's location.
- Form submission to collect support requests, stored in a JSON file on the server.
- Responsive design for use on various devices.

## Technologies Used

- **Backend:** Flask
- **Frontend:** HTML, CSS, JavaScript
- **API:** OpenWeatherMap API
- **Data Storage:** JSON file for form submissions

## Getting Started

### Prerequisites

- Python 3.x
- Flask
- OpenWeatherMap API Key

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Mordecai-Wambua/Weather-Service-Project.git
   cd Weather-Service-Project
   ```

2. **Install dependencies:**
   ```bash
   pip install flask requests
   ```

### Running the Application

1. **Run the Flask application:**

   ```bash
   python3 app.py your_openweather_api_key
   ```

2. **Open your web browser and navigate to http://127.0.0.1:5000/.**

### API Endpoints

- GET /: Renders the main dashboard with weather data for the default or queried city.
- POST /submit_form: Handles form submissions and saves the data to a JSON file.

### Usage

- Dashboard: Displays current weather, forecast, and air quality information for the selected city.
- Support Form: Users can fill out and submit a support request form. The data is stored in form_data.json.
- Weather Forecast Display
  The weather forecast is displayed in a 5-column layout, showing the date, temperature, condition, and an icon for each day.

### Form Submission

Upon submitting the form, the user is redirected to the dashboard, and the form data is saved to a JSON file on the server.
