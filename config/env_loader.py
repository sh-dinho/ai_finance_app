import os

def load_dotenv(path=".env"):
    if not os.path.exists(path):
        return

    with open(path, "r") as f:
        for line in f:
            line = line.strip()

            # Skip comments and empty lines
            if not line or line.startswith("#"):
                continue

            # Skip malformed lines
            if "=" not in line:
                continue

            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip()

            # Skip empty keys
            if not key:
                continue

            # Do not overwrite existing environment variables
            if key not in os.environ:
                os.environ[key] = value
