<<<<<<< HEAD
# Python Data Analysis & Statistical Modeling Project

This project is a Python-based data analysis tool designed to automate data extraction from Excel files, perform data cleaning, and execute statistical modeling using `statsmodels`.

## 📂 Project Structure

- **main.py**: The main entry point of the application. It coordinates the analysis workflow.
- **functions.py**: A modular script containing helper functions for data processing and custom calculations.
- **requirements.txt**: A list of external libraries required to run the project.

## 🛠 Technologies & Libraries

The project leverages the following Python libraries:

- **Pandas**: For data manipulation and handling Excel files.
- **NumPy**: For numerical computations.
- **Statsmodels**: For conducting statistical tests and building models (e.g., Regression).
- **Openpyxl**: The engine used by Pandas to read and write `.xlsx` files.
- **SciPy/Patsy**: Supporting libraries for advanced statistical operations.

## 🚀 Getting Started

### Prerequisites

Ensure you have Python 3.13 installed on your system.

### Installation

1. **Clone or download** the project files to your local machine.

2. (Optional) **Create a virtual environment** to keep dependencies isolated:
   ```bash
   python -m venv venv

3. **Activate the virtual environment:**
    For Windows: venv\Scripts\activate
    for macOS or Linux : source venv/bin/activate

4. **Install the required dependencies**
    Use this command in terminal: pip install -r requirements.txt

5. **Usage**

    Place your data file in exm_datasets, there is one example dataset in file

    Run the analysis like this:
        If you have your variables between columns <start_column> <end_column>:
        python main.py path\to\data.xlsx <start_column> <end_column>

        For example:
        python main.py exm_datasets\data.xlsx 1 5

    
    Data Orientation: Your variables must be in different columns, not in rows.Result
    Placement: Your result/target table should be located after the $n^{th}$ column (where $n$ is your specified end column).
    File Format: Currently, only .xlsx files are supported. New updates for other formats are coming soon.

6. **UPDATES (V 1.1.0)**
    For optimizing O() and memory usage, lasso algorithm have been used with ridge.
    First version of the program, testdata2 used 491.65 MB at peak. Currently, it is decreased to 5.93 MB

        

=======



