import logging
import os
import argparse
import bpe_tokenizer.util
import bpe_tokenizer.bpe_state

DEFAULT_MIN_WORD_COUNT = -1

parser = argparse.ArgumentParser()

parser.add_argument('-d', '--data-set', help='Path to data-set', required=True)
parser.add_argument('-o', '--output-path', help='Where to save a model', required=True)
parser.add_argument('-n', '--name', help='Name of saved model', required=True)
parser.add_argument('-e', '--epoch', help='Number of merging iterations', type=int, default=50)
parser.add_argument('-w', '--word-count',
                    help='Stop when this number of words is completed',
                    type=int,
                    default=DEFAULT_MIN_WORD_COUNT)

args = parser.parse_args()

logging.basicConfig(level=logging.INFO)
bpe_state = bpe_tokenizer.bpe_state.BpeState(epoch=args.epoch)

for (root, _, files) in os.walk(args.data_set):
    for file in files:
        with open(os.path.join(root, file), 'r') as data:
            source = data.read()

        bpe_state.update(source)

        logging.info('{file_name} is processed, number of words: {word_count}'.format(file_name=file,
                                                                                      word_count=bpe_state.words()))

        if args.word_count != DEFAULT_MIN_WORD_COUNT and bpe_state.words() >= args.word_count:
            break

bpe_tokenizer.util.save_to_file(bpe_state, os.path.join(args.output_path, args.name))

logging.info('Table is built and supports {count} words'.format(count=bpe_state.words()))
