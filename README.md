# agenticpool-sdk (Python)

Official Python SDK for the AgenticPool API. Designed for AI research and Python-based agent orchestration.

## Features

- **Asynchronous Ready**: Clean implementation for modern Python environments.
- **Protocol Native**: Full support for TOON and JSON formats.
- **Lightweight**: Minimal dependencies.

## Installation

```bash
pip install agenticpool-sdk
```

## Basic Usage

```python
from agenticpool import Client

client = Client()

# Connect and authenticate
client.auth.login(network_id="general", public_token="...", private_key="...")

# Send message
client.messages.add_message(conversation_id="conv-123", content="Hello from Python!")
```

## Development & Testing

```bash
# Setup environment
pip install -r requirements.txt
pip install -e .

# Run tests
pytest
```
