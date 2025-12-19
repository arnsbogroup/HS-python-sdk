from heysender import (
    HeysenderClient,
    MessageBuilder,
    HeysenderException,
    AnonymizeOption
)

# Build the client
client = HeysenderClient("your-api-key", "your-api-secret")

# Build the message
message = (MessageBuilder(
    from_email="sender@yourdomain.com",
    from_name="Your Name",
    subject="Test Email",
    html="<h1>Hello</h1><p>World!</p>"
)
.add_to("example@heysender.com", "Mr. Sender")
.add_bcc("example2@heysender.com")
.set_tracking(True)
.add_tag("tagTest", "some tag")
.set_anonymize_options([AnonymizeOption.CONTENT, AnonymizeOption.SUBJECT])
.build()
)

try:
    # Send the message and get response in return
    raw_response = client.send_message(message)
    print(f"Success: {raw_response}")

    # Get the latest request response object from the client
    responseObject = client.get_last_response()
    print(f"Last response text: {responseObject.text}")
    print(f"Last response status code: {responseObject.status_code}")

except HeysenderException as e:
    # Handle exception
    print(f"Error ({e.status_code}): {e.message}")
