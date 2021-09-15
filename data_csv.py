import csv

'''
Car_Data: class read model and owner csv file and return information in dictionary.
write model and owner csv file using database information.
'''

class Car_Data:
    def __init__(self, csv_name):
        self.csv_name = csv_name

    '''
    read_model_csv: Read model csv return infromation into dictonary.
    '''
    def read_model_csv(self):
        with open(self.csv_name, mode='r') as csv_file:
            # Read CSV file
            csv_reader = csv.DictReader(csv_file)
            line_count = 0
            model_data = []
            for row in csv_reader:
                if line_count == 0:
                    print(f'Column names are {", ".join(row)}')
                    line_count += 1
                model_data.append({
                    'model_name': row["model_name"],
                    "launch_date": row["launch_date"]
                })
                line_count += 1
            return model_data 


    '''
    read_owner_csv: Read owner csv return infromation into dictonary.
    '''
    def read_owner_csv(self):
        with open(self.csv_name, mode='r') as csv_file:
            # Read CSV file
            csv_reader = csv.DictReader(csv_file)
            line_count = 0
            owner_data = []
            for row in csv_reader:
                if line_count == 0:
                    print(f'Column names are {", ".join(row)}')
                    line_count += 1
                owner_data.append({
                    'owner_name': row["owner_name"],
                    "address": row["address"]
                })
                line_count += 1
            return owner_data

    '''
    write_model_csv: Write model csv from database information.
    '''
    def write_model_csv(self, model_data):
        with open(self.csv_name, mode='w') as model_file:
            model_writer = csv.writer(model_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            model_writer.writerow(['model_name', 'launch_date'])
            for model in model_data:
                model_writer.writerow([model['model_name'],model['launch_date']])

    '''
    write_owner_csv: Write owner csv from database information.
    '''
    def write_owner_csv(self, owner_data):
        with open(self.csv_name, mode='w') as owner_file:
            owner_writer = csv.writer(owner_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            owner_writer.writerow(['owner_name','address'])
            for owner in owner_data:
                owner_writer.writerow([owner['owner_name'],owner['address']])   