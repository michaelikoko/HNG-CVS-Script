import json
import hashlib
import csv

def calculate_sha256(filename):
    """This function calculates and returns the sha256 code in hexadecimal of the given json file"""
    sha256_hash = hashlib.sha256()
    with open(filename,"rb") as f:
        for byte_block in iter(lambda: f.read(4096),b""):
            sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()

def create_new_csv_file(filename, fieldnames):
    """This function creates a csv file and inputs header row, based on the parameters passed"""

    with open(filename, mode="w") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

def write_to_csv_file(filename, data):
    """This function appends data passed on function call to a csv file specified in the parameters."""

    with open(filename, mode="a") as csv_file:
        writer = csv.writer(csv_file,  delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(data)

def main():
    """This function reads a csv file, creates a json file for each entry, and outputs another csv file with the sha256 of each entry's json file added to it"""

    FILENAME = "HNGi9-CSV-FILE.csv"

    with open(FILENAME) as csv_file:
        print("Processing csv file...")
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        json_format = {"format": "CHIP-0007"}

        for row in csv_reader:

            if line_count == 0:
                column_names = [*row]
                fieldnames = [*column_names, "sha256"]
                csv_filename = "HNGi9-CSV-FILE.output.csv"
                create_new_csv_file(csv_filename, fieldnames)
                line_count += 1

            else:
                if not row[0].isnumeric():
                    continue

                filename = row[1]
                entry_dict = json_format.copy()

                for j in range(len(column_names)):
                    entry_dict[f"{column_names[j]}"] = row[j]
                json_object = json.dumps(entry_dict, indent=4)

                try:
                    json_filename = f"./{filename}.json"
                    with open(json_filename, "w") as outfile:
                        outfile.write(json_object)

                    sha256 = calculate_sha256(json_filename)

                    data = [*row, sha256]
                    write_to_csv_file(csv_filename, data)
                except Exception as error:
                    print("Error")
                    print(error)

                line_count += 1
        print(f'Processed {line_count} lines.')

if __name__ == "__main__":
    main()

