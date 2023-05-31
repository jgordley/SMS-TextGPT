# SMS-TEXTGPT by Jack Gordley
# SMS chatbot powered by OpenAI's GPT-3 and Telnyx's SMS API
import os
from dotenv import load_dotenv
from flask import Flask, request
import openai
import telnyx

# Load environment variables from .env file
load_dotenv()
telnyx.api_key = os.getenv("TELNYX_API_KEY")
your_telnyx_number = os.getenv("TELNYX_PHONE_NUMBER")
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize flask application
app = Flask(__name__)

# Initialize message history dictionary with keys being phone numbers and values
# being a list of messages
history_dict = {}

# Generate response using OpenAI model
def SendChatRequest(from_number):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=history_dict[from_number],
        max_tokens=150
    )
    return response['choices'][0]['message']['content']

# Send SMS message to user using Telnyx API
def SendChatResponse(message, to_number):
    telnyx.Message.create(
        from_=your_telnyx_number,
        to=to_number,
        text=message
    )

# Handle inbound SMS messages from Telnyx number
@app.route('/webhooks', methods=['POST'])
def webhooks():
    body = request.json
    message_id = body["data"]["payload"]["id"]
    from_number = body["data"]["payload"]["from"]["phone_number"]
    text = body['data']['payload']['text']

    # Only look at message events generated from external numbers
    if from_number != your_telnyx_number:
        print(f"Received inbound message with ID: {message_id}")
        print(f"From number: {from_number}")
        print(f"Message text: {text}")

        # Add message to history dictionary
        if history_dict.get(from_number, 0):
            history_dict[from_number].append({'role': 'user', 'content': text})
        else:
            history_dict[from_number] = [{'role': 'user', 'content': text}]

        # Generate response and add to history dictionary
        llm_response = SendChatRequest(from_number)
        history_dict[from_number].append({'role': 'system', 'content': llm_response})

        # Send response back to the sender
        SendChatResponse(llm_response, from_number)

    return '', 200

if __name__ == '__main__':
    app.run(debug=True)