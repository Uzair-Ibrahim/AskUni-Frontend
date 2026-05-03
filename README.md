# AskUni Chatbot - Frontend

This is the frontend interface for the FAST NUCES Chatbot, built using **Chainlit**. It features a custom theme and a mock backend for testing the user experience.

## 🚀 Features

* **User Interface:** Clean chat interface.
* **Custom Styling:** Dedicated theme (light/dark mode support).
* **Mock Backend:** A template `app.py` that simulates response delays to test the UI flow.

## 🛠️ Tech Stack

* **Framework:** Chainlit
* **Language:** Python
* **Design:** Custom CSS and JSON theme configurations

## 📂 Project Structure

* `app.py`: Main logic for the chat interface and UI testing.
* `/public`: Contains the university logo, custom CSS, and theme settings.
* `requirements.txt`: List of necessary Python packages.

## ⚙️ How to Run

1. **Create a Virtual Environment** (Optional):
   
   ```powershell
   python -m venv venv
   venv\Scripts\activate
   ```

2. **Install Dependencies:**
   
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch the App:**
   
   ```bash
   chainlit run app.py -w
   ```
