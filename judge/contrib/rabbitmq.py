import json
import logging
from datetime import datetime
from typing import Any, Callable, Dict
from uuid import UUID

import aio_pika
from aio_pika import Message, connect_robust
from aio_pika.abc import AbstractIncomingMessage

from judge.config import settings

logger = logging.getLogger(__name__)


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return str(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


class RabbitMQ:
    _instance = None
    _connection = None
    _channel = None
    _queue = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RabbitMQ, cls).__new__(cls)
        return cls._instance

    async def connect(self) -> None:
        if not self._connection:
            self._connection = await connect_robust(settings.RABBITMQ_URL)
            self._channel = await self._connection.channel()
            self._queue = await self._channel.declare_queue(
                "submissions",
                durable=True
            )

    async def close(self) -> None:
        if self._connection:
            await self._connection.close()
            self._connection = None
            self._channel = None
            self._queue = None

    async def publish(self, message: Dict[str, Any]) -> None:
        if not self._connection:
            await self.connect()

        logger.info(f"Publishing message: {message}")

        try:
            message_body = json.dumps(message, cls=UUIDEncoder).encode()
            logger.info(f"Serialized message: {message_body.decode()}")

            await self._channel.default_exchange.publish(
                Message(
                    body=message_body,
                    delivery_mode=aio_pika.DeliveryMode.PERSISTENT
                ),
                routing_key="submissions"
            )
            logger.info("Message published successfully")
        except Exception as e:
            logger.error(f"Error publishing message: {str(e)}")
            raise

    async def consume(self, callback: Callable[[Dict[str, Any]], Any]) -> None:
        if not self._connection:
            await self.connect()

        async def process_message(message: AbstractIncomingMessage):
            async with message.process():
                try:
                    body = json.loads(message.body.decode())
                    logger.info(f"Received message from queue: {body}")
                    await callback(body)
                except Exception as e:
                    logger.error(f"Error processing message: {str(e)}")
                    logger.error(f"Message body: {message.body.decode()}")

        await self._queue.consume(process_message)
