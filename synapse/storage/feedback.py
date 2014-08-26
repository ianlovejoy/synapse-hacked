# -*- coding: utf-8 -*-
# Copyright 2014 matrix.org
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from twisted.internet import defer

from ._base import SQLBaseStore, Table
from synapse.api.events.room import FeedbackEvent

import collections
import json


class FeedbackStore(SQLBaseStore):

    def _store_feedback_txn(self, txn, event):
        self._simple_insert_txn(txn, "feedback", {
            "event_id": event.event_id,
            "feedback_type": event.feedback_type,
            "room_id": event.room_id,
            "target_event_id": event.target_event,
            "sender": event.user_id,
        })

    @defer.inlineCallbacks
    def get_feedback_for_event(self, event_id):
        sql = (
            "SELECT events.* FROM events INNER JOIN feedback "
            "ON events.event_id = feedback.event_id "
            "WHERE feedback.target_event_id = ? "
        )

        rows = yield self._execute_and_decode(sql, event_id)

        defer.returnValue(
            [
                self._parse_event_from_row(r)
                for r in rows
            ]
        )
