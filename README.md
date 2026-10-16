# Welcome to Budget Buddy!

## About this App

Budget buddy is a budgeting app where you can plan your budget, track your expenses, and visualize them using charts.<br>
- The **Dashboard Page** contains the month's summary, budget breakdown, and the charts that visualize your budget and expenses.<br>
- The **Budget Page** is where you plan your budget and display all of your budget.<br>
- The **Expense Page** is where you track your expense history.

## How to Setup and Run Budget Buddy

**1. Install this app.** <br>
- In GitHub, click the green Code button then select download zip.<br>
- Extract the zip to a folder of your choosing.<br>

**2. Setup your virtual environment.** <br>
- Creating your virtual environment.<br>
```
python3 -m venv Budget_Buddy
```
- Activating your virtual environment.<br>
    + Windows
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  SP1\Scripts\activate
  ```
    + MacOS/LInux
  ```bash
  source SP1/bin/activate
  ```

**3. In your virtual environment, install streamlit and matplotlib.** <br>
```
pip install streamlit matplotlib
```

**4. Run the app.** <br>
```
streamlit run main.py
```

## Limitations

This app was created in these versions: <br>
- **Python Version**: 3.14.4
- **Streamlit Version**: 1.64.0
- **Matplotlib Version**: 3.11.2
