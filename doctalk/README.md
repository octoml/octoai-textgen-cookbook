# How to build a complete document Q&A chatbot using RAG powered by Langchain, OctoAI and Pinecone

## Project Overview

This "DocTalk" project presents a full stack RAG application that lets the user perform Q&A tasks on a documentation source of your choice. By default, we're performing documentation Q&A on the [Pinecone documentation pages](https://docs.pinecone.io/docs/quickstart).

Let's take a look at the layers that compose this full stack RAG application:
* We've built our RAG backend using Langchain in Python. The RAG example leverages Pinecone to provide a vector database, and OctoAI to provide an embedding (GTE-Large) and LLM (Mixtral-8x7B) API.
* This RAG Python backend containerized and deployed on an AWS Lambda which lets us easily connect any frontend to its serverless API.
* Finally we've built a Next.js front end which sents its request to the AWS Lambda to perform RAG on the documentation source. This Next.js frontend can be easily deployed on Vercel.

The application demonstrates how to do document processing, embedding generation, and conversational retrieval using the OctoAI LLM and Embeddings models and Pinecone as a Vector DB. It is designed to be run both as a command-line interface (CLI) application, as an AWS Lambda function, or as a Next.js user facing applications.


### This project is divided into 4 parts:

1. **Vector database setup**: you'll learn how to load and process documents from specified URLs, convert text data into embedding vector that will then be stored in a vector database hosted on Pinecone.
2. **Langchain Python app**: you'll run a standalone langchain app in Python that will let you perform simple RAG-based document question and answering against the vector database that we'll have set up in step 1.
3. **AWS Lambda setup**: you'll containerize the Langchain Python app using Docker and deploy it as an AWS Lambda serverless function.
4. **Frontend testing and deployment**: you'll run and deploy a Next.js frontend for your app on Vercel to allow anyone to perform documentation Q&A on a streamlined webapp.


## Features

### Back-end
- Load and process documents from specified URLs.
- Generate embeddings for text data using OctoAI embedding API.
- Populate your embedding vectors into a Pinecone vector database.
- Leverage the OctoAI LLM endpoints for language understanding and processing (specifically OctoAI).
- Compatible with AWS Lambda for serverless deployment.

### Front-end
- Utilize the AWS Lambda option from the Python backend.
- Pre-built Next.js starter to get started, quick.
- Tailwind, for easy plug and play with your own theme.

## Prerequisites

### API Tokens

