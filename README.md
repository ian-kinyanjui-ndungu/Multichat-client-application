# Distributed Chat Application

## Project Overview
A scalable and secure distributed chat application built using Python, demonstrating advanced network programming concepts.

## Features
- Real-time messaging
- Secure client-server communication
- User authentication
- Encrypted message transmission
- Multi-threaded server architecture

## Prerequisites
- Python 3.8+
- pip package manager

## Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/distributed-chat-app.git

# Navigate to project directory
cd distributed-chat-app

# Install dependencies
pip install -r requirements.txt
```

## Configuration
1. Copy `.env.example` to `.env`
2. Modify configuration parameters as needed

## Running the Application
### Start Server
```bash
python run_server.py
```

### Start Client
```bash
python -m client.client
```

## Testing
```bash
# Run all tests
python -m unittest discover tests
```

## Project Structure
- `client/`: Client-side implementation
- `server/`: Server-side implementation
- `security/`: Encryption and security modules
- `utils/`: Utility functions and logging
- `tests/`: Unit and integration tests

## Contributing
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License
MIT License