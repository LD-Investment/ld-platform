import re
from datetime import datetime
from typing import List

import pytz
from django.db import models
from django.utils import timezone


class CoinnessNewsDataManager(models.Manager):
    def create(self, *args, **kwargs):
        """
        Should parse raw data scraped from web, validate and persist
        """
        date = kwargs.pop("date", None)  # e.g 23:002022년 2월 5일 토요일
        # bull_bear = kwargs.pop(
        #     "bull_bear", "Bull 0Bear 0"
        # )  # e.g Bull 268Bear 22\n공유하기업계동향

        kwargs["date"] = self._parse_date(date) if date else timezone.now()
        # bull_bear = self._parse_bull_bear(bull_bear)
        # kwargs["bull_count"] = bull_bear[0]
        # kwargs["bear_count"] = bull_bear[1]

        return super().create(**kwargs)

    @staticmethod
    def _parse_date(data: str) -> datetime:
        """
        Args:
            data: "23:002022년 2월 5일 토요일"

        Return:
            <datetime.datetime object>
        """
        UTC = pytz.timezone("UTC")
        KST = pytz.timezone("Asia/Seoul")

        date_in_kr = data[5:-4]  # now converted to 2022년 2월 5일
        obj = datetime.strptime(date_in_kr, "%Y년 %m월 %d일")
        now_utc = obj.replace(tzinfo=UTC)
        now_kst = now_utc.astimezone(KST)
        return now_kst

    @staticmethod
    def _parse_bull_bear(data: str) -> List[int]:
        """
        Args:
            data: "Bull 268Bear 22\n공유하기업계동향"

        Return:
            [0, 0]
        """
        result = re.findall(r"\d+", data)
        return [int(s) for s in result]
