## Overview
This project is a chatbot named "HeyBuddy" that provides information about any campus or school or university. The chatbot is built using Flask, SQLite, and the Azure OpenAI service for natural language processing.

## Features
- User authentication for admin access
- Admin panel to view unresolved queries
- Chat interface for users to ask questions
- Integration with Azure OpenAI for intelligent responses

## Prerequisites
- Python 3.8+
- Azure account with OpenAI service set up
- An Azure VM for deployment

## Installation

1. **Clone the repository:**
    ```bash
    [git clone https://github.com/jithin2059/HeyBuddy.git]
    cd HeyBuddy
    ```

2. **Set up a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    
4. **Configure Azure OpenAI:**
   Update the `app.py` with your Azure endpoint and API key:
    ```python
    client = AzureOpenAI(azure_endpoint="YOUR_AZURE_ENDPOINT", azure_deployment="DEPLOYMENT", api_key="YOUR_API_KEY", api_version="2024-02-01")
    ```

## Running the Application

1. **Run the Flask application:**
    ```bash
    python main.py
    ```

2. **Access the application:**
   Open your browser and go to `http://127.0.0.1:5000/`.

## Deployment on Azure VM

1. **Create an Azure VM:**
   - Follow the Azure documentation to create a VM: [Create a Linux VM in the Azure portal](https://docs.microsoft.com/en-us/azure/virtual-machines/linux/quick-create-portal).

2. **SSH into your VM:**
    ```bash
    ssh your_username@your_vm_ip_address
    ```

3. **Install necessary packages:**
    ```bash
    sudo apt update
    sudo apt install python3-pip python3-venv
    ```

4. **Transfer your project files to the VM:**
   You can use SCP or any other method to transfer files.

    ```bash
    scp -r ./gitam-chatbot your_username@your_vm_ip_address:~/gitam-chatbot
    ```

5. **Set up the environment on the VM:**
    ```bash
    cd ~/gitam-chatbot
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

6. **Run the Flask application:**
    ```bash
    python main.py
    ```

7. **Configure firewall settings on Azure:**
   Ensure your VM's network security group allows traffic on port 5000.

## Usage

- **Login as Admin:**
  - Navigate to `/login` and use the default credentials (`admin` / `admin`).
  - View unresolved queries and manage the chatbot responses.

- **Chat Interface:**
  - Navigate to `/chatbot` to start interacting with the chatbot.
