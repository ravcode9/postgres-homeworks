import os
import psycopg2 as ps
import csv


def load_data_from_csv(file_name, table_name):
    file_path = os.path.join(os.path.dirname(__file__), 'north_data', file_name)

    conn = None
    cur = None

    try:
        conn = ps.connect(host='localhost', database='north', user='postgres', password='12345')
        cur = conn.cursor()

        if os.path.isfile(file_path):
            with open(file_path, 'r', encoding='UTF-8') as file:
                csv_reader = csv.reader(file)
                next(csv_reader)

                for row in csv_reader:
                    cur.execute(
                        f"INSERT INTO {table_name} VALUES ({','.join(['%s'] * len(row))})", row
                    )

            conn.commit()
            print(f"Данные успешно загружены в таблицу {table_name} из файла {file_path}.")
        else:
            print(f"Файл '{file_path}' не существует.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


load_data_from_csv('employees_data.csv', 'employees')
load_data_from_csv('customers_data.csv', 'customers')
load_data_from_csv('orders_data.csv', 'orders')

