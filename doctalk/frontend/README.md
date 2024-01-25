# README

## Project Overview

This is a Next.js frontend for the Python backend available in this repo. It uses the AWS Lambda function option mentioned there to output a RAG Chat Application with the documentation of two products: Pinecone and OctoAI. The frontend is currently hardcoded to Pinecone, but that can be swapped easily.

## Features

- Utilize the AWS Lambda option from the Python backend.
- Pre-built Next.js starter to get started, quick.
- Tailwind, for easy plug and play with your own theme.

## Prerequisites

Before running this application, you need to make sure you are setup to run Next.js. Learn more in the [Next.js docs](https://nextjs.org/docs/getting-started/installation).

Additionally, you need to set up a `.env` file in the root of the project with the necessary environment variables.

- Your AWS API endpoint and key will be generated when you set up the backend.

## Environment Variables

Make sure you have the `.env` file in the project's root directory, following this template:

```
API_ENDPOINT=YOUR-ENDPOINT
API_KEY=YOUR-KEY
```

Replace the placeholder values with your actual AWS API keys and endpoints.

## Developing

Install dependencies

```bash
yarn
```

Start the dev server

```bash
yarn dev
```

## Deploying

The easiest way to deploy is by using [Vercel](https://vercel.com/docs/frameworks/nextjs), but you can use [any host](https://nextjs.org/docs/app/building-your-application/deploying#self-hosting) that supports Node.js.

## Contributing

Contributions to this project are welcome. Please ensure that your code adheres to the project's coding standards and includes appropriate tests.

## License

This project is licensed under the MIT License.
