#!/usr/bin/env python
# coding: utf-8

# Copyright 2016, Beryl8 Plus, Co,Ltd.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging


class Log:
    @staticmethod
    def info(message):
        if __debug__:
            Log.debug(message.encode('utf8'))
        else:
            logging.info(message)

    @staticmethod
    def warn(message):
        if __debug__:
            Log.debug(message.encode('utf8'))
        else:
            logging.warn(message)

    @staticmethod
    def error(message):
        if __debug__:
            Log.debug(message.encode('utf8'))
        else:
            logging.error(message)

    @staticmethod
    def fatal(message):
        if __debug__:
            Log.debug(message.encode('utf8'))
        else:
            logging.fatal(message)

    @staticmethod
    def debug(message):
        print "[DEBUG] " + message
        logging.debug(message)


