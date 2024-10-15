# EventGate Backend

This project is the backend for EventGate, a Flask-based web application for generating and managing virtual event tickets. It uses Firebase for database storage and Pyrebase for Firebase integration. The application also supports CORS and sends confirmation emails to attendees.

### Project Structure

```
EventGate-Backend/
├── app.py
├── config.py
├── gen_uuid.py
├── mail.py
├── requirements.txt
├── test.py
└── vercel.json
```
### Files

- **[app.py](app.py)**: Main application file that sets up Flask routes and handles ticket creation and retrieval.
- **[config.py](config.py)**: Configuration file for Firebase and other settings.
- **[gen_uuid.py](gen_uuid.py)**: Contains the `generate_unique_id` function to generate unique user IDs.
- **[mail.py](mail.py)**: Handles sending emails to attendees.
- **[requirements.txt](requirements.txt)**: Lists the Python dependencies for the project.
- **[test.py](test.py)**: Contains test functions and utilities.
- **[vercel.json](vercel.json)**: Configuration file for deploying the application on Vercel.

## Setup

1. Clone the repository:
    ```sh
    git clone https://github.com/riz4d/EventGate-Backend/tree/main
    cd EventGate-Backend
    ```

2. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```

3. Configure Firebase:
    - Update `firebase_config` in `config.py` with your Firebase project details.

4. Run the application:
    ```sh
    python app.py
    ```

## API Endpoints

### Create Ticket

- **URL**: `/api/ticket`
- **Method**: `POST`
- **Description**: Creates a new ticket for an attendee.
- **Request Body**:
    ```json
    {
        "fullname": "John Doe",
        "email": "john.doe@example.com"
    }
    ```
- **Response**:
    ```json
    {
        "status": true,
        "message": "Ticket created",
        "data": {
            "fullname": "John Doe",
            "email": "john.doe@example.com",
            "userId": "12345678",
            "attendeeType": "participant",
            "present": false
        },
        "id": "12345678"
    }
    ```

### Get All Ticket IDs

- **URL**: `/api/ticket`
- **Method**: `GET`
- **Description**: Retrieves all ticket IDs.

## Functions

### `generate_unique_id`

- **File**: [gen_uuid.py](gen_uuid.py)
- **Description**: Generates a unique user ID.
- **Usage**:
    ```python
    from gen_uuid import generate_unique_id
    new_id = generate_unique_id()
    ```

### `send_email`

- **File**: [mail.py](mail.py)
- **Description**: Sends an email to the attendee.
- **Usage**:
    ```python
    from mail import send_email
    status_code, response = send_email(attendee_email, subject, text_content, attendee_name, attendee_email, user_id, ticket_type, qr_code_url)
    ```
## Contributing

We welcome contributions to improve EventGate-Backend! To contribute, follow these steps:

1. Fork the repository.
2. Create a new branch:
    ```sh
    git checkout -b feature-branch
    ```
3. Make your changes and commit them:
    ```sh
    git commit -m "Description of your changes"
    ```
4. Push to the branch:
    ```sh
    git push origin feature-branch
    ```
5. Open a pull request describing your changes.

Please ensure your code adheres to the existing style and includes appropriate tests.

## Issues

If you encounter any issues or have suggestions for improvements, please open an issue on the [GitHub Issues](https://github.com/riz4d/EventGate-Backend/issues) page.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.