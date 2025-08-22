import requests
import csv
from datetime import date

today = date.today()
formatted_date = today.strftime("%Y-%m-%d")  # e.g., "2025-08-18"


# Specify the output CSV file name
filename = f"customer_data_{formatted_date}.csv"

COOKIE_HEADER = "JSESSIONID=9EB1EB51FB74CD179E337EEAFDDF1E43; XSRF-TOKEN=EN77-ZS88-UVK9-HH1S-6GYB-MWMT-CMNX-4DRL"
headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9",
        "Cookie": COOKIE_HEADER,
        "Priority": "u=1, i",
        "Sec-Ch-Ua": '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "Windows",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
        "Content-Type": "application/json"
    }


# Gets value from object if key exists, None otherwise
def get_value(obj, key):
    if key in obj:
        return obj[key]
    else:
        return None


def retrieve_customer_list(offset, page_size):
    # Session object keeps cookies between requests
    # session = requests.Session()

    data_url = f"https://marketing.foodtecsolutions.com/ws/loyalty/report/customerPerformance?merchant=Gregorio%27s%20Trattoria&paging-offset={offset}&paging-limit={page_size}"

    data_response = requests.get(data_url, headers=headers)

    if data_response.status_code == 200:
        data = data_response.json()
        print(f'Total Count: {data["totalCount"]}')
        return data['result']
    else:
        raise Exception(f"Data fetch failed: {data_response.text}")


def retrieve_customer_details(customer_id):
    data_url = f"https://marketing.foodtecsolutions.com/ws/common/customer/findById?merchant=Gregorio%27s%20Trattoria&customerId={customer_id}"

    data_response = requests.get(data_url, headers=headers)

    if data_response.status_code == 200:
        data = data_response.json()
        return data
    else:
        print(f"Data fetch failed: {data_response.text}")


def retrieve_customer_points(customer_id):
    data_url = f"https://marketing.foodtecsolutions.com/ws/common/customer/{customer_id}/loyalty/pointsHistory?merchant=Gregorio%27s%20Trattoria&customerId={customer_id}&paging-offset=0&paging-limit=1"

    data_response = requests.get(data_url, headers=headers)

    if data_response.status_code == 200:
        data = data_response.json()
        if len(data['result']) > 0:
            return data['result'][0]['newTotal']
        else:
            print(f"Customer {customer_id} has no points rows")
    else:
        print(f"Data fetch failed: {data_response.text}")


def retrieve_customer_coupons(customer_id):
    data_url = f"https://marketing.foodtecsolutions.com/ws/common/customer/{customer_id}/loyalty/coupons?merchant=Gregorio%27s%20Trattoria&customerId={customer_id}&paging-offset=0&paging-limit=25"

    data_response = requests.get(data_url, headers=headers)

    if data_response.status_code == 200:
        data = data_response.json()
        return data['result']
    else:
        print(f"Data fetch failed: {data_response.text}")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    output_data = [["Customer ID", "Name", "Email", "Phone Number", "Birthday", "Points", "Coupon List"]]
    page_size_val = 1000
    for i in range(0, 15000, page_size_val):
        customer_list = retrieve_customer_list(i, page_size_val)
        for customer in customer_list:
            customer_id = customer['Customer']['value']
            customer_details = retrieve_customer_details(customer_id)
            customer_points = retrieve_customer_points(customer_id)
            customer_coupon_data_list = retrieve_customer_coupons(customer_id)
            if customer_details is None:
                output_data.append([customer_id, '', '', '', '', customer_points])
            else:
                output_data.append([
                    customer_id,
                    get_value(customer_details, 'name'),
                    get_value(customer_details, 'email'),
                    get_value(customer_details, 'phone'),
                    get_value(customer_details, 'birthday'),
                    customer_points,
                    customer_coupon_data_list
                ])
            print(f"{customer_id}")

    # Open the file in write mode and create a CSV writer object
    with open(filename, 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Write the data rows
        writer.writerows(output_data)

    print(f"Data successfully written to {filename}")
