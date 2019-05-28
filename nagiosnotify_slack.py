#!/usr/bin/env python

# Copyright 2019 University of Southern California Information Sciences Institute All Rights Reserved.
#
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

from __future__ import print_function  # (at top of module)

import argparse
import requests
import json

from nagiosnotify import NagiosNotify


class SlackNotify(NagiosNotify):
    # The following variables become duplicated between nagiosnotify_slack.py and nagiosnotify_teams.py.  They also
    # cause the _get_args method in each to contain duplicate code.  This is intentional to allow both slack and teams
    # notifications at the same time.  Please set values appropriately:

    # To create a link to nagios xi
    _NAGIOS_SERVER = ""

    # Primary slack channel
    _PRIMARY_CHANNEL = "#alerts"

    # Secondary slack channel
    _SECONDARY_CHANNEL = None

    # Web Hook URL
    _WEB_HOOK_URL = "https://hooks.slack.com/services/PUT URL HERE"

    # List of Nagios service names to send to secondary slack channel
    # _LIST_SERVICEDISPLAYNAMES = ['Yum Updates', 'APT Updates']
    _LIST_SERVICEDISPLAYNAMES = []

    # List of Nagios service state names to send to secondary slack channel
    # _LIST_STATE = ['WARNING']
    _LIST_STATE = []

    # Message for services
    _SERVICE_MESSAGE = "STATUS: {0}   HOST: {1}   SERVICE: {2}    MESSAGE: {3}"

    # List of Nagios ENV variables for services messages
    _SERVICE_MESSAGE_LIST = ["NAGIOS_SERVICESTATE", "NAGIOS_HOSTNAME", "NAGIOS_SERVICEDISPLAYNAME",
                             "NAGIOS_SERVICEOUTPUT"]

    # Message for hosts
    _HOST_MESSAGE = "STATUS: {0}   HOST: {1}   MESSAGE: {2}"

    # List of Nagios ENV variables for host messages
    _HOST_MESSAGE_LIST = ["NAGIOS_HOSTSTATE", "NAGIOS_HOSTNAME", "NAGIOS_HOSTOUTPUT"]

    # Slack botname
    _SLACK_BOTNAME = "nagios"

    _icon = None

    _nagios_state = None

    def _get_args(self):
        parser = self._get_parser()

        parser.add_argument('-wh', '--webhook', required=False, action='store', help='WebHook URL')
        parser.add_argument('-b', '--bot', required=False, action='store', help='BOT name')
        parser.add_argument('-si', '--skipicon', required=False, action='store_false',
                            help='Skip having an icon at the start of the message')

        args = parser.parse_args()

        # replace default values with what was passed in
        if args.primary:
            self._PRIMARY_CHANNEL = args.primary

        if args.secondary:
            self._SECONDARY_CHANNEL = args.secondary

        if args.nagios:
            self._NAGIOS_SERVER = args.nagios

        if args.webhook:
            self._WEB_HOOK_URL = args.webhook

        if args.bot:
            self._SLACK_BOTNAME = args.bot

        if args.servicemessage:
            self._SERVICE_MESSAGE = args.servicemessage

        if args.servicemessagelist:
            self._SERVICE_MESSAGE_LIST = args.servicemessagelist

        if args.hostmessage:
            self._HOST_MESSAGE = args.hostmessage

        if args.hostmessagelist:
            self._HOST_MESSAGE_LIST = args.hostmessagelist

        if args.test:
            self._TEST = args.test

        # all clearing the list inside the script
        if args.clear:
            self._LIST_STATE = []
            self._LIST_SERVICEDISPLAYNAMES = []
        else:
            if args.primary or args.secondary:
                print("WARNING: you may need to --clear the state and service lists")

        if args.services:
            self._LIST_SERVICEDISPLAYNAMES = args.services

        if args.states:
            self._LIST_STATE = args.states

        return args

    # Create a link to Nagios
    def _get_link(self, host):
        text_message = " <https://{0}/nagiosxi/includes/components/xicore/status.php?host={1}|See Nagios>"
        return text_message.format(self._NAGIOS_SERVER, host)

    # Set the icon to display
    def _get_icon(self, state):
        if state == "CRITICAL":
            return ":x:  "
        elif state == "DOWN":
            return ":x:  "
        elif state == "WARNING":
            return ":warning:  "
        elif state == "OK":
            return ":white_check_mark:  "
        elif state == "UP":
            return ":white_check_mark:  "
        elif state == "UNKNOWN":
            return ":question:  "
        else:
            return ":white_medium_square:  "

    def _customization_call(self, state):
        self._icon = self._get_icon(state)
        self._nagios_state = state

    def _get_request_data(self):
        args = self._get_args()
        # Grab Nagios environment variables.  Use default values for command line testing
        nagios_servicestate = self._get_env('NAGIOS_SERVICESTATE')
        nagios_hostname = self._get_env('NAGIOS_HOSTNAME')
        nagios_hoststate = self._get_env('NAGIOS_HOSTSTATE')
        nagios_servicedisplayname = self._get_env('NAGIOS_SERVICEDISPLAYNAME')

        text_message = self._get_message(nagios_servicestate, nagios_hoststate, self._SERVICE_MESSAGE,
                                         self._SERVICE_MESSAGE_LIST, self._HOST_MESSAGE, self._HOST_MESSAGE_LIST)

        if args.skipicon:
            text_message = self._icon + text_message
        if args.skiplink:
            text_message = text_message + self._get_link(nagios_hostname)

        slack_channel = self._get_channel(args.channel, self._PRIMARY_CHANNEL, self._SECONDARY_CHANNEL,
                                          self._LIST_STATE, self._LIST_SERVICEDISPLAYNAMES, self._nagios_state,
                                          nagios_servicedisplayname)

        # Slack Web Hook app
        url = self._WEB_HOOK_URL

        json_data = {
            "channel": slack_channel,
            "username": self._SLACK_BOTNAME,
            "text": text_message
        }

        request_data = {
            "url" : url,
            "data" : {'payload' : json.dumps(json_data)}
        }

        return request_data

    def do_notify(self):
        request_data = self._get_request_data()

        res = requests.post(request_data['url'], data=request_data['data'])
        return res


def main():
    slack = SlackNotify()
    res = slack.do_notify()
    print(res)


if __name__ == "__main__":
    main()
