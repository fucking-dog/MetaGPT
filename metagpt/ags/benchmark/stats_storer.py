#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/9/13 12:29
@Author  : femto Zheng
@File    : utils from https://github.com/femto/minion
"""
import json
import os
from abc import ABC, abstractmethod
from typing import List

class StatsStorer(ABC):
    @abstractmethod
    async def update_stats(self, stats_data: dict):
        pass

    @abstractmethod
    async def get_stats(self, item_id: str):
        pass


class JsonStatsStorer(StatsStorer):
    def __init__(self, file_path: str):
        self.file_path = file_path

        # Load existing data
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as f:
                self.data = json.load(f)
        else:
            self.data = {}

    async def update_stats(self, stats_data: dict):

        stats_entry = {
            "item_id": stats_data['item_id'],
            "answer": str(stats_data['answer']),
            "raw_answer": stats_data['raw_answer'],
            "raw_correct_answer": stats_data['raw_correct_answer'],
            "correct_answer": stats_data['correct_answer'],
            "outcome": stats_data['outcome'],

        }

        # Update or add new entry
        if stats_data['item_id'] in self.data:
            self.data[stats_data['item_id']].append(stats_entry)
        else:
            self.data[stats_data['item_id']] = [stats_entry]

        # Write updated data back to file
        with open(self.file_path, 'w') as f:
            json.dump(self.data, f, indent=2)

    async def get_stats(self, item_id: str):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as f:
                data = json.load(f)
            return data.get(item_id, [])
        return []


class MultipleStatsStorer(StatsStorer):
    def __init__(self, storers: List[StatsStorer]):
        self.storers = storers

    async def update_stats(self, stats_data: dict):
        for storer in self.storers:
            await storer.update_stats(stats_data)

    async def get_stats(self, item_id: str):
        all_stats = []
        for storer in self.storers:
            return await storer.get_stats(item_id)
            all_stats.extend(stats)
        return all_stats