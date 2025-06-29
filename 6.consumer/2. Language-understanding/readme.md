Cancel Timer Assignment
This repository contains a solution for the "Cancel the Timer" assignment from the IoT-For-Beginners lesson on language understanding. The implementation uses Rasa for natural language understanding (NLU) and AWS Lambda for a serverless application, without relying on Azure or LUIS.
Instructions to Run

Set Up Environment:

Install Python 3.7+ and pip.
Install Rasa: pip install rasa.
Install AWS CLI and configure it with your AWS credentials.


NLU Model Setup:

Clone this repository: git clone <your-repo-url>.
Navigate to the project directory: cd <project-directory>.
Train the Rasa NLU model: rasa train.
The trained model will be saved as models/nlu.tar.gz.


Serverless Deployment:

Ensure lambda_function.py is in the project root.
Package the code and model into a ZIP file: Include lambda_function.py and models/nlu.tar.gz in a zip (e.g., function.zip).
Deploy to AWS Lambda: aws lambda update-function-code --function-name YourFunctionName --zip-file fileb://function.zip.
(Optional) Set up an API Gateway trigger if needed.


Testing:

Use the AWS Lambda console to test with inputs like "Cancel the timer" or "Stop the timer".
Check the logs in CloudWatch to verify the "Intent recognized: CancelTimer" message.
Expected response: {"response": "Timer cancelled"}.


Notes:

Ensure the Rasa model and Lambda function are compatible with your AWS region.
Adjust the Lambda handler code if using a different model path or intent name.



Files Included

nlu.yml: Rasa NLU configuration with "CancelTimer" intent examples.
lambda_function.py: AWS Lambda function to handle the intent and log recognition.

License
This project is for educational purposes only.
