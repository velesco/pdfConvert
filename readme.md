# DOCX to PDF Converter Service

This service is a simple Flask-based application that converts DOCX documents to PDFs using LibreOffice. It was containerized via Docker.

## Files

- **[app.py](app.py):** Main Flask application that handles document conversion.
- **[DockerFile](DockerFile):** Docker configuration to build the container image.
- **[requirements.txt](requirements.txt):** Python dependencies required for the application.

## How to Run Locally

1. **Install Dependencies:**

   ```sh
   pip install -r requirements.txt

2. **Run the Application:**

   ```sh
   python app.py

The server will start on port 8820.

## Using Docker

1. **Build the Docker Image:**

   ```sh
   docker build -f DockerFile -t docx-to-pdf .

2. **Run the Docker Container:**

   ```sh
   docker run -p 8820:8820 docx-to-pdf

## API Endpoint

## API Endpoint

- **POST** `/convert`

  - **Description:** Convert an uploaded DOCX file to a PDF.
  - **Form Data:** 
    - `document` — DOCX file to convert.
  - **Response:** On success, returns the converted PDF file as an attachment.

## Troubleshooting

- Ensure Docker is installed if running in a container.
- Confirm LibreOffice is correctly installed in the Docker image.
- Check logs for any errors printed by the application.