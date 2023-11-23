import os
import pandas as pd

def show_sentence(sent):
    print("--------------------------------------------------\n") 
    print(sent)
    print("--------------------------------------------------")

def get_clause_annotation(df):
    """
    Gets user choice
    """
    annotated_df = df.loc[:,["sents"]]
    if "has_clause" in df.columns:
        start_row = df.loc[df['has_clause'] == -1].index[0]
        annotated_df["has_clause"] = df["has_clause"]
        annotated_df["type"] = df["type"]
    else:
        start_row = 0
        annotated_df["has_clause"] = -1
        annotated_df["type"] = ""
    for index, row in annotated_df.iloc[start_row:].iterrows():

        # Get the clausal embedding annotation
        print("==================================")
        print("Embedded Clause")
        print("==================================\n")
        print("Does the following sentence have an embedded clause?\n")
        show_sentence(row.sents)
        while True:
            user_input = input("Answer ('y' or 'n' or 'u'): ")
            if user_input == "y":
                row["has_clause"] = 1
                break
            if user_input == "n":
                row["has_clause"] = 0
                break
            if user_input == 'u':
                row["has_clause"] = 2
                break
            if user_input == 'q':
                return annotated_df
            else:
                print("Unrecognized input. Please type one of the desired keys.")
                print("Does the following sentence have an embedded clause?\n")
                print(row.sents)

        # Get the clause type annotation
        if row["has_clause"] != 1:
            annotated_df.loc[index] = row
            continue
        print("==================================")
        print("Clause type")
        print("==================================\n")
        print("What is the clause type of the embedded clause in the follwing sentence?\n")
        show_sentence(row.sents)
        while True:
            user_input = input("Answer ('d','c','p','a' or 'u'): ")
            if user_input == "d":
                row["type"] = "declarative"
                break
            if user_input == "c":
                row["type"] = "constituent"
                break
            if user_input == "p":
                row["type"] = "polar"
                break
            if user_input == "a":
                row["type"] = "alternative"
                break
            if user_input == "u":
                row["type"] = "unknown"
                break
            if user_input == "q":
                return annotated_df
            else:
                print("Unrecognized input. Please type one of the desired keys.")
                print("What is the clause type of the  embedded clause?\n")
                show_sentence(row.sents)

        annotated_df.loc[index] = row

    return annotated_df

def main():
    # This imports all of the pre-filtered sentences from the dataset
    file_path = "annotated_data.csv"
    if os.path.exists(file_path):
        clauses_all = pd.read_csv("annotated_data.csv")
    else:
        clauses_all = pd.read_csv("sentences_filtered_1-1000.csv")


    # Do some annotations
    annotated_df = get_clause_annotation(clauses_all)
    # Save the file
    annotated_df.to_csv("annotated_data.csv")

main()
