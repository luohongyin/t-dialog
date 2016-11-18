#! /usr/bin/env python
import os
import re

directory = '/data/sls/static/fisher/Part2/transcription/'
bracket_toks = 'bracket_toks'
chat = 'chat'

def _main( ):
    f_b_toks = open(bracket_toks, 'w')
    f_chat = open(chat, 'w')
    b_toks = set([])
    for filename in os.listdir(directory):
        if not filename.endswith(".txt"):
            continue
        f = open('%s/%s' % (directory, filename))
        f.readline()
        f.readline()
        prev_sent = None
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
            if prev_sent and sent:
                f_chat.write('%s\n%s\n' % (prev_sent, sent))
            prev_sent = sent

    for b_tok in b_toks:
        f_b_toks.write('%s\n' % b_tok)

if __name__ == '__main__':
    _main( )
