import json
import pandas as pd
import numpy as np


def flatten_data(df):

    '''Filters the data into the different disease categories and 
    normalises the json column '''

    df['patient_response'] = df['patient_response'].apply(json.loads)

    normalized_dfs = []
    for index, row in df.iterrows():
        extracted = {}
        for entry in row["patient_response"]:
            for question in entry["questions"]:
                question_id = f"Q{entry['id']}{question['number']}"
                response = question["response"]

                if isinstance(response, list):
                    response = ", ".join(map(str, response))

                extracted[question_id] = response

        extracted["original_index"] = index
        normalized_dfs.append(extracted)

    df_normalized = pd.DataFrame(normalized_dfs)
    df_final = df.drop(columns=["patient_response"]).merge(df_normalized, left_index=True, right_on="original_index").drop(columns=["original_index"])


    return df_final

def create_val_cols(df, columns_to_check):
    '''creates validation columns'''
    
    for col in columns_to_check:
            if col not in df.columns:
                df[col] = None

    question_columns = [col for col in df.columns if col.startswith("Q") and not col.endswith("_val")]

    # Create validation columns dynamically
    for col in question_columns:
        df[f"{col}_val"] = np.where(df[col].isnull(), None, "valid")

    return df

def sum_missing_vals(df, excluded_cols):
    val_cols = {col for col in df.columns if col.startswith("Q") and col.endswith("_val")}
    excluded_cols = {"Q5b1_val", "Q5b2_val", "Q19a_val", "Q19b_val", "Q28a_val", "Q29a_val", "Q30a_val",
                      "Q31a_val", "Q32a_val", "Q38a_val", "Q38b_val", "Q39a_val"}
    compulsory_cols = list(val_cols - excluded_cols)
    total_missing_question = int(df[compulsory_cols].isnull().sum().sum())

    return total_missing_question

def prepare_report_table(df):
    val_cols = [col for col in df.columns if col.startswith("Q") and col.endswith("val")]

    # Count null values in validation columns
    null_counts = df[val_cols].isna().sum()

    # Filter columns with at least a null
    null_counts = null_counts[null_counts > 0]

    null_counts.index = null_counts.index.str.replace("_val", "", regex=True)

    if not null_counts.empty: 
        null_table = "\n".join([f"{col}: {count} invalid values" for col, count in null_counts.items()])
        null_report = f"\n\nColumns with invalid valid:\n{null_table}"
    else:
        null_report = "\n\nAll mandatory columns for this entry have valid data."

    return null_report




