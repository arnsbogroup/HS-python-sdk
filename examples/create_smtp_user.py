from heysender import (
    HeysenderClient,
    HeysenderException,
    AnonymizeOption
)

# Build the client
client = HeysenderClient("your-api-key", "your-api-secret")

try:
    # Get domains
    client.get_domains()
    domains = client.get_last_response().json()
    print(f"Raw response: {domains}")

    # Create smtp user on a specific domain id
    raw_response = client.create_smtp_user(domains[0]['id'], f"example@{domains[0]['url']}",[AnonymizeOption.CONTENT, AnonymizeOption.SUBJECT])
    print(f"Raw response: {raw_response}")

    # Get the latest request response object from the client
    responseObject = client.get_last_response()
    print(f"Last response json: {responseObject.json()}")
    print(f"Last response status code: {responseObject.status_code}")

    # Get all smtp users on domain
    raw_response = client.get_smtp_users(domains[0]['id'])
    print(f"Raw response: {raw_response}")

    # Get the latest request response object from the client
    responseObject = client.get_last_response()
    print(f"Last response json: {responseObject.json()}")
    print(f"Last response status code: {responseObject.status_code}")

except HeysenderException as e:
    # Handle exception
    print(f"Error ({e.status_code}): {e.message}")
