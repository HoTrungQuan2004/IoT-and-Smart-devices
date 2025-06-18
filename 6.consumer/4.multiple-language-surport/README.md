# Universal Translator Project

This project demonstrates a simple, text-based universal translator using two virtual IoT devices and a central message hub.

## How it Works

1.  **`server.py`**: A lightweight Flask web server that acts as a message broker. It has two endpoints:
    *   `/send`: A device sends a message here. The hub stores it for the recipient.
    *   `/receive/<device_id>`: A device polls this endpoint to check for new messages addressed to it.

2.  **`device.py`**: A command-line script that represents a virtual device.
    *   It takes user input from the console.
    *   It sends the input text to the hub, addressed to the other device.
    *   In the background, it continuously polls the hub for incoming messages.
    *   When a message is received, it uses the `googletrans` library to translate the text into its own configured language and prints the result.

## Setup

1.  **Install Python**: Make sure you have Python 3.6+ installed.

2.  **Create a Virtual Environment**: Open your terminal in the project directory and run the following command to create a virtual environment named `venv`.

    ```bash
    python -m venv venv
    ```

3.  **Activate the Virtual Environment**: You need to "activate" the environment to start using it.

        source venv/bin/activate
       
    Your terminal prompt should change to show `(venv)` at the beginning, indicating the environment is active.

5.  **Install Dependencies**: With the virtual environment active, install the required libraries. This time, they will be installed inside the isolated environment, avoiding any conflicts.

    ```bash
    pip install Flask requests "googletrans==4.0.0-rc1"
    ```

## How to Run

You will need to open **three separate terminal windows**.

**Important**: In each new terminal, you must first navigate to the project folder and **activate the virtual environment** using the `source venv/bin/activate` command from Step 3.

### Terminal 1: Start the Hub

In the first terminal (with the venv activated), run the Flask hub.

```bash
python hub.py
```

### Terminal 2: Start Device 1 (e.g., English)

In the second terminal (with the venv activated), run the device script for English.

```bash
python device.py --id device1 --lang en --target-lang vi --target-id device2
```

### Terminal 3: Start Device 2 (e.g., Vietnamese)

In the third terminal (with the venv activated), run the device script for Vietnamese.

```bash
python device.py --id device2 --lang vi --target-lang en --target-id device1
```

## Usage

1.  With all three terminals running, type a message in English into the **Device 1** terminal and press Enter.
2.  The translated message (in French) will appear in the **Device 2** terminal.
3.  Now, type a message in French into the **Device 2** terminal.
4.  The translated message (in English) will appear back in the **Device 1** terminal.

To stop the project, you can press `Ctrl+C` in each terminal. To exit the virtual environment, simply type `deactivate`.