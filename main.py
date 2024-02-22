import os
import argparse
import asyncio
import logging
import time
from dotenv import load_dotenv
import gui


logger = logging.getLogger("asyncio_chat")


async def main(host, port_listen, port_write, hash):
    messages_queue = asyncio.Queue()
    sending_queue = asyncio.Queue()
    status_updates_queue = asyncio.Queue()

    await asyncio.gather(generate_msgs(messages_queue),
                        gui.draw(messages_queue, sending_queue, status_updates_queue))


if __name__ == '__main__':
    load_dotenv()
    logging.basicConfig(format="%(levelname)-3s %(message)s", level=logging.DEBUG)

    command_arguments = argparse.ArgumentParser(
        description="Скрипт подключения к подпольному чату с графическим интенрфейсом"
    )
    command_arguments.add_argument(
        "--host", help="Укажите хост чата", default=os.getenv("HOST")
    )
    command_arguments.add_argument(
        "--portlisten",
        help="Укажите порт просмотра чата",
        default=int(os.getenv("LISTEN_PORT")),
        type=int,
    )
    command_arguments.add_argument(
        "--portwrite",
        help="Укажите порт отправки в чат",
        default=int(os.getenv("WRITE_PORT")),
        type=int,
    )
    command_arguments.add_argument(
        "--hash", help="Укажите токен чата", default=os.getenv("ACCOUNT_HASH")
    )

    args = command_arguments.parse_args()
    while True:
        try:
            asyncio.run(main(args.host, args.portlisten, args.portwrite, args.hash))
        except OSError as error:
            logger.error(f"Возникла ошибка: {error}")
            logger.error("Сеанс завершен")
            break
