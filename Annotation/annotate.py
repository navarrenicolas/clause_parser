import pandas as pd

def get_clause_annotation(df):
    """
    Gets user choice
    """
    annotated_df = df.copy()
    annotated_df["has_clause"] = None
    annotated_df["type"] = ""
    for index, row in df.iterrows():

        # Get the clausal embedding annotation
        print("Does the following sentence have an embedded clause?\n")
        print(row.sents)
        while True:
            user_input = input("Answer ('y' or 'n' or 'u'): ")
            if user_input == "y":
                row["has_clause"] = 1
                break
            if user_input == "n":
                row["has_clause"] = 0
                break
            if user_input == 'u':
                row["has_clause"] = -1
            else:
                print("Please type either 'y' or 'n' or 'u'.")
                print("Does the following sentence have an embedded clause?\n")
                print(row.sents)

        # Get the clause type annotation
        if row["has_clause"] != 1:
            continue
        print("What is the clause type of the  embedded clause?\n")
        print(row.sents)
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
            else:
                print("Please type one of the desired keys.")
                print("Does the following sentence have an embedded clause?\n")
                print(row.sents)

        print(row)
        annotated_df.loc[index] = row

    return annotated_df

def main():
    # This imports all of the pre-filtered sentences from the dataset
    #TODO: Check if there is an annotated dataframe already
    clauses_all = pd.read_csv("sentences_filtered_1-1000.csv")

    annotated_df = get_clause_annotation(clauses_all.loc[0:3])

    annotated_df.to_csv("annotated_data.csv")

main()
