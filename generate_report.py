import numpy as np
from import_data import import_data
from process_data import create_val_cols, flatten_data, sum_missing_vals, prepare_report_table
from datetime import datetime, timedelta
from send_email import send_email
import os

def generate_report():

    # Import the data
    df = import_data()
    diseases = ['HIV','Tuberculosis', 'Diabetes']
    disease_df = {}

    # Split the data
    for disease in diseases:
        disease_df[f"df_{disease}"] = df[df['disease'] == disease]

        # Flatten the data
        if not disease_df[f"df_{disease}"].empty:
            disease_df[f"df_{disease}"] = flatten_data(disease_df[f"df_{disease}"])
    
    df_HIV = disease_df["df_HIV"].drop(columns='disease')
    df_TB = disease_df["df_Tuberculosis"].drop(columns='disease')
    df_diabetes = disease_df["df_Diabetes"].drop(columns='disease')

    # run the specific validation per disease and generate the report
    #--------------------------- HIV -------------------------------------
    if not df_HIV.empty:

        # Fill out the df
        
        columns_to_check = [f"Q{i}a" for i in range(1, 23)]

        # Add validation columns
        df_HIV = create_val_cols(df_HIV, columns_to_check)

        # Answer val cols
        HIV_total_expected_questions = df_HIV.shape[0] * 16

        # Missing compulsory/follow up questions
        # If yes to 9a, answer 10a -15a
        for i in range(10, 16):
            df_HIV[f"Q{i}a_val"] = np.where((df_HIV['Q9a'] == "Yes") & (df_HIV[f"Q{i}a"].notna()), "valid", 
                                            np.where((df_HIV['Q9a'] == "No") & (df_HIV[f"Q{i}a"].isna()), "valid", None))
        

        # If 2a male then 10a must not null
        # df_HIV['Q10a_val'] = np.where((df_HIV['Q9a'] == "Yes") & (df_HIV['Q10a'].notna()) , "valid",
        #                               np.where((df_HIV['Q9a'] == "No") & (df_HIV['Q10a'].isna()), "valid", None))
        
        
         #########

        
        HIV_total_missing_question = int(df_HIV[[f"Q{i}a_val" for i in range(1, 23)]].isnull().sum().sum())


    #--------------------------- Tuberculosis -------------------------------------
    if not df_TB.empty:

        # Fill out the df
        columns_to_check = [f"Q{i}a" for i in range(1, 19)]
        columns_to_check.insert(columns_to_check.index('Q8a') + 1, "Q8b")
        columns_to_check.insert(columns_to_check.index('Q8b') + 1, "Q8c")


        # Add validation columns
        df_TB = create_val_cols(df_TB, columns_to_check)

        # Answer val cols
        TB_total_expected_questions = df_TB.shape[0] * 18

        # Missing compulsory/follow up questions
        # If 8a yes, then 8b&8c must not be null
        df_TB['Q8b_val'] = np.where((df_TB['Q8a'] == "Yes") & (df_TB['Q8b'].notna()) , "valid",
                                    np.where((df_TB['Q8a'] != "Yes") & (df_TB['Q8b'].isna()) , "valid", None))
        df_TB['Q8c_val'] = np.where((df_TB['Q8a'] == "Yes") & (df_TB['Q8c'].notna()) , "valid",
                                    np.where((df_TB['Q8a'] != "Yes") & (df_TB['Q8c'].isna()) , "valid", None))

        # Add all mising values in validation columns
        TB_total_missing_question = int(df_TB[[col for col in df_TB.columns if col.startswith("Q") and col.endswith("_val")]].isnull().sum().sum())

        #-------------------------- Diabetes -----------------------------------------
    if not df_diabetes.empty:
        
        # Fill out the df
        columns_to_check = [f"Q{i}a" for i in range(1, 40)]
        columns_to_check.insert(columns_to_check.index('Q5a'), "Q5b")
        columns_to_check.insert(columns_to_check.index('Q5b'), "Q5b1")
        columns_to_check.insert(columns_to_check.index('Q5b1'), "Q5b2")
        columns_to_check.insert(columns_to_check.index('Q19a'), "Q19b")
        columns_to_check.insert(columns_to_check.index('Q38a'), "Q38b")

        
        # Add validation columns
        df_diabetes = create_val_cols(df_diabetes, columns_to_check)

        # Answer val cols
        # diabetes_total_expected_questions = df_TB.shape[0] * 32
        
        # If you answered ‘Yes’ to 5a, 5b(1,2,3 are compulsory)
        for i in range(1, 3):
            df_diabetes[f"Q5b{i}_val"] = np.where((df_diabetes['Q5a'] == "Yes") & (df_diabetes[f'Q5b{i}'].notna()), "valid", 
                                                  np.where((df_diabetes['Q5a'] == "No") & (df_diabetes[f'Q5b{i}'].isna()), "valid", None))

        df_diabetes[f"Q5b_val"] = np.where((df_diabetes['Q5a'] == "Yes") & (df_diabetes['Q5b'].notna()), "valid", 
                                                  np.where((df_diabetes['Q5a'] == "No") & (df_diabetes[f'Q5b'].isna()), "valid", None))


        # If 19a is yes, then 19b must not be null;
        df_diabetes['Q19b_val'] = np.where((df_diabetes['Q19a'] == "Yes") & (df_diabetes['Q19b'].notna()) , "valid",
                                           np.where((df_diabetes['Q19a'] != "Yes") & (df_diabetes['Q19b'].isna()), "valid", None))

        # 28a yes continue to 29-32; no skip to 33
        # # If 28a is yes, then 29-32 must not be null; 
        for i in range(29, 33):
            df_diabetes[f"Q{i}a_val"] = np.where((df_diabetes['Q28a'] == "Yes") & (df_diabetes[f"Q{i}a"].notna()), "valid", 
                                                 np.where((df_diabetes['Q28a'] != "Yes") & (df_diabetes[f"Q{i}a"].isna()), "valid", None))

        df_diabetes["Q33a_val"] = np.where((df_diabetes['Q2a'] == "Male") & (df_diabetes["Q33a"].isna()), "valid", df_diabetes["Q33a_val"])
             
        
     
        # if 2a is female then 28a must not be null
        df_diabetes["Q28a_val"] = np.where((df_diabetes['Q2a'] == "Female") & (df_diabetes["Q28a"].notna()), "valid", 
                                                 np.where((df_diabetes['Q2a'] == "Male") & (df_diabetes['Q28a'].isna()), "valid", None))

        # If 38a is yes, then 38b must not be null;
        df_diabetes['Q38b_val'] = np.where((df_diabetes['Q38a'] == "Yes") & (df_diabetes['Q38b'].notna()) , "valid", 
                                           np.where((df_diabetes['Q38a'] == "No") & (df_diabetes['Q38b'].isna()), "valid", None))

        val_cols = {col for col in df_diabetes.columns if col.startswith("Q") and col.endswith("_val")}
        excluded_cols = {"Q5b1_val", "Q5b2_val", "Q19a_val", "Q19b_val", "Q28a_val", "Q29a_val", "Q30a_val",
                          "Q31a_val", "Q32a_val", "Q38a_val", "Q38b_val", "Q39a_val"}
        compulsory_cols = list(val_cols - excluded_cols)
        diabetes_total_missing_question = int(df_diabetes[[col for col in df_diabetes.columns if col.startswith("Q") and col.endswith("_val")]].isnull().sum().sum())
        # diabetes_total_missing_question = int(df_diabetes[compulsory_cols].isnull().sum().sum())

    # ---------------------------------Report------------------------------------------------
    report_date = datetime.today().strftime('%b %d, %Y')
    end_date = datetime.now()
    start_date = end_date - timedelta(days=1)
    start_date = start_date.strftime('%b %d, %Y')
    end_date = end_date.strftime('%b %d, %Y')

    diabetes_total = df_diabetes.shape[0] * 32
    TB_total = df_TB.shape[0] * 18
    HIV_total = df_HIV.shape[0] * 16
    report_content = f"""
    HTHA Data Validity Check Report ({report_date})
    Period in review: {start_date} - {end_date}

    Diabetes:
    {(
        f"Total expected questions = {diabetes_total}  [Number of rows ({df_diabetes.shape[0]}) × Number of compulsory questions (32)]\n"
        f"Missing compulsory/follow-up questions = {diabetes_total_missing_question}\n"
        f"Accuracy Rate = ((Total Expected - Total Issues) / Total Expected) * 100\n"
        f"= (({diabetes_total} - {diabetes_total_missing_question}) / {diabetes_total}) * 100\n"
        f"Data Accuracy: {((diabetes_total - diabetes_total_missing_question) / diabetes_total) * 100:.2f}%"
        f"{prepare_report_table(df_diabetes)}"
    ) if df_diabetes.shape[0] > 0 else "There is no data for this entry."}

    Tuberculosis:
    {(
        f"Total expected questions = {TB_total}  [Number of rows ({df_TB.shape[0]}) × Number of compulsory questions (18)]\n"
        f"Missing compulsory/follow-up questions = {TB_total_missing_question}\n"
        f"Accuracy Rate = ((Total Expected - Total Issues) / Total Expected) * 100\n"
        f"= (({TB_total} - {TB_total_missing_question}) / {TB_total}) * 100\n"
        f"Data Accuracy: {((TB_total - TB_total_missing_question) / TB_total) * 100:.2f}%"
        f"{prepare_report_table(df_TB)}"
    ) if df_TB.shape[0] > 0 else "There is no data for this entry."}

    HIV:
    {(
        f"Total expected questions = {HIV_total}  [Number of rows ({df_HIV.shape[0]}) × Number of compulsory questions (16)]\n"
        f"Missing compulsory/follow-up questions = {HIV_total_missing_question}\n"
        f"Accuracy Rate = ((Total Expected - Total Issues) / Total Expected) * 100\n"
        f"= (({HIV_total} - {HIV_total_missing_question}) / {HIV_total}) * 100\n"
        f"Data Accuracy: {((HIV_total - HIV_total_missing_question) / HIV_total) * 100:.2f}%"
        f"{prepare_report_table(df_HIV)}"
    ) if df_HIV.shape[0] > 0 else "There is no data for this entry."}
    """

    # Save report to a text file
    with open("HTHA_Data_Validity_Report.txt", "w") as file:
        file.write(report_content)

    # df_diabetes.to_csv('data.csv', index=False)
    print("report generated successfully")

    return

if __name__ == '__main__':
    generate_report()
    send_email(
        sender_password=os.getenv("SENDER_PASSWORD"),
        file_path="HTHA_Data_Validity_Report.txt"
    )
