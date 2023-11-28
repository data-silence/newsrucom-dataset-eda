"""
This is where the libraries are imported, and the supporting tools for working with the news database are defined
Здесь импортируются библиотеки, и определяются вспомогательные инструменты для работы с базой данных новостей
"""

# Common libs:
import os
import sys
import datetime as dt
import re
import logging
from collections import Counter
from numpy.linalg import norm

# ML libs:
import numpy as np
import pandas as pd
from sklearn.cluster import AgglomerativeClustering
from navec import Navec

# Other libs
import asyncio
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Graphs
import seaborn as sns
import matplotlib.pyplot as plt
sns.set(style="darkgrid")

# Aiogram
# from aiogram import Router, F
# from aiogram.fsm.context import FSMContext
# from aiogram.fsm.state import StatesGroup, State
# from aiogram.types import FSInputFile, CallbackQuery, Message, ReplyKeyboardRemove
# from aiogram.filters import CommandStart
# from aiogram.filters.callback_data import CallbackData
# from aiogram_calendar import DialogCalendar, DialogCalendarCallback
#
# from aiogram import Bot, Dispatcher
# from aiogram.fsm.storage.memory import MemoryStorage


load_dotenv()

DB_TM = os.getenv("DB_TM")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")

time_machine = create_engine(
    f'postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_TM}', pool_pre_ping=True)

TOKEN = os.getenv("BOT_TOKEN")

navec = Navec.load('models//navec.tar')


class DataBaseMixin:
    """
    Contains a set of universal functions for working with databases
    Содержит набор универсальных функций для работы с базами данных
    """

    @staticmethod
    def get(query: str, engine) -> list[dict]:
        """
        db -> data as a list of dicts

        Accepts a query in the database and returns the result of its execution
        Принимает запрос в БД и возвращает результат его исполнения
        """
        with engine.begin() as conn:
            query_text = text(query)
            result_set = conn.execute(query_text)
            results_as_dict = result_set.mappings().all()
            return results_as_dict
