# Helium Mum Data Validation

## Overview

This project is designed to collect data from the Helium Mum database periodically and validate the user responses.

---

## Project Workflow

1. **Data Extraction**: Query the production database and import data.
2. **Data Normalization**: Normalize the response column from json formatted fields to tabular columns.
3. **Data Validation**: Perform data validation on user responses.
4. **Generate Report**: Generate validation report. 
5. **Send Email**: Send an email with the validation report attached.

---

## Getting Started

### Prerequisites

- Python 3.12
- Internet connection

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Helium-Data/HM-data-validation.git
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Environment Variables

Create a `.env` file in your project directory with the following structure:

```python
HOSTNAME='hostname'
USERNAME='username'
DATABASE='database'
PORT_ID='port_id'
PSWD='password'
SENDER_PASSWORD='sender_password'
```

### Usage

Run the script:
   ```bash
   python generate_report.py
   ```

### Key Functions

1. **import_data()**: Retrieves data from the database and stores it as a python dataframe.
2. **Flatten_data(dataframe)**: Normalizes the json formatted patient_response column values.
3. **Generate_data()**: Acts as the entry point for the process, performs the validation, generates the report and sends the email.
