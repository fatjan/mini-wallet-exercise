# Mini Wallet Exercise

This repository hosts an API backend service for managing a simple mini wallet.


## Features

- **Wallet Management:**
  - Create and manage wallets for users.
  - Deposit funds into wallets.
  - Withdraw funds from wallets.

- **Transaction Tracking:**
  - Record and track all wallet transactions.
  - View transaction history.

- **Authorization:**
  - Secure API endpoints with token-based authorization.
  - Generate and use tokens for authenticated requests.

- **Database Interaction:**
  - Utilize MySQL for persistent data storage.
  - Implement database migrations for seamless updates.

- **Docker Support:**
  - Dockerize the application for easy deployment and isolation.


## Installation

1. **Clone the repository:**
    ```bash
    git clone git@github.com:fatjan/mini-wallet-exercise.git
    ```

2. **Create a virtual environment:**
    ```bash
    python -m venv venv
    ```

3. **Activate the virtual environment:**
    ```bash
    source venv/bin/activate
    ```

4. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5. **Set up MySQL:**
    - Ensure MySQL is installed on your machine. If not, download it [here](https://dev.mysql.com/downloads/).
    - Run MySQL locally and create two databases: one for development (`wallet_db`) and another for testing (`test_db`).

6. **Configure Environment:**
    - Copy the `.env-template` file and rename it to `.env`.
    - Fill in the required credentials, ensuring the database name matches the ones created in step 5.

7. **Migrate the Database:**
    ```bash
    flask db migrate
    flask db upgrade
    ```

8. **Run the application (without Docker):**
    ```bash
    flask run
    ```

    Access the App:
    - Open a web browser and navigate to `http://127.0.0.1:5000`

    To enable authorization:
    - Initiate the authorization process by making a request to the `/api/v1/init` endpoint.
    - Copy the generated token.
    - Click on "Authorize" in the top right corner of the application.
    - Paste the copied token into the authorization prompt with the following format "Token {your_pasted_token}".

9. **Run the tests (without Docker):**
    ```bash
    flask test
    ```

10. **Run the application using Docker:**
    - Build the Docker image:
        ```bash
        docker build -t mini_wallet_app .
        ```
    - Run the Docker container:
        ```bash
        docker run -p 5000:5000 mini_wallet_app
        ```

11. **Access Your Flask App:**
    - Open a web browser and navigate to `http://localhost:5000` to access your Flask app running inside the Docker container.

12. **Format Python Files:**
    - To format a specific file:
        ```bash
        black path-to-file
        ```
    - To format all files in a directory:
        ```bash
        black .
        ```

13. **Reporting Issues:**
    If you encounter any issues, please create a new [issue here](https://github.com/fatjan/mini-wallet-exercise/issues).

Feel free to reach out if you have any questions or need further assistance!
