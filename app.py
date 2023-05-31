import os
from flask import Flask, request
from flask_cors import CORS
import openai
import telnyx

telnyx.api_key = os.getenv("TELNYX_API_KEY")
your_telnyx_number = "+17577317540"
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
cors = CORS(app)

history_dict = {}

def SendChatRequest(from_number):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=history_dict[from_number],
        max_tokens=150
    )

    return response['choices'][0]['message']['content']

def SendChatResponse(message, to_number):
    telnyx.Message.create(
        from_=your_telnyx_number,
        to=to_number,
        text=message
    )

@app.route('/webhooks', methods=['POST'])
def webhooks():
    body = request.json
    message_id = body["data"]["payload"]["id"]
    from_number = body["data"]["payload"]["from"]["phone_number"]
    text = body['data']['payload']['text']

    if from_number != your_telnyx_number:

        print(f"Received inbound message with ID: {message_id}")
        print(f"From number: {from_number}")
        print(f"Message text: {text}")

        if history_dict.get(from_number, 0):
            history_dict[from_number].append({'role': 'user', 'content': text})
        else:
            history_dict[from_number] = [{'role': 'user', 'content': text}]

        llm_response = SendChatRequest(from_number)
        history_dict[from_number].append({'role': 'system', 'content': llm_response})

        print(history_dict)
        SendChatResponse(llm_response, from_number)

    return '', 200

if __name__ == '__main__':
    app.run(debug=True)