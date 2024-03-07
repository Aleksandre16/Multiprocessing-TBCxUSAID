"""წინა დავალება შეასრულეთ შემდეგი კლასების გამოყენებით
ProcessPoolExecutor, ThreadPoolExecutor
შექმენით 5 პროცესი და თითოეულ პროცესში 20 ნაკადი. ფაილში შეინახეთ 100 პროდუქტის ინფორმაცია."""
import os
import json
import concurrent.futures
import time
import requests

folder_path = "json_files"
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

filename = os.path.join(folder_path, "all_products.json")

api_base_url = "https://dummyjson.com/products/"
api_urls = [f"{api_base_url}{i}" for i in range(1, 101)]
process_output = []

for i in range(0, len(api_urls), 20):
    process_output.append(api_urls[i:i + 20])


def request_url(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        with open(filename, 'a') as file:
            json.dump(data, file)
            file.write("\n")
    else:
        print(f"Wrong API URL: {url}")


def thread_process(x):
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as thread_executor:
        for url in x:
            thread_executor.submit(request_url, url, filename)


def main():
    start = time.perf_counter()
    with concurrent.futures.ProcessPoolExecutor(max_workers=5) as process_executor:
        process_executor.submit(thread_process, api_urls)

    print("Successfully added!")
    end = time.perf_counter()
    print(end - start)


if __name__ == "__main__":
    main()
