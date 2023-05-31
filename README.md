# SMS-TextGPT

SMS-TextGPT is a simple Flask implementation of OpenAI's ChatGPT that incorporates Telnyx SMS for sending and receiving text messages. This application allows you to have interactive conversations with an AI-powered language model using SMS.

<div>
    <img src="screenshots/screenshot1.PNG" alt="Screenshot 1" width="400" />
    <img src="screenshots/screenshot2.PNG" alt="Screenshot 2" width="400" />
</div>

## Prerequisites

Before running this code, make sure you have the following:

- Python 3.x installed on your machine.
- The required Python packages installed. You can install them using pip with the following command:

```bash
pip install flask openai telnyx
or
pip install -r requirements.txt
```
- API keys for both OpenAI and Telnyx. Set the environment variables in the `.env` file for OPENAI_API_KEY and TELNYX_API_KEY to the respective API keys.
- A Telnyx [phone number](https://telnyx.com/products/phone-numbers). These can be purchased for around $1 and send messages at an extremely cheap rate. Set the value for your phone number in the `.env` file with name TELNYX_PHONE_NUMBER.

## Features
- Uses OpenAI's ChatGPT model (gpt-3.5-turbo) for generating AI responses.
- Handles incoming SMS messages and sends AI-generated replies using Telnyx SMS.
- Maintains conversation history for each phone number communicating with the application

## Installation
1. Clone this repository or download the source code.
```bash
git clone https://github.com/johngordley/sms-textgpt.git
```
2. Install the required dependencies as mentioned in the prerequisites section.
3. Set the environment variables for your API keys and Telnyx phone number
4. Set up your Telnyx messaging profile to point to your webhook endpoint. In order to do this, you will need to either host this application or expose a local endpoint on your machine using a service such as [ngrok](https://ngrok.com/). Below you can see my local ngrok URL in the messaging profile for my Telnyx number:
![Screenshot 1](screenshots/screenshot3.PNG)
A more detailed tutorial on this setup can be found in the [Telnyx Developer Docs: Receiving a Message Tutorial](https://developers.telnyx.com/docs/v2/messaging/messages/tutorials/receive_message/receive_message/).
4. Run the application
```bash
flask run
or
python app.py
```

## Usage
Once the application is running, it listens for incoming SMS messages at the /webhooks endpoint. Remember to configure your Telnyx account to forward incoming messages to the URL where this application is hosted or you will not receive any messages.

To have a conversation with the AI, simply send an SMS to your Telnyx phone number associated with this application. The application will process the message, generate an AI response using OpenAI's ChatGPT, and send it back to the sender.

## Contributing
Contributions are welcome! If you find any issues or have suggestions for improvement, please open an issue or submit a pull request on the GitHub repository.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

## Authors
- [John Gordley](https://github.com/jgordley)

## Acknowledgements
- This project is based on OpenAI's GPT-3.5 language model and Telnyx SMS API.
- Thanks to the Flask and Telnyx communities for their contributions.