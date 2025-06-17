# Smart Timer with LUIS 


## Components

1.  **`luis_simulator.py`**: A Flask-based web server that acts as a mock LUIS service. It parses text to identify intents (`SetTimer`, `CancelTimer`) and extracts entities (like duration).
2.  **`smart_timer_app.py`**: The main application. It includes:
    *   **Main Controller**: Takes user input, communicates with the LUIS simulator, and issues commands.
    *   **Virtual IoT Device**: Manages the timer itself (starting, stopping, announcing when time is up).

## Setup

1.  **Install Python**: Ensure you have Python 3.6+ installed.
2.  **Install Flask**: Flask is required for the LUIS simulator. Open your terminal or command prompt and run:
    ```bash
    pip install Flask requests
    ```
    (`requests` is used by `smart_timer_app.py` to talk to the simulator).

## How to Run

You'll need to run the LUIS simulator first, and then the smart timer application in a separate terminal.

1.  **Start the LUIS Simulator:**
    Open a terminal or command prompt, navigate to the directory where you saved the files, and run:
    ```bash
    python luis_simulator.py
    ```
    You should see output indicating the Flask server is running (e.g., `* Running on http://127.0.0.1:5000/`). Keep this terminal open.

2.  **Start the Smart Timer App:**
    Open a **new** terminal or command prompt, navigate to the same directory, and run:
    ```bash
    python smart_timer_app.py
    ```

3.  **Interact with the App:**
    The `smart_timer_app.py` terminal will prompt you for commands. Try things like:
    *   `set timer for 10 seconds`
    *   `create a timer for 1 minute`
    *   `set a timer for 1 minute and 30 seconds`
    *   `cancel timer`
    *   `stop the timer`
    *   `exit` (to close the smart timer app)

    You will see log messages in both terminals:
    *   The `luis_simulator.py` terminal will show the text it received and the intent it detected.
    *   The `smart_timer_app.py` terminal will show controller actions and virtual IoT device messages.

