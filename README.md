# Djangologue

Djangologue is a real-time chat application built with Django, utilizing Django Rest Framework for RESTful APIs, Django Channels for handling WebSockets, and Daphne as the ASGI server.

## Features

- Real-time messaging: Engage in instant messaging with other users using WebSockets for real-time communication.
- User authentication and room permission checks: Securely login to access the chat application and join only the rooms you have permission to access, ensuring privacy and security.
- Message storage and retrieval: All messages are stored in the database and can be retrieved via a RESTful API endpoint.



## Requirements

- Python 3.x
- Django
- Django Rest Framework
- Django Channels
- Daphne

## Installation

1. Clone the repository:

```bash
git clone git@github.com:aminamerian/djangologue.git
```
2. Install dependencies:

```bash
cd djangologue
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
3. Apply migrations:
```bash
python manage.py migrate
```
4. Run the development server:
```bash
python manage.py runserver
```
5. Access the application at http://localhost:8000/.

## Contributing
Contributions are welcome! Please feel free to open issues or submit pull requests.
