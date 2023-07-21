import requests
import csv
import argparse
from datetime import datetime

def get_vk_friends(token, user_id):
    url = f"https://api.vk.com/method/friends.get"
    params = {
        "access_token": token,
        "user_id": user_id,
        "v": "5.131",
        "fields": "first_name,last_name,country,city,bdate",
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "response" in data:
        return data["response"]["items"]
    else:
        print("Ошибка при получении списка друзей:")
        print(data)
        return None

def generate_report(data, output_file):
    with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["Имя", "Фамилия", "Страна", "Город", "Дата рождения"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for friend in data:
            writer.writerow({
                "Имя": friend.get("first_name", ""),
                "Фамилия": friend.get("last_name", ""),
                "Страна": friend.get("country", {}).get("title", ""),
                "Город": friend.get("city", {}).get("title", ""),
                "Дата рождения": friend.get("bdate", ""),
            })

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Получение списка друзей из ВКонтакте и генерация отчета в формате CSV")
    parser.add_argument("token", type=str, help="Авторизационный токен")
    parser.add_argument("user_id", type=int, help="ID пользователя для генерации отчета")
    parser.add_argument("--output_file", type=str, default="report.csv",
                        help="Путь к выходному файлу. По умолчанию — файл с именем report.csv в текущей директории")
    args = parser.parse_args()

    friends_data = get_vk_friends(args.token, args.user_id)
    if friends_data:
        generate_report(friends_data, args.output_file)
        print("Отчет успешно сгенерирован.")
