import pandas as pd

def merge_dataframes(excel_file, csv_file):
    excel_data = pd.read_excel(excel_file, index_col=0)
    csv_data = pd.read_csv(csv_file, index_col=0)
    merged_data = pd.concat([excel_data, csv_data], axis=1)
    return merged_data

def main():
    merged_data = merge_dataframes('../../data/raw/students.xlsx', '../../data/raw/students_scores.csv')
    merged_data['AVG_subject'] = (merged_data['STEM_subjects'] + merged_data['H_subjects']) / 2
    merged_data.to_csv('../../data/processed/current_data.csv')

if __name__ == "__main__":
    main()
