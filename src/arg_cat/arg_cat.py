import getopt
import os
import sys
from typing import List


class KeyEntity(object):
    def __init__(self):
        self.key: str = ''
        self.key_short: str = ''
        self.key_upper: str = ''
        self.value: str = ''
        self.bool_value: bool = False
        self.is_a_bool: bool = False
        self.is_a_path: bool = False


class ArgCat:

    keys = {}

    def add_key(self, key: str, is_a_bool: bool = False, is_a_path: bool = False):
        key_entity = KeyEntity()
        key_entity.key = key
        key_entity.key_upper = key.upper()
        key_entity.key_short = key[0]
        if is_a_bool:
            key_entity.is_a_bool = is_a_bool
            key_entity.value = 'False'
        if is_a_path:
            key_entity.is_a_path = is_a_path
        self.add_key_entity(key_entity)

    def add_keys(self, keys: List[str]):
        for key in keys:
            self.add_key(key)

    def add_key_entity(self, key_entity: KeyEntity):
        if ' ' in key_entity.key:
            raise Exception('Key can not include space.')
        if ' ' in key_entity.key_upper:
            raise Exception('Key upper can not include space.')
        if key_entity.key == '':
            raise Exception('Key can not be empty.')
        if key_entity.key_upper == '':
            key_entity.key_upper = key_entity.key.upper()
        if key_entity.key_short == '':
            key_entity.key_upper = key_entity.key[0]
        self.keys[key_entity.key] = key_entity

    def add_key_entities(self, key_entities: List[KeyEntity]):
        for key_entity in key_entities:
            self.add_key_entity(key_entity)

    def from_arg(self):
        key_list = []
        for key_entity in self.keys.values():
            key = key_entity.key
            if not key_entity.is_a_bool:
                key = key + "="
            key_list.append(key)
        key_short_list = ''
        for key_entity in self.keys.values():
            key_short = key_entity.key_short
            if not key_entity.is_a_bool:
                key_short = key_short + ":"
            key_short_list += key_short
        try:
            opts, args = getopt.getopt(sys.argv[1:], key_short_list, key_list)
        except getopt.GetoptError as err:
            print(str(err))
            sys.exit(2)
        for opt, arg in opts:
            if opt.startswith('--'):
                full_opt = opt[2:]
                if full_opt in self.keys.keys():
                    for key_entity in self.keys.values():
                        if key_entity.key == full_opt:
                            self.__set_key_entity_value(key_entity, arg)
                        else:
                            continue
                else:
                    print(f"{opt} command not in the arg_cat arg list.")
                    sys.exit(2)
            elif opt.startswith('-'):
                short_opt = opt[1:]
                if short_opt in key_short_list:
                    for key_entity in self.keys.values():
                        if key_entity.key_short == short_opt:
                            self.__set_key_entity_value(key_entity, arg)
                        else:
                            continue
                else:
                    print(f"{opt} command not in the arg_cat arg list.")
                    sys.exit(2)
            else:
                print(f"{opt} command is not an arg.")
                sys.exit(2)
        pass

    def from_environ(self):
        for key_entity in self.keys.values():
            if key_entity.key_upper in os.environ:
                self.__set_key_entity_value(key_entity, os.environ[key_entity.key_upper], from_env=True)
            else:
                continue

    def from_arg_and_environ(self, environ_override_all: bool = False):
        if environ_override_all:
            self.from_arg()
            self.from_environ()
        else:
            self.from_environ()
            self.from_arg()

    def get_string(self, key: str) -> str:
        if not self.keys[key].is_a_bool:
            return self.keys[key].value
        raise Exception(f"The `{key}` is not a string arg.")

    def get_bool(self, key: str) -> bool:
        if self.keys[key].is_a_bool:
            return self.keys[key].bool_value
        raise Exception(f"The `{key}` is not a bool arg.")

    def put(self, key: str, value, is_a_bool: bool = False, is_a_path: bool = False):
        if key not in self.keys.keys():
            self.add_key(key, is_a_bool, is_a_path)
        self.__set_key_entity_value(self.keys[key], f'{value}', from_env=True)

    def __set_key_entity_value(self, key_entity: KeyEntity, value: str, from_env: bool = False):
        if key_entity.is_a_bool:
            if from_env:
                if value in ['True', 'true', 'Yes', 'yes', 'y', '1']:
                    key_entity.bool_value = True
                else:
                    key_entity.bool_value = False
            else:
                key_entity.bool_value = True
        elif key_entity.is_a_path:
            key_entity.value = os.path.join(os.getcwd(), value)
        else:
            key_entity.value = value
