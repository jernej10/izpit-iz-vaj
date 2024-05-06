import csv

def read_data(filename):
    data = []
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            data.append(row)
    return data

def validate(reference_data, current_data):
    reference_header = reference_data[0]
    current_header = current_data[0]

    if len(reference_header) != len(current_header):
        print("Število stolpcev se ne ujema!")
        return False

    if reference_header != current_header:
        print("Imena stolpcev niso ista!")
        return False

    for i in range(1, len(reference_data)):
        reference_row = reference_data[i]
        current_row = current_data[i]

        for j in range(len(reference_row)):
            reference_value = reference_row[j]
            current_value = current_row[j]

            if type(reference_value) != type(current_value):
                print(f"Tip podatkov ni enak => {reference_header[j]}!")
                return False

    print("Validacija uspešna!")
    return True

def main():
    reference_data = read_data('../../data/processed/reference_dataset.csv')
    current_data = read_data('../../data/processed/current_data.csv')
    validate(reference_data, current_data)

if __name__ == "__main__":
    main()
