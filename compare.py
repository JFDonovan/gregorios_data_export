import csv


OLD_CUSTOMER_DATA_FILE_NAME = 'test_customer_data_2025-08-24_105153.csv'
NEW_CUSTOMER_DATA_FILE_NAME = 'test_customer_data_2025-08-24_121255.csv'
OUTPUT_FILE_NAME = f"{OLD_CUSTOMER_DATA_FILE_NAME} v {NEW_CUSTOMER_DATA_FILE_NAME}"


class Customer:
    def __init__(self, csv_row):
        self.id = csv_row[0]
        self.name = csv_row[1]
        self.email = csv_row[2]
        self.phone_number = csv_row[3]
        self.birthday = csv_row[4]
        self.points = csv_row[5]
        self.coupon_list = csv_row[6]

    def make_row(self):
        return [self.id, self.name, self.email, self.phone_number, self.birthday, self.points, self.coupon_list]

    def make_discrepancy_row(self, old_customer):
        return_row = [self.id, '', '', '', '']
        # todo
        if self.points != old_customer.points:
            return_row.append(int(self.points) - int(old_customer.points))
        if str(self.coupon_list) != str(old_customer.coupon_list):
            return_row.append("HERE") # TODO
        return return_row

    def __eq__(self, other):
        return (self.id == other.id and
                    self.name == other.name and
                    self.email == other.email and
                    self.phone_number == other.phone_number and
                    self.birthday == other.birthday and
                    str(self.coupon_list) == str(other.coupon_list)
                )


if __name__ == '__main__':
    old_customer_dict = {}
    discrepancy_list = []

    with (open(OLD_CUSTOMER_DATA_FILE_NAME, 'r', encoding='utf-8', newline='') as old_customer_data_file,
          open(NEW_CUSTOMER_DATA_FILE_NAME, 'r', encoding='utf-8', newline='') as new_customer_data_file):

        old_customer_data_list = csv.reader(old_customer_data_file)

        for row in old_customer_data_list:
            customer_id = row[0]
            old_customer_dict[customer_id] = Customer(row)

        new_customer_data_list = csv.reader(new_customer_data_file.readlines())

        for row in new_customer_data_list:
            customer = Customer(row)
            try:
                old_customer = old_customer_dict[customer.id]
            except KeyError:
                discrepancy_list.append(customer.make_row())
            if not customer == old_customer:
                discrepancy_list.append(customer.make_discrepancy_row(old_customer))


        print(discrepancy_list)

        # Open the file in write mode and create a CSV writer object
        with open(OUTPUT_FILE_NAME, 'w', encoding='utf-8', newline='') as csvfile:
            writer = csv.writer(csvfile)

            # Write the data rows
            writer.writerows(discrepancy_list)

        print(f"Data successfully written to {OUTPUT_FILE_NAME}")




