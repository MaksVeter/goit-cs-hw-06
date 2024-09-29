import asyncio
import multiprocessing
from http_server import run_http_server  # Імпортуємо вашу функцію HTTP сервера
# Імпортуємо вашу функцію сокет сервера
from socket_server import main as run_socket_server

if __name__ == '__main__':
    # Запускаємо HTTP сервер в окремому процесі
    http_process = multiprocessing.Process(target=run_http_server)
    http_process.start()

    # Запускаємо сокет сервер
    asyncio.run(run_socket_server())
