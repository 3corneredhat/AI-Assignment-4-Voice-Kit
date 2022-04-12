#!/usr/bin/env python3
# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

'''A demo of the Google CloudSpeech recognizer.'''
import argparse
import locale
import logging
#Added for the conversational agent.
from aiy.board import Board, Led
from aiy.cloudspeech import CloudSpeechClient
import aiy.voice.tts
import random

def get_hints(language_code):
    if language_code.startswith('en_'):
        return ('turn on the light',
                'do you like music',
                'repeat after me',
                'do you like star wars',
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
    client = CloudSpeechClient()

    with Board() as board:
        while True:
            hints = get_hints(args.language) #init and reassign hints
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
            #Additional 1 adapted from AIY guide
            elif 'repeat after me' in text:
                aiy.voice.tts.say('Okay. Ready.')
                hints = ['i\'m done', 'done', 'i am']
                while True:
                    text = client.recognize(language_code=args.language, hint_phrases=hints)
                    if text is None:
                        logging.info('You said nothing.')
                        continue

                    logging.info('You said: "%s"' % text)
                    text = text.lower()
                    # Remove "repeat after me" from the text to be repeated
                    to_repeat = text.replace('repeat after me', '', 1)
                    if 'i\'m done'in text or 'i am done' in text:
                        aiy.voice.tts.say('Great! I hope that was fun for you.')
                        break
                    else:
                        aiy.voice.tts.say(to_repeat)
            #additional 2
            elif 'how are you' in text:
                aiy.voice.tts.say('I\'m doing well. How are you?')
                hints = ['good', 'excellent', 'bad','tired','sick','i\m', 'i am', 'feeling']
                while True:
                    logging.info('Say something.')
                    text = client.recognize(language_code=args.language, hint_phrases=hints)
                    if text is None:
                        logging.info('You said nothing.')
                        continue
                    logging.info('You said: "%s"' % text)
                    text = text.lower()
                    if 'good' in text or 'excellent' in text:
                        aiy.voice.tts.say('That\'s good to hear.')
                        break
                    elif 'bad' in text or 'tired' in text:
                        aiy.voice.tts.say("I hope your day gets better.")
                        break
                    elif 'sick' in text: 
                        aiy.voice.tts.say("I\'m sorry to hear that. Get well soon.")
                        break
            #additional 3
            elif 'can you speak other languages' in text or 'do you know other languages' in text:
                aiy.voice.tts.say('Yes. What language do you want me to speak?')
                while True:
                    hints = ['german', 'spanish', 'french','italian','english','korean','mandarin',
                             'only know how to say', 'i love you', 'languages']
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
                    elif 'only' in text and 'i love you' in text:
                        board.led.state = Led.BLINK
                        aiy.voice.tts.say("uh oh! you caught me!")
                        board.led.state = Led.OFF
                        break
                    else:
                        aiy.voice.tts.say('I can only say things in german, spanish, french, and italian')
            #additional 4
            elif 'do you like star wars' in text:
                aiy.voice.tts.say('Yes. Can you guess my favorite character?')
                count = 0
                hints = ['darth maul','luke skywalker', 'darth vader','princess leia','boba fett','r2 d2',
                             'c3po', 'mandalorian', 'grogu', 'IG11','baby yoda', 'yoda', 'obi-wan kenobi', 'han solo']
                while True:
                    logging.info('Say something.')
                    text = client.recognize(language_code=args.language, hint_phrases=hints)
                    if text is None:
                        logging.info('You said nothing.')
                        continue
                    logging.info('You said: "%s"' % text)

                    if 'IG11' in text:
                        aiy.voice.tts.say('That\'s right!')
                        break
                    elif 'give up' in text:
                        aiy.voice.tts.say('It is IG11 from the Mandolorian.')
                        break
                    elif count == 3:
                        aiy.voice.tts.say('I\'ll give you a hint. They are from the star wars extended universe.')
                        count += 1
                    else:
                        aiy.voice.tts.say('Try again.')
                        count+=1
            #additional 5
            elif 'do you listen to music' in text or 'do you like music' in text:
                aiy.voice.tts.say('yes. I enjoy listening to classical music.')
                hints = ['listen', 'like', 'other kinds', 'other kind', 'music', 'favorite composer', 'favourite composer']
                while True:
                    logging.info('Say something.')
                    text = client.recognize(language_code=args.language, hint_phrases=hints)
                    if text is None:
                        logging.info('You said nothing.')
                        continue
                    logging.info('You said: "%s"' % text)
                    text = text.lower()
                    if 'other kinds of music' in text or 'other kind of music' in text:
                        genre = ['rock', 'rap', 'classical', 'country']
                        rand_genre = genre[random.randint(0,len(genre)-1)]
                        aiy.voice.tts.say('I also enjoy listening to ' + rand_genre)
                        break
                    #this AI is very cultured, she likes to flex that she's multilingual. 
                    elif 'favourite composer' in text or 'favorite composer' in text:
                        aiy.voice.tts.say('if i had to choose it would be')
                        composers = [('johannes brahms','de-DE'), ('antonio vivaldi','it-IT'),
                                    ('manuel de falla','es-ES'), ('jean baptiste lully', 'fr-FR'),
                                    ('sir edward elgar','en-US')]
                        rand_composer = composers[random.randint(0,len(composers)-1)]
                        aiy.voice.tts.say(rand_composer[0],rand_composer[1])
                        break
            #additional 6
            elif 'can you tell me a joke' in text:
                aiy.voice.tts.say('sure. what kind of joke do you want to hear?')
                hints = ['dad','how about', 'computer science','can you','could you', 'joke', 'tell me',
                         'programmer', 'programming']
                program_jokes = ['A Computer Science student at MIT showed up at his'+
                                 ' buddies dorm room with a new bike. His buddy said, sweet bike,'+
                                 ' where did you get it?. You will never believe this, he said, '+
                                 ' I was walking across campus and this beautiful blonde on a'+
                                 ' bike stopped, threw down her bike, tore off all her clothes'+
                                 ' and said take whatever you want!. His buddy stared at him'+
                                 ' blankly for a minute, then said, smart, Her clothes would'+
                                 ' have never fit you.',
                                 'Why are i and j a good source of information?'+
                                 ' they\'re always in the loop',
                                 'My girlfriend dumped me after I named a class after her.'+
                                 ' She felt like I treated her like an object.' ]
                dad_jokes = ['Of all the inventions of the last 100 years, the dry erase board has to be the most remarkable.',
                             'Where do you take someone who\’s been injured in a peak-a-boo accident? To the I.C.U.',
                             'What has five toes but isn\'t your foot? My foot.'] 
                while True:
                    logging.info('Say something.')
                    text = client.recognize(language_code=args.language, hint_phrases=hints)
                    if text is None:
                        logging.info('You said nothing.')
                        continue
                    logging.info('You said: "%s"' % text)
                    text = text.lower()

                    if ('how about' in text or 'tell me' in text) and 'computer science' in text or 'programming' in text or 'programmer' in text:
                        rand_joke = program_jokes[random.randint(0,len(program_jokes)-1)]
                        aiy.voice.tts.say(rand_joke)
                        break
                    elif ('how about' in text or 'tell me' in text) and 'dad joke' in text:
                        rand_joke = dad_jokes[random.randint(0,len(dad_jokes)-1)]
                        aiy.voice.tts.say(rand_joke)
                        break
                    elif 'any' in text:
                        temp = program_jokes + dad_jokes
                        rand_joke = temp[random.randint(0,len(temp)-1)]
                        aiy.voice.tts.say(rand_joke)
                        break
            elif 'goodbye' in text:
                break

if __name__ == '__main__':
    main()
