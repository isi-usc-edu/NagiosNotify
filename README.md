# Nagios Notify
Nagios Integration with Slack and Microsoft Teams



## Description
Scripts to send Nagios notifications to Slack or Microsoft Teams.  The scripts support 
multiple channel notifications based on notification state (Host / Service) and service 
name (Service only)

All of the global variables at the beginning of nagiosnotify_slack.py and nagiosnotify_teams.py 
can be overriden by command line arguments.  Both nagiosnotify_slack.py and nagiosnotify_teams.py
require nagiosnotify.py, but do not require each other.

The code works with Python 2.6, 2.7, and 3.7.  The unit test code works with Python 2.7 and 3.7.



#### Logic blueprint:

| Override   | Primary  | Secondary | State List | Service Name List | Result                     | 
| :--------: |:--------:| :--------:| :---------:| :---------------: | :------------------------: | 
| A          | B        | C         | [ ]        | [ ]               | A                          | 
|            | B        |           |            |                   | B                          | 
|            | B        | C         |            |                   | B                          | 
|            | B        | C         | [ ]        |                   | if in [ ] C else B         | 
|            | B        | C         |            | [ ]               | if in [ ] C else B         | 
|            | B        | C         | [ ]        | [ ]               | if in [ ] and [ ] C else B |    



#### Script Arguments:

| Argument   | Name                 |  Purpose                                                                                               |
| :--------: |:--------------------:| :------------------------------------------------------------------------------------------------------|
|-h          | Help                 | Prints out help message regarding arguments                                                            |
|-c          | Override channel     | Overrides ALL channel values in the script or arguments                                                |
|-pc         | Primary channel      | Set the primary channel that is in the script                                                          |
|-sc         | Secondary channel    | Set the secondary channel that is in the script                                                        |
|-n          | Nagios               | Nagios hostname to create link to message                                                              |
|-svc        | List of Services     | Set the list of services that is in the script                                                         |
|-st         | List of States       | Set the list of states that is in the script.  Can be host or service states or both                   |
|-clr        | Clear Lists          | Set the list of services and list of states to empty lists                                             |
|-t          | Test                 | Bypass the Nagios ENV existance check and set to test data for testing.  Do not use in production      |
|-hm         | Host message         | Set the message used for host messages.  Use Python substitution, {#}, to replace with Nagios ENVs     |
|-hl         | Host message list    | Set the Nagios ENVs used for host message substitution                                                 |
|-sm         | Service message      | Set the message used for service messages.  Use Python substitution, {#}, to replace with Nagios ENVs  |
|-sl         | Service message list | Set the Nagios ENVs used for service message substitution                                              |
|-sk         | Skip Nagios link     | Do not put the link to Nagios onto the message                                                         |
|-si         | Skip icon            | **SLACK ONLY** Skip putting an icon onto the message                                                   |
|-b          | BOT Name             | **SLACK ONLY** Override the BOT name that is in the script                                             |
|-wh         | WebHook URL          | **SLACK ONLY** Override the web hook URL that is in the script                                         |



#### Use Cases:

1. All notifications go to a single channel - applies to host and service notification
   1. Pass in the override channel  
   1. Just set the primary channel value, don't set value for secondary channel

1. Elevate/Downgrade notifications - applies to host and/or service based on values in the state list
   1. Set primary and secondary channel values.  Set states that should be in the secondary channel.

1. Elevate/Downgrade service notifications - applies to service notifications only
   1. Set primary and secondary channel values.  Set the service names that should be in the secondary channel.

1. Elevate/Downgrade service notifications based on their state - applies to service notifications only
   1. Set primary and secondary channel values.  Set the service names and service states that should be in the secondary channel.



## Script configuration

Here are the minimum global variables needed to configure each notification script

1. nagiosnotify_slack.py
    1. _NAGIOS_SERVER - DNS name of your Nagios server.  Used to create links inside notifications
    1. _PRIMARY_CHANNEL - #primary-channel - Channel where notifications should go
    1. _SECONDARY_CHANNEL - #secondary-channel - Secondary channel - NOTE: Requires setting _LIST_SERVICEDISPLAYNAMES or _LIST_STATE
    1. _WEB_HOOK_URL - https://... - The Incoming Web Hook URL that has been configured with your organization
1. nagiosnotify_teams.py
    1. _NAGIOS_SERVER - DNS name of your Nagios server.  Used to create links inside notifications
    1. _PRIMARY_CHANNEL - https://... - The Web Hook URL that has been configured with your primary channel
    1. _SECONDARY_CHANNEL - https://... - The Web Hook URL that has been configured with your secondary channel NOTE: Requires setting _LIST_SERVICEDISPLAYNAMES or _LIST_STATE


## Nagios configuration

Steps to configure the notifications within Nagios.

1. Select Configure > Core Config Manager
    1. Select Commands > Add New > set the following values
        1. Command Name:  slack-host-notification
        1. Command Line:  $USER1$/nagiosnotify_slack.py -c "$_CONTACTOVERRIDECHANNEL$" > /tmp/slack2.log 2>&1
        1. Command Type:  misc command
        1. Active should be checked
    1. Select Save > Add New > set the following values
        1. Command Name:  slack-service-notification
        1. Command Line:  $USER1$/nagiosnotify_slack.py -c "$_CONTACTOVERRIDECHANNEL$" > /tmp/slack2.log 2>&1
        1. Command Type:  misc command
        1. Active should be checked
    1. Select Save > Apply Configuration
1. Select Configure > Core Config Manager
    1. Select Contacts > Add New > set the following values (you can choose Skip for any value not mentioned)
        1. Common Settings > Contact Name: Slack
        1. Common Settings > Description: Slack notification
        1. Alert Settings > Host Notifications Timeperiod: 24x7
        1. Alert Settings > Service Notifications Timeperiod: 24x7
        1. Alert Settings > Host Notification options: Down, Up
        1. Alert Settings > Service Notification options: Warning, Unknown, Critical, Ok
        1. Alert Settings > Manage Host Notification Commands: slack-host-notification
        1. Alert Settings > Manage Service Notification Commands: slack-service-notification
        1. NOTE: For an Override contact, do the same as above but then do the following.  Do not do this for the Slack contact
            1. Misc Settings > Manage Free Variables > 
                1. Name: _overridechannel    NOTE: This is the same channel name as $_CONTACTOVERRIDECHANNEL$ using Nagios rules for Contact ENVs
                1. Value: #some-override-channel
            1. Select Insert
        1. Select Save > Apply Configuration
1. Add the contact to any host or service configuration



