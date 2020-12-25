# bpe-ts
Simple BPE tokenizer service with utility script

# Prerequisites
In order to use the project you need:
 - Python 3.x or higher
 - Flask module

# Creating new table
Project provides you with utility script (called `bpe_create.py`) to create your own BPE tables that can be further used for server processing. Usage example:
```shell
python bpe_create.py \
-d dataset \           # Path to dataset that should be used
-o ./ \                # Path where we should save a model
-n eng_only_10000.bpe\ # Name of saved table
-e 1000 \              # Number of merging iterations (the bigger -> the better -> the slower)
-w 10000 \             # Number of words that table should support (if not specified - there's no upper boundary)
```

For additional information use:
```shell
python bpe_create.py --help
```

# Running processing server
In order to run `bpe-ts` server you should call `bpe_processing_server.py` and specify what BPE-table should be used:
```shell
python bpe_processing_server.py \
-t eng_only_10000.bpe \           # Path to prebuilt table
-p 8080                           # Port where to run a server
```

For additional information use:
```shell
python bpe_processing_server.py --help
```

# Using processsing server
Currently `bpe-ts` server supports only one REST-method called `/process`. It expects a data from you in format:
```
{
  'text': '<text_to_process>'
}
```

Response format is:
```
{
  'status': 'ok',
  'processed_text': '<processed_text>'
}
```

To test processing server with CURL use command:
```shell
curl --header "Content-Type: application/json" \
--request POST\
-d "{\"text\":\"This is my great text and I'd like to see it tokenized\"}"  \
<server_address>:<server_port>/process
```
