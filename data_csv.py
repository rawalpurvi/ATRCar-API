import csv


class CAR_DATA:
    def __init__(self, csv_name):
        self.csv_name = csv_name


    def read_model_csv(self, csv_name):
        with open(csv_name, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            line_count = 0
            model_data = []
            for row in csv_reader:
                if line_count == 0:
                    print(f'Column names are {", ".join(row)}')
                    line_count += 1
                model_data.append({
                    'model_name': row["modle_name"],
                    "launch_date": row["launch_date"]
                })
                line_count += 1
            return model_data
    

    def read_owner_csv(self, csv_name):
        with open(csv_name, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            line_count = 0
            owner_data = []
            for row in csv_reader:
                if line_count == 0:
                    print(f'Column names are {", ".join(row)}')
                    line_count += 1
                owner_data.append({
                    'owner_name': row["modle_name"],
                    "purchase_date": row["purchase_date"]
                })
                line_count += 1
            return owner_data

    def write_model_csv(self, csv_name, model_data):
        with open(csv_name, mode='w') as model_file:
            model_writer = csv.writer(model_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for model in model_data:
                model_writer.writerow([model['model_name'],model['launch_date']])

    def write_owner_csv(self, csv_name, owner_data):
        with open(csv_name, mode='w') as owner_file:
            owner_writer = csv.writer(owner_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for owner in owner_data:
                owner_writer.writerow([owner['owner_name'],owner['purchase_date']])