For this RAG example, we'll be using Pinecone for the vector database:
-   To get a Pinecone API Key: please follow the steps [here](https://docs.pinecone.io/docs/quickstart)

We'll also be using OctoAI for the embedding model and LLM APIs:
-   To get an OctoAI API Token: please follow the steps [here](https://octo.ai/docs/getting-started/how-to-create-octoai-api-token)

### Python Setup

Before running this application, you need to have Python installed on your system along with the application dependencies. You can use tools like `conda`, `poetry`, or `virtual env` to manage your Python environments.

If you're using virtual env, you can run the following from this top level directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Then you can install these packages using pip:

```bash
python3 -m pip install -r requirements.txt
```

### Playwright

The Langchain document loader we are using requires the playwright module. It needs to be initialized before first use. This can be done with the following command:

```bash
python3 -m playwright install
```

### Next.js

Before running this application, you need to make sure you are set up to run Next.js. Learn more in the [Next.js docs](https://nextjs.org/docs/getting-started/installation).

## 1 - Vector DB Setup

### Environment Setup

Make sure you have the `.env` file in the project's `1_vector_db/` directory, following this template:

```
PINECONE_API_KEY=YOUR-PINECONE-TOKEN
PINECONE_ENV=gcp-starter
OCTOAI_TOKEN=YOUR-OCTOAI-TOKEN
```

It's highly likely you'll be getting started in Pinecone's `gcp-starter` pod environment if you're using the free tier of their service. See what other pod environments are available on [their documentation page](https://docs.pinecone.io/docs/indexes#pod-environments).

Replace the placeholder values with your actual API keys and endpoints, which you can obtain by following the pre-requisite steps above.

### Setting up the Vector DB

To set up the Pinecone Vector DB, go ahead and run the following script in `1_vector_db`:

`python3 init_vectordb.py`

It will take several minutes to scrape the documents, perform pre-processing of the text information, convert to the vector space, and populate the pinecone index.

You should see an output that looks as follows after executing the script. You can ignore the Beautiful Soup warning.

```
Initializing the Pinecone index...
Loading the content we want to run RAG on, this could take a couple of minutes...
/Users/moreau/Documents/Projects/octoai-textgen-cookbook/doctalk/1_vector_db/init_vectordb.py:46: MarkupResemblesLocatorWarning: The input looks more like a filename than markup. You may want to open this file and pass the filehandle into Beautiful Soup.
  return {"page_content": str(BeautifulSoup(content, "html.parser").contents)}
Preprocessing the data before storing in the vector DB
Adding the vector embeddings into the database, this could take a couple of minutes...
Done!
```

This code was tested on MacOS and Ubuntu.

## 2 - RAG Langchain App

### Environment Setup

Make sure you have the `.env` file in the project's `2_langchain` directory, following this template:

```
PINECONE_API_KEY=YOUR-TOKEN
PINECONE_ENV=gcp-starter
OCTOAI_TOKEN=YOUR-TOKEN
OCTOAI_ENDPOINT_URL="https://text.octoai.run/v1/chat/completions"
OCTOAI_MODEL="llama-2-13b-chat-fp16"
```

Replace the placeholder values with your actual API keys and endpoints. Do remember to update the `PINECONE_ENV` variable if you are using an existing Pinecone environment.

## Running the Application

### As a Command-Line Interface

To run the application via CLI, execute the main script:

`python main.py`

You will be prompted to enter the data source and your query. After providing the necessary inputs, the application will process the request and display the output.

-   This code was tested on MacOS and Ubuntu

## 3 - AWS Lambda Setup

The application can also be deployed as an AWS Lambda function. To do so, package the application with the required dependencies and upload it to AWS Lambda. Set the handler function as `main.handler`.

### Deploying the Application to AWS Lambda as a Container Image

#### Prerequisites:

-   AWS Account

-   AWS CLI configured

-   Docker installed

-   AWS SAM CLI installed (see https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)

#### _Using AWS SAM CLI and Docker:_

To deploy this Python application to AWS Lambda using a container image,
you will need to follow these steps:

_Prepare the Dockerfile:_ Ensure the Dockerfile is set up correctly to
build a container image suitable for AWS Lambda. This involves
specifying the base image, copying your application code into the
container, installing any dependencies, and setting the entry point for
your Lambda function. We've provided you with a Dockerfile that meets
the requirements stated above so you can edit it.

_Build the Container Image:_ Use AWS SAM CLI to build your container
image. Run the following command from the `app/` directory:

`sam build --use-container`

#### _Deploy to AWS Lambda:_

First, you need to upload your container image to Amazon Elastic
Container Registry (ECR). You can do this using the Docker CLI.

The commands below assume your region is us-east-1, and you can modify it accordingly.



`aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <YOUR_AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com`

`docker tag doctalkfunction:v1 <YOUR_AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/doctalkfunction:v1`

`docker push <YOUR_AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/doctalkfunction:v1`

Second, you need to create a lambda function of type container image from the uploaded docker image. You can do that from the AWS console by going to Lambda and then clicking Create new function as shown below

![](media/image4.png)


Configure Lambda and API Gateway: After deployment, you need to
configure your Lambda function in the AWS Management Console

####

####

#### _Increase the function timeout, and scale up the resource specs_

####

From the lambda function management console, go to General Configuration
and change the Timeout to 15 mins. Also since the compute resources are
allocated based on the Memory size you give to the lambda function, it
is a good idea to increase the Memory to 2048 MB

![](media/image1.png)

#### _Add configuration variables_

![](media/image2.png)

#### _Create API Gateway_

Use the python
script at `api-gateway.py` to create an API gateway for the lambda
function that allows clients to call it over HTTPS.

## 4 - Frontend Setup

WIP

## Contributing

Contributions to this project are welcome. Please ensure that your code adheres to the project's coding standards and includes appropriate tests.

## License

This project is licensed under the MIT License.
