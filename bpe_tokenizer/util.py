import json

from bpe_tokenizer.bpe_state import BpeState


def save_to_file(state: BpeState, path):
    with open(path, 'w') as built_table:
        built_table.write(json.dumps(state._get_map()))


def load_from_file(path):
    new_state = BpeState()

    with open(path, 'r') as table_data:
        new_state._set_map(json.load(table_data))

    return new_state
