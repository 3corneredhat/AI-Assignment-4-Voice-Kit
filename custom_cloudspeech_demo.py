#!/usr/bin/env python3
# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""A demo of the Google CloudSpeech recognizer."""
import argparse
import locale
import logging
import aiy.voice.tts

from aiy.board import Board, Led
from aiy.cloudspeech import CloudSpeechClient


def get_hints(language_code):
    if language_code.startswith('en_'):
        return ('turn on the light',
                'turn off the light',
                'blink the light',
                'goodbye')
    return None

def locale_language():
    language, _ = locale.getdefaultlocale()
    return language

def main():
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser(description='Assistant service example.')
    parser.add_argument('--language', default=locale_language())
    args = parser.parse_args()

    logging.info('Initializing for language %s...', args.language)
    hints = get_hints(args.language)
    client = CloudSpeechClient()
    with Board() as board:
        while True:
            if hints:
                logging.info('Say something, e.g. %s.' % ', '.join(hints))
            else:
                logging.info('Say something.')
            text = client.recognize(language_code=args.language,
                                    hint_phrases=hints)
            if text is None:
                logging.info('You said nothing.')
                continue

            logging.info('You said: "%s"' % text)
            text = text.lower()
            if 'turn on the light' in text:
                board.led.state = Led.ON
            elif 'turn off the light' in text:
                board.led.state = Led.OFF
            elif 'blink the light' in text:
                board.led.state = Led.BLINK
            #additional 1
            elif 'repeat after me' in text:
                aiy.voice.tts.say("Okay. Ready.")
                # Remove "repeat after me" from the text to be repeated
                while True:
                    if hints:
                        logging.info('Say something, e.g. %s.' % ', '.join(hints))
                    else:
                        logging.info('Say something.')
                    text = client.recognize(language_code=args.language, hint_phrases=hints)
                    if text is None:
                        logging.info('You said nothing.')
                        continue

                    logging.info('You said: \'%s' % text)
                    text = text.lower()
                    to_repeat = text.replace('repeat after me', '', 1)
                    if 'i\'m done' in text:
                        aiy.voice.tts.say('Great. I hope that was fun for you.')
                        break
                    else:
                        aiy.voice.tts.say(to_repeat)
            #additional 2
            elif 'can you speak other languages' in text or 'can you say things in other languages' in text:
                aiy.voice.tts.say('Yes. What language do you want to hear?')
                while True:
                    logging.info('Say something.')
                    text = client.recognize(language_code=args.language, hint_phrases=hints)
                    if text is None:
                        logging.info('You said nothing.')
                        continue
                    logging.info('You said: "%s"' % text)
                    text = text.lower()
                    if 'german' in text:
                        aiy.voice.tts.say('ich liebe dich', lang='de-DE')
                        break
                    elif 'spanish' in text:
                        aiy.voice.tts.say('te amo', lang='es-ES')
                        break
                    elif 'french' in text:
                        aiy.voice.tts.say('je t\'aime', lang='fr-FR')
                        break
                    elif 'italian' in text:
                        aiy.voice.tts.say('ti amo', lang='it-IT')
                        break
                    else:
                        aiy.voice.tts.say('I can only say things in german, spanish, french, and italian')
            #additional 3
            elif 'do you like star wars' in text:
                aiy.voice.tts.say('Yes. Can you guess my favorite character?')
                count = 0
                while True:
                    logging.info('Say something.')
                    text = client.recognize(language_code=args.language, hint_phrases=hints)
                    if text is None:
                        logging.info('You said nothing.')
                        continue
                    logging.info('You said: "%s"' % text)
                    text = text.lower()

                    if 'i g eleven' in text:
                        aiy.voice.tts.say('That\'s right!')
                        break
                    elif 'give up' in text:
                        aiy.voice.tts.say('It was i g eleven from the Mandolorian.')
                        break
                    elif count == 3:
                        aiy.voice.tts.say('I\'ll give you a hint. They are from the star wars extended universe.')
                    else:
                        aiy.voice.tts.say('Try again.')
                        count+=1
            #additional 4
            elif 'listen to music' in text:
                aiy.voice.tts.say('yes. I enjoy listening to classical music.')
                count = 0
                while True:
                    logging.info('Say something.')
                    text = client.recognize(language_code=args.language, hint_phrases=hints)
                    if text is None:
                        logging.info('You said nothing.')
                        continue
                    logging.info('You said: "%s"' % text)
                    text = text.lower()

                    if 'what other kind of music do you like' in text:
                        genre = ['rock', 'rap', 'classical', 'country']
                        random = random.randint(0,len(genre)-1)
                        aiy.voice.tts.say('I also enjoy listening to ' + random)
                        break
                    elif 'favorite composer' in text:
                        aiy.voice.tts.say('if i had to choose it would be')
                        composers = [('johannes brahms','de-DE'), ('antonio vivaldi','it-IT'),
                                    ('manuel de falla','es-ES'), ('jean baptiste lully', 'fr-FR'),
                                    ('sir edward elgar','en-US')]
                        rand_composer = random.randint(0,len(composers)-1)
                        aiy.voice.tts.say(rand_composer[0],rand_composer[1])
                        break
            elif 'goodbye' in text:
                break

if __name__ == '__main__':
    main()
