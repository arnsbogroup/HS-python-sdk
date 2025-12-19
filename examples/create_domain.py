from heysender import (
    HeysenderClient,
    HeysenderException
)

# Build the client
client = HeysenderClient("your-api-key", "your-api-secret")

try:
    # Create domain
    raw_response = client.create_domain('example.heysender.com')
    print(f"Raw response: {raw_response}")

    # Get all domains on account
    raw_response = client.get_domains()
    print(f"Raw response: {raw_response}")

    # Get the latest request response object from the client
    responseObject = client.get_last_response()
    print(f"Last response json: {responseObject.json()}")
    print(f"Last response status code: {responseObject.status_code}")

except HeysenderException as e:
    # Handle exception
    print(f"Error ({e.status_code}): {e.message}")
