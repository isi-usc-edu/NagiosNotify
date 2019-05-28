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


class TeamsNotify(NagiosNotify):
    # The following variables become duplicated between nagiosnotify_slack.py and nagiosnotify_teams.py.  They also
    # cause the _get_args method in each to contain duplicate code.  This is intentional to allow both slack and teams
    # notifications at the same time.  Please set values appropriately:

    # To create a link to nagios xi
    _NAGIOS_SERVER = ""

    # Primary slack channel
    _PRIMARY_CHANNEL = "https://outlook.office.com/webhook/PUT WEBHOOK URL HERE"

    # Secondary slack channel
    _SECONDARY_CHANNEL = None

    # List of Nagios service names to send to secondary slack channel
    # _LIST_SERVICEDISPLAYNAMES = ['Yum Updates', 'APT Updates']
    _LIST_SERVICEDISPLAYNAMES = []

    # List of Nagios service state names to send to secondary slack channel
    # _LIST_STATE = ['WARNING']
    _LIST_STATE = []

    # Message for services
    _SERVICE_MESSAGE = "**STATUS:** {0}   **HOST:** {1}   **SERVICE:** {2}    **MESSAGE:** {3}"
    # _SERVICE_MESSAGE = "STATUS: {0}   HOST: {1}   SERVICE: {2}    MESSAGE: {3}"

    # List of Nagios ENV variables for services messages
    _SERVICE_MESSAGE_LIST = ["NAGIOS_SERVICESTATE", "NAGIOS_HOSTNAME", "NAGIOS_SERVICEDISPLAYNAME",
                             "NAGIOS_SERVICEOUTPUT"]

    # Message for hosts
    _HOST_MESSAGE = "**STATUS:** {0}   **HOST:** {1}   **MESSAGE:** {2}"

    # List of Nagios ENV variables for host messages
    _HOST_MESSAGE_LIST = ["NAGIOS_HOSTSTATE", "NAGIOS_HOSTNAME", "NAGIOS_HOSTOUTPUT"]

    _color = None

    _nagios_state = None

    def _get_args(self):
        parser = self._get_parser()

        args = parser.parse_args()

        # replace default values with what was passed in
        if args.primary:
            self._PRIMARY_CHANNEL = args.primary

        if args.secondary:
            self._SECONDARY_CHANNEL = args.secondary

        if args.nagios:
            self._NAGIOS_SERVER = args.nagios

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
        text_message = "[See Nagios](https://{0}/nagiosxi/includes/components/xicore/status.php?host={1}) "
        return text_message.format(self._NAGIOS_SERVER, host)

    # Set the icon to display
    def _get_color(self, state):
        if state == "CRITICAL":
            return "ff0000"
        elif state == "DOWN":
            return "ff0000"
        elif state == "WARNING":
            return "ffaa1d"
        elif state == "OK":
            return "00ff00"
        elif state == "UP":
            return "00ff00"
        elif state == "UNKNOWN":
            return "888888"
        else:
            return "000000"

    def _customization_call(self, state):
        self._color = self._get_color(state)
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

        if args.skiplink:
            text_message = text_message + self._get_link(nagios_hostname)

        channel = self._get_channel(args.channel, self._PRIMARY_CHANNEL, self._SECONDARY_CHANNEL, self._LIST_STATE,
                                    self._LIST_SERVICEDISPLAYNAMES, self._nagios_state, nagios_servicedisplayname)

        json_data = {
            "@type": "MessageCard",
            "themeColor": self._color,
            "text": text_message
        }

        request_data = {
            'url' : channel,
            'data' : json.dumps(json_data)
        }

        return request_data

    def do_notify(self):
        request_data = self._get_request_data()

        headers = {'Content-type': 'application/json'}
        res = requests.post(request_data['url'], data=request_data['data'], headers=headers)
        return res


def main():
    teams = TeamsNotify()
    res = teams.do_notify()
    print(res)


if __name__ == "__main__":
    main()
