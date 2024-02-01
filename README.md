# mini-wallet-exercise
An API backend service for managing a simple mini wallet


## Installation

1. Clone the repository:

    ```bash
    git clone git@github.com:fatjan/mini-wallet-exercise.git
    ```

2. Create virtual environment:
    ```bash
    python -m venv venv
    ```

3. Activate virtual environment:
    ```bash
    source venv/bin/activate
    ```

4. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

5. Copy .env-template file and rename it to .env, fill in the required credentials

6. Run the application:
    ```bash
    flask run
    ```

7. Run the tests:
    ```bash
    flask test
    ```
    or 
    ```bash
    pytest
    ```
    Run a specific test file:
    ```bash
    pytest -k path-to-test-file
    ```
    Run a specific test file while seeing the print statement:
    ```bash
    pytest -k path-to-test-file -s
    ```

8. DB related:
    ```bash
    flask db init
    flask db migrate
    flask db upgrade
    ```

9. Format the python file:
    ```bash
    black path-to-file
    ```

    or in a directory consisting the files:
    ```bash
    black .
    ```