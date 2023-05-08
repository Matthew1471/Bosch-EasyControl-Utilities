#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of Enphase-API <https://github.com/Matthew1471/Bosch-EasyControl-Utilities>
# Copyright (C) 2023 Matthew1471!
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# We decode some of the base64 values.
import base64

# We process JSON files.
import json

# Thanks to https://homematic-forum.de/forum/viewtopic.php?t=65434
def integer_to_homematic_ip_key(number):
    '''Converts integer number to Homematic IP key'''
    homematic_ip_alphabet = '0123456789ABCEFGHJKLMNPQRSTUWXYZ'
    result = ''
    while number > 0:
        result = homematic_ip_alphabet[number & 0b11111] + result
        if len(result) in [6,12,18,24]:
            result = '-' + result
        number >>= 5
    return result

def decode_known_encoded_paths(setting_path, setting_value):

    if len(setting_path) == 2:
        # Connected Devices.
        if setting_path[0] == 'devices':
            if len(setting_value['value']) == 1:
                setting_value['value'][0]['dlk'] = integer_to_homematic_ip_key(int(setting_value['value'][0]['dlk'], 16))
                setting_value['value'][0]['name'] = base64.b64decode(setting_value['value'][0]['name']).decode('utf-8')
        # Energy currency.
        elif setting_path[0] == 'energy' and setting_path[1] == 'currency':
            setting_value['value'] = base64.b64decode(setting_value['value']).decode('utf-8')

    elif len(setting_path) == 3:
        # Zone, program or device names.
        if setting_path[0] in ['zones', 'programs', 'devices'] and setting_path[2] == 'name':
            setting_value['value'] = base64.b64decode(setting_value['value']).decode('utf-8')
        # Gateway user address.
        elif setting_path[0] == 'gateway' and setting_path[1] == 'user' and setting_path[2] == 'address':
            if len(setting_value['value']) == 1:
                user_address = setting_value['value'][0]

                user_address['address'] = base64.b64decode(user_address['address']).decode('utf-8')
                user_address['city'] = base64.b64decode(user_address['city']).decode('utf-8')
                user_address['country'] = base64.b64decode(user_address['country']).decode('utf-8')
                user_address['state'] = base64.b64decode(user_address['state']).decode('utf-8')
                user_address['zip'] = base64.b64decode(user_address['zip']).decode('utf-8')
        # Gateway user name, email or phone.
        elif setting_path[0] == 'gateway' and setting_path[1] == 'user' and setting_path[2] in ['name', 'email', 'phone']:
            setting_value['value'] = base64.b64decode(setting_value['value']).decode('utf-8')
        # Gateway installer companyName, contactName, email or phone.
        elif setting_path[0] == 'gateway' and setting_path[1] == 'installer' and setting_path[2] in ['companyName', 'contactName', 'email', 'phone']:
            setting_value['value'] = base64.b64decode(setting_value['value']).decode('utf-8')

    elif len(setting_path) == 5:
        # Auto away users.
        if setting_path[0] == 'system' and setting_path[1] == 'autoAway' and setting_path[2] == 'users' and setting_path[4] == 'name':
            setting_value['value'] = base64.b64decode(setting_value['value']).decode('utf-8')

def convert_easycontrol_json_list(settings_json_list, decode = True, fix_booleans = True):
    # Heavily inspired by https://stackoverflow.com/questions/67440569/python-convert-path-to-dict.
    settings_json_dictionary = {}

    # Each of the list items is an individual setting with a URL path as its ID.
    for setting_value in settings_json_list:
        # Error if there is no ID key to identify the setting.
        if setting_value['id'] is None:
            raise ValueError('Missing setting key ID.')

        # Each setting has an ID that follows a URL structure; separate by slashes, disregarding the first '/'.
        settings_path = setting_value['id'].lstrip('/').split('/')

        # Remove the original ID from this setting as it has now been extracted.
        del setting_value['id']

        # We can fix some boolean types not being stored as JSON booleans.
        if fix_booleans:
            for key in ['available', 'recordable', 'used', 'writeable']:
                if key in setting_value:
                    # Python's bool() sees 'false' as true, so we implement a more conservative conversion.
                    if setting_value[key] in ['false', 0]:
                        setting_value[key] = False
                    elif setting_value[key] in ['true', 1]:
                        setting_value[key] = True

        # We can fix some settings being inconsistently Base64 encoded (and the device keys are Base32 encoded).
        if decode:
            decode_known_encoded_paths(settings_path, setting_value)

        # Pop off the last key-value component.
        setting_key = settings_path.pop(-1)

        # Find the target dict starting from the root.
        target_dict = settings_json_dictionary
        for component in settings_path:
            target_dict = target_dict.setdefault(component, {})

        # Assign the key and the value.
        target_dict[setting_key] = dict(sorted(setting_value.items()))

    # Return the new dictionary.
    return settings_json_dictionary

def main():
    # Load the settings_file.
    with open('Settings_Data.json', mode='r', encoding='utf-8') as settings_file:
        # Parse the settings_file as a JSON list of settings.
        settings_json_list = json.load(settings_file)

    # Convert the settings JSON list to a proper JSON dictionary (and decode encoded values where appropriate and fix JSON boolean types).
    converted_json_settings = convert_easycontrol_json_list(settings_json_list)

    # The converted settings JSON dictionary as a pretty-printed key ordered string.
    formatted_settings = json.dumps(converted_json_settings, indent=2, sort_keys=True)

    # Output the formatted output to the console.
    print(formatted_settings)

    # Write the formatted output to the output_file.
    with open('Settings_Data_Converted.json', mode='w', encoding='utf-8') as output_file:
        output_file.write(formatted_settings)

# Launch the main method if invoked directly.
if __name__ == '__main__':
    main()