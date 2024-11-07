# Personal Financial Manager

## Overview
The **Personal Financial Manager** is a web application designed to help users track their expenses and manage their finances. The backend is built with Django, while the frontend uses HTML and CSS with Bootstrap for a responsive and user-friendly interface.

## System Architecture
The architecture is composed of:
1. **Backend (Django)** - Manages data processing, user authentication, and business logic.
2. **Frontend (HTML, CSS with Bootstrap)** - Provides a responsive user interface for interacting with the application.
3. **Database** - Stores user-specific financial data, including expenses and income.

This architecture ensures a clear separation between the backend logic and frontend display, making the application more maintainable and scalable.

## Design Patterns
This project incorporates several design patterns to address specific design needs:

1. **Singleton** (Creational)
   - Ensures only one instance of essential services exists across the application, reducing redundant instantiation and maintaining a single source of truth.
   - Example: The Singleton pattern is applied to manage key services, ensuring that only one instance of each service is created throughout the application.

2. **Factory Method** (Creational)
   - Facilitates the creation of specific types of objects, enabling flexible and decoupled code.
   - Example: Used to generate different types of users, allowing for scalable and manageable user creation processes.

3. **Observer** (Behavioral)
   - Provides a subscription mechanism to notify different parts of the system when changes occur.
   - Example: The Observer pattern monitors changes in data (such as expenses) and sends notifications, ensuring that users are updated in real time when relevant data is modified.

## UML Diagrams
Currently, UML diagrams are not available for this project. Future updates may include:
- **Class Diagram** - To illustrate the relationships and patterns applied within the system.
- **Sequence Diagram** - To show the flow of interactions, such as expense management and balance updates.

These diagrams will provide a clearer view of the project structure and design patterns.

## Usage Instructions
1. **Installation**
   - Clone the repository: `https://github.com/alisherseitkadyr/Personal-Financial-Manager.git`
   - Install dependencies for the backend:
     ```bash
     cd backend
     pip install -r requirements.txt
     python manage.py migrate
     ```

2. **Running the Application**
   - Start the Django server:
     ```bash
     python manage.py runserver
     ```
   - Open a browser and go to `http://127.0.0.1:8000` to use the application.

3. **Register and Login**
   - Register a new user account or log in to access the application's financial management features.

4. **Tracking Finances**
   - Use the web interface to add, view, and manage expenses and monitor balance updates.

## Assumptions and Limitations
- **User-specific data** - Each user has a separate balance and financial records.
- **No Internet Connection Dependency** - The application operates fully offline, without requiring an internet connection.
- **Limitations**:
   - **No Multi-device Synchronization** - The current version does not support data synchronization across multiple devices or sharing a common database across users.
   - **Limited Analytics** - The application offers only basic expense and income tracking without advanced financial analysis or forecasting features.
   - **Single Currency Support** - The application currently supports only one currency, with no option for currency conversion.
   - **No Automatic Data Backup** - Users do not have built-in options for cloud or local backup of their financial data.
