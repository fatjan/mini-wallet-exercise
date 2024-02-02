# Mini Wallet Exercise

This repository contains an API backend service for managing a simple mini wallet.

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
    - Ensure MySQL is installed on your machine. If not, you can download it [here](https://dev.mysql.com/downloads/).
    - Run MySQL locally and create two databases: one for development (`wallet_db`) and another for testing (`test_db`).

6. **Configure Environment:**
    - Copy the `.env-template` file and rename it to `.env`.
    - Fill in the required credentials, ensuring the database name matches the ones created in step 5.

7. **Run the application:**
    ```bash
    flask run
    ```

8. **Run the tests:**
    ```bash
    flask test
    ```

9. **Database Operations:**
    ```bash
    flask db init
    flask db migrate
    flask db upgrade
    ```

10. **Format Python Files:**
    - To format a specific file:
        ```bash
        black path-to-file
        ```
    - To format all files in a directory:
        ```bash
        black .
        ```

11. **Reporting Issues:**
    If you encounter any issues, please create a new [issue here](https://github.com/fatjan/mini-wallet-exercise/issues).

Feel free to reach out if you have any questions or need further assistance!
