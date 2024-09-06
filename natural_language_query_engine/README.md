
# Project Setup Guide

Follow the steps below to set up the project and run the service:

## 1. Create a Virtual Environment

Before you begin, ensure that Python is installed on your machine. Then, create a virtual environment by running the following command:

```bash
python -m venv venv
```

Activate the virtual environment:

- On **Windows**:
  ```bash
  .\venv\Scripts\activate
  ```
- On **macOS/Linux**:
  ```bash
  source venv/bin/activate
  ```

## 2. Install Dependencies

Once your virtual environment is activated, install the required dependencies by running:

```bash
pip install -r requirements.txt
```

## 3. Set Up Environment Variables

Make sure to create a `.env` file in the root directory of the project. Inside the `.env` file, provide the following values:

```env
COUCHBASE_PASSWORD=your_couchbase_password
COUCHBASE_URL=your_couchbase_url
COUCHBASE_USERNAME=your_couchbase_username
OCTOAI_API_TOKEN=your_octoai_api_token
ENDPOINT_URL=your_octoai_endpoint_url
```

Replace `your_*` with the actual values.

## 4. Run the Service

After setting up the environment variables, you can run the service by executing:

```bash
python main.py
```

This will start the service as configured.