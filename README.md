Athena AI Agent with Streamlit UI

Overview

The Athena AI Agent is an AI-driven application that enables users to interact with Amazon Athena using natural language. This project integrates AWS Bedrock, AWS Transcribe, and Streamlit to provide a seamless user experience. Users can either speak or type generic English statements, which are transformed into SQL queries using a Large Language Model (LLM). The generated queries are executed on Athena, and the results are displayed in real-time.
Features

    Natural Language Interface: Users can interact with Athena using spoken or written English.

    Speech-to-Text: Leverages AWS Transcribe to convert speech into text.

    AI-Powered Query Generation: Uses AWS Bedrock and an LLM to generate SQL queries from natural language input.

    Real-Time Query Execution: Executes the generated SQL queries on Amazon Athena and returns results in real-time.

    Streamlit UI: Provides an intuitive and interactive web interface for users.

    Multi-Table Support: Supports querying across three predefined tables in Athena.

Architecture

The application follows a serverless, AI-driven architecture:

    User Interaction:

        Users provide input via speech (using a microphone) or text (typed input) through the Streamlit UI.

    Speech-to-Text Conversion:

        If the input is speech, AWS Transcribe converts it into text.

    Query Generation:

        The text input is passed to the AWS Bedrock Agent, which uses an LLM to generate an SQL query.

    Query Execution:

        The generated SQL query is executed on Amazon Athena via a Lambda function.

    Result Display:

        The query results are returned to the Streamlit UI and displayed to the user in real-time.

plaintext
Copy

User -> Streamlit UI -> AWS Transcribe (if speech) -> AWS Bedrock Agent -> Lambda Function -> Athena -> Streamlit UI

Setup
Prerequisites

    An AWS Account with access to:

        Amazon Athena

        AWS Bedrock

        AWS Lambda

        AWS Transcribe

        Amazon S3

    Python 3.x

    AWS CLI configured with appropriate permissions

    Streamlit installed (pip install streamlit)

Steps

    Clone the Repository:
    bash
    Copy

    git clone https://github.com/jchowdhary/athenaAIAgent.git
    cd athenaAIAgent

    Set Up AWS Services:

        Athena: Create a database and tables in Athena pointing to your S3 data.

        Lambda: Deploy the Lambda function provided in the lambda directory.

        Bedrock Agent: Configure the Bedrock Agent to use the Lambda function as an Action Group.

        Transcribe: Ensure AWS Transcribe is enabled in your AWS account.

    Install Dependencies:
    bash
    Copy

    pip install -r requirements.txt

    Run the Streamlit Application:
    bash
    Copy

    streamlit run app.py

    Access the Application:

        Open the provided URL in your browser to access the Streamlit UI.

Usage

    Launch the Streamlit UI:

        Run the Streamlit application and open the UI in your browser.

    Provide Input:

        Use the microphone to speak your query or type it in the text box.

        Example: "Show total revenue by customer for 2023."

    View Results:

        The application will:

            Convert speech to text (if applicable).

            Generate an SQL query using the Bedrock Agent.

            Execute the query on Athena.

            Display the results in real-time.

Example Workflow
User Input

    Speech: "Find all orders placed in January 2023."

    Text: "Show the top 10 customers by total revenue."

Generated SQL
sql
Copy

SELECT *
FROM Orders
WHERE date_parse(orderdate, '%m/%d/%Y') BETWEEN date_parse('01/01/2023', '%m/%d/%Y') AND date_parse('01/31/2023', '%m/%d/%Y');

Response
json
Copy

{
    "results": [
        {
            "orderid": "12345",
            "customerid": "67890",
            "orderdate": "01/15/2023",
            "totaldue": "150.00"
        },
        {
            "orderid": "12346",
            "customerid": "67891",
            "orderdate": "01/20/2023",
            "totaldue": "200.00"
        }
    ]
}

Directory Structure
Copy

athenaAIAgent/
├── app.py                    # Streamlit application
├── lambda/                   # Lambda function code
│   ├── lambda_function.py    # Main Lambda handler
│   └── requirements.txt      # Python dependencies
├── scripts/                  # Utility scripts
│   ├── deploy.sh             # Deployment script
│   └── test.sh               # Testing script
├── docs/                     # Documentation
│   └── architecture.md       # Architecture overview
├── README.md                 # This file
└── LICENSE                   # License file

Contributing

Contributions are welcome! Please follow these steps:

    Fork the repository.

    Create a new branch for your feature or bugfix.

    Submit a pull request with a detailed description of your changes.

License

This project is licensed under the MIT License. See the LICENSE file for details.
Acknowledgments

    AWS Bedrock for AI-powered query generation.

    AWS Transcribe for speech-to-text conversion.

    Amazon Athena for serverless query execution.

    Streamlit for the interactive UI.

Contact

For questions or feedback, please contact:

    Author: [Your Name]

    Email: [Your Email]

    GitHub: [Your GitHub Profile]

This README provides a professional and comprehensive overview of your project, highlighting its AI-driven capabilities and user-friendly interface. Let me know if you need further refinements!


