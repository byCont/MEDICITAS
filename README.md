# MEDICITAS

MEDICITAS is a web application designed to connect patients with medical specialists, allowing them to easily find and book appointments. The application is split into a React frontend and a FastAPI backend.

## Features

-   **User Authentication:** Secure registration and login for patients and doctors.
-   **Doctor Search:** Patients can search for doctors by specialty or name.
-   **Specialty Browsing:** Explore available medical specialties.
-   **Appointment Management:** Patients can view and manage their upcoming and past appointments.
-   **Doctor Profiles:** Detailed profiles for each doctor, including specialties and contact information.
-   **Responsive Design:** User-friendly interface across various devices.
-   **Theming:** Supports light and dark themes.

## Technologies Used

### Frontend

-   **React:** A JavaScript library for building user interfaces.
-   **TypeScript:** A superset of JavaScript that adds static typing.
-   **Vite:** A fast build tool for modern web projects.
-   **SCSS (Sass):** CSS preprocessor for enhanced styling capabilities.
-   **Bootstrap:** A popular CSS framework for responsive and mobile-first front-end web development.
-   **React Router DOM:** For declarative routing in React applications.

### Backend

-   **Python:** The programming language used for the backend.
-   **FastAPI:** A modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints.
-   **Uvicorn:** An ASGI server for FastAPI.
-   **Pydantic:** Data validation and settings management using Python type hints.
-   **SQLAlchemy (likely):** For database interactions (inferred from `seeds.py` and typical FastAPI setups).

## Prerequisites

Before you begin, ensure you have the following installed:

-   Node.js (LTS version recommended)
-   npm (comes with Node.js) or Yarn
-   Python 3.8+
-   pip (Python package installer)
-   Git

## Installation

Clone the repository:

```bash
git clone https://github.com/bycont/medicitas.git
cd medicitas
```

### Backend Setup

1.  Navigate to the `api` directory:
    ```bash
    cd api
    ```
2.  Create a Python virtual environment:
    ```bash
    python -m venv venv
    ```
3.  Activate the virtual environment:
    -   **Windows:**
        ```bash
        .\venv\Scripts\activate
        ```
    -   **macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```
4.  Install the backend dependencies:
    ```bash
    pip install -r requirements.txt
    ```
5.  Run database seeds (optional, for initial data):
    ```bash
    python run_seeds.py
    ```

### Frontend Setup

1.  Navigate to the `front` directory:
    ```bash
    cd ../front
    ```
2.  Install the frontend dependencies:
    ```bash
    npm install
    # or yarn install
    ```

## Running the Application

### Running the Backend (API)

1.  Ensure you are in the `api` directory and your virtual environment is activated.
2.  Start the FastAPI development server:
    ```bash
    uvicorn app.main:app --reload
    ```
    The API will be available at `http://127.0.0.1:8000` (or similar).

### Running the Frontend

1.  Ensure you are in the `front` directory.
2.  Start the Vite development server:
    ```bash
    npm run dev
    # or yarn dev
    ```
    The frontend application will be available at `http://localhost:5173` (or similar).

## API Endpoints (Overview)

The backend provides RESTful API endpoints for managing doctors, specialties, appointments, and user authentication. Key endpoints include:

-   `/doctors/`: CRUD operations for doctor information.
-   `/specialties/`: CRUD operations for medical specialties.
-   `/appointments/`: Manage patient appointments.
-   `/auth/`: User registration and login.

For detailed API documentation, once the backend is running, navigate to `http://127.0.0.1:8000/docs` (Swagger UI) or `http://127.0.0.1:8000/redoc` (ReDoc).

## Folder Structure

```
medicita/
├── api/                  # Backend (FastAPI)
│   ├── app/              # FastAPI application code
│   │   ├── __init__.py
│   │   ├── main.py       # Main FastAPI application
│   │   └── seeds.py      # Database seeding script
│   ├── requirements.txt  # Python dependencies
│   ├── run_seeds.py      # Script to run database seeds
│   └── venv/             # Python virtual environment
├── front/                # Frontend (React)
│   ├── public/           # Static assets
│   ├── src/              # React source code
│   │   ├── assets/       # Images, fonts
│   │   ├── components/   # Reusable React components
│   │   ├── contexts/     # React Context API for global state
│   │   ├── hooks/        # Custom React hooks
│   │   ├── interfaces/   # TypeScript interfaces
│   │   ├── pages/        # Page-level React components
│   │   ├── router/       # React Router configuration
│   │   └── services/     # API service integrations
│   ├── .env.development  # Environment variables for development
│   ├── .env.production   # Environment variables for production
│   ├── package.json      # Frontend dependencies and scripts
│   └── vite.config.ts    # Vite configuration
├── .gitignore
└── README.md             # This file
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

