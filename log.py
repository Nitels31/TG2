import functools
import logging
from pathlib import Path
import sys
import time
from typing import Any
from loguru import logger

# ==============================================================================
# 1. АВТОМАТИЧНЕ СТВОРЕННЯ ПАПКИ ТА ФАЙЛІВ ЛОГІВ
# ==============================================================================
# Створюємо папку log (працює коректно і на Windows, і на Linux)
LOG_DIR = Path("log")
LOG_DIR.mkdir(parents=True, exist_ok=True)

WARNING_LOG_PATH = LOG_DIR / "warning.log"
USERS_LOG_PATH = LOG_DIR / "users.log"

# Створюємо самі файли, якщо вони відсутні
WARNING_LOG_PATH.touch(exist_ok=True)
USERS_LOG_PATH.touch(exist_ok=True)

# ==============================================================================
# 2. НАЛАШТУВАННЯ LOGURU (ЧАС, РОТАЦІЯ 50 MB, UTF-8)
# ==============================================================================
logger.remove()

# Ваш формат: Секунда:Година:День:Рік
TIME_FORMAT = "{time:ss:HH:DD:YYYY}"

FMT_WARNING = (
    f"{TIME_FORMAT} | <level>{{level: <8}}</level> | "
    f"{{name}}:{{function}}:{{line}} - {{message}}"
)
FMT_USERS = f"{TIME_FORMAT} | {{message}}"

# Консоль
logger.add(sys.stderr, format=FMT_WARNING, level="INFO", enqueue=True)

# 1. log/warning.log — ТІЛЬКИ WARNING ТА ПОМИЛКИ (до 50 MB)
logger.add(
    str(WARNING_LOG_PATH),
    format=FMT_WARNING,
    level="WARNING",
    rotation="50 MB",
    encoding="utf-8",
    enqueue=True,
    backtrace=True,
    diagnose=False,
)

# 2. log/users.log — ПОВІДОМЛЕННЯ КОРИСТУВАЧА, БОТА ТА ШІ (до 50 MB)
chat_logger = logger.bind(is_chat=True)
logger.add(
    str(USERS_LOG_PATH),
    format=FMT_USERS,
    level="INFO",
    rotation="50 MB",
    encoding="utf-8",
    enqueue=True,
    filter=lambda record: record["extra"].get("is_chat") is True,
)

# ==============================================================================
# 3. ПЕРЕХОПЛЕННЯ СИСТЕМНИХ ПОМИЛОК ТА ПОМИЛОК TELEBOT -> warning.log
# ==============================================================================


class InterceptHandler(logging.Handler):
    """Ловить помилки telebot, urllib3 та стандартного logging і пише в warning.log"""

    def emit(self, record: logging.LogRecord) -> None:
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)


def _handle_unhandled_crash(exc_type, exc_value, exc_traceback):
    """Ловить падіння скрипта і пише в warning.log"""
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logger.opt(exception=(exc_type, exc_value, exc_traceback)).critical(
        "Фатальне падіння програми:"
    )


sys.excepthook = _handle_unhandled_crash

# ==============================================================================
# 4. ПЕРЕХОПЛЕННЯ TELEBOT -> users.log
# ==============================================================================
try:
    import telebot
    from telebot import apihelper

    # Вхідні повідомлення від користувача
    _orig_process_new_messages = telebot.TeleBot.process_new_messages

    @functools.wraps(_orig_process_new_messages)
    def _intercept_incoming(self, new_messages):
        for msg in new_messages:
            try:
                user = getattr(msg, "from_user", None)
                user_tag = (
                    f"@{user.username}"
                    if (user and user.username)
                    else f"ID:{getattr(user, 'id', 'None')}"
                )
                chat_id = getattr(getattr(msg, "chat", None), "id", "Unknown")

                text = (
                    getattr(msg, "text", None)
                    or getattr(msg, "caption", None)
                    or f"<{getattr(msg, 'content_type', 'media')}>"
                )

                chat_logger.info(
                    f"[КОРИСТУВАЧ -> БОТ] [Чат:{chat_id} | Від:{user_tag}]: {text}"
                )
            except Exception as e:
                logger.warning(f"Помилка читання повідомлення: {e}")
        return _orig_process_new_messages(self, new_messages)

    telebot.TeleBot.process_new_messages = _intercept_incoming

    # Вихідні відповіді бота (send_message / reply_to)
    _orig_send_message = apihelper.send_message

    @functools.wraps(_orig_send_message)
    def _intercept_outgoing(token, chat_id, text, *args, **kwargs):
        chat_logger.info(f"[БОТ -> КОРИСТУВАЧ] [Чат:{chat_id}]: {text}")
        return _orig_send_message(token, chat_id, text, *args, **kwargs)

    apihelper.send_message = _intercept_outgoing

except ImportError:
    pass

# ==============================================================================
# 5. ПЕРЕХОПЛЕННЯ GEMINI ШІ -> users.log (та помилок ШІ -> warning.log)
# ==============================================================================


def _extract_prompt(args: tuple, kwargs: dict) -> str:
    content = kwargs.get("contents")
    if content is None:
        if len(args) > 1:
            content = args[1]
        elif len(args) > 0:
            content = args[0]
    return (
        str(content)
        if not isinstance(content, (list, tuple))
        else " ".join(str(i) for i in content)
    )


def _extract_response_text(res: Any) -> str:
    try:
        if hasattr(res, "text") and res.text:
            return res.text
        if hasattr(res, "candidates") and res.candidates:
            parts = res.candidates[0].content.parts
            return "".join(getattr(p, "text", "") for p in parts)
    except Exception:
        return "<Відповідь заблокована фільтром безпеки або порожня>"
    return str(res)


# Для бібліотеки google-genai
try:
    from google.genai.models import Models

    _orig_genai = Models.generate_content

    @functools.wraps(_orig_genai)
    def _intercept_genai(self, *args, **kwargs):
        prompt = _extract_prompt(args, kwargs)
        chat_logger.info(f"[ШІ ЗАПИТ]: {prompt}")
        t0 = time.perf_counter()
        try:
            res = _orig_genai(self, *args, **kwargs)
            chat_logger.info(
                f"[ШІ ВІДПОВІДЬ ({time.perf_counter() - t0:.2f}s)]: {_extract_response_text(res)}"
            )
            return res
        except Exception as err:
            logger.error(f"[ШІ ПОМИЛКА] Промпт: {prompt} | Помилка: {err}")
            raise

    Models.generate_content = _intercept_genai
except (ImportError, AttributeError):
    pass

# Для бібліотеки google-generativeai
try:
    import google.generativeai as legacy_genai

    _orig_legacy = legacy_genai.GenerativeModel.generate_content

    @functools.wraps(_orig_legacy)
    def _intercept_legacy(self, *args, **kwargs):
        prompt = _extract_prompt(args, kwargs)
        chat_logger.info(f"[ШІ ЗАПИТ]: {prompt}")
        t0 = time.perf_counter()
        try:
            res = _orig_legacy(self, *args, **kwargs)
            chat_logger.info(
                f"[ШІ ВІДПОВІДЬ ({time.perf_counter() - t0:.2f}s)]: {_extract_response_text(res)}"
            )
            return res
        except Exception as err:
            logger.error(f"[ШІ ПОМИЛКА] Промпт: {prompt} | Помилка: {err}")
            raise

    legacy_genai.GenerativeModel.generate_content = _intercept_legacy
except (ImportError, AttributeError):
    pass