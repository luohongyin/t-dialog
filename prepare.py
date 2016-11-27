#! /usr/bin/env python
import os
import re

directory = '/data/sls/static/fisher/Part2/transcription/'
topic_list = '/data/sls/static/fisher/Part2/liste_Fisher.lst'
bracket_toks = 'bracket_toks'
chat = 'chat'

# TODO: perhaps add token for end_of_sentences

def _main( ):
    f_b_toks = open(bracket_toks, 'w')
    f_chat = open(chat, 'w')
    b_toks = set([])

    # load topics
    topics = {}
    for line in open(topic_list):
        items = line.split(',')
        if len(items) == 12 and 'ENG' in items[3]:
            topics[items[0]] = items[3]

    for filename in os.listdir(directory):
        if not filename.endswith(".txt"):
            continue
        call_id = re.match('.*_.*_(\d+).txt', filename).group(1)
        # no label for topic
        if call_id not in topics:
            continue

        f = open('%s/%s' % (directory, filename))
        f.readline()
        f.readline()

        history_sent = '[Dialog_beginning]'
        prev_sent = '[Dialog_beginning]'
        for line in f:
            line = line.strip()
            if not line:
                continue
            words = re.split('\s+', line)
            sent = ''
            for i in range(3, len(words)):
                if re.search('[a-zA-Z]', words[i]):
                    if re.match('\[.+\]$', words[i]):
                        b_toks.add(words[i])
                        if words[i] == '[noise]':
                            continue
                    sent += ' ' + words[i]
            sent = sent.strip()
            # remove rubbish and empty sentences from training
            # this may not be practical in real condition
            if history_sent and prev_sent and sent:
                f_chat.write('%s %s %s\n%s\n' % (topics[call_id], history_sent, prev_sent, sent))
            history_sent, prev_sent = prev_sent, sent

    for b_tok in b_toks:
        f_b_toks.write('%s\n' % b_tok)

if __name__ == '__main__':
    _main( )
