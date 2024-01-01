import json
import re

import httpx
import inquirer


class LiteQuran:
    BASE_URL = 'https://litequran.net'

    def __init__(self):
        self.surah_list = []
        self.session = httpx.Client()

    def __del__(self):
        self.session.close()

    def __fetch_surah_list(self):
        response = self.session.get(self.BASE_URL)
        self.surah_list = re.findall(r'li><a href="(.*?)"', response.text)

    def surah_select(self):
        self.__fetch_surah_list()
        surah_name = [
            inquirer.List(
                'surah',
                message = f'Found ({len(self.surah_list)}) surah! Your choice?',
                choices = [name.title() for name in self.surah_list]
            )
        ]
        answer = inquirer.prompt(surah_name)
        return answer['surah'].lower()

    def __findall(self, response, pattern):
        return ' '.join(re.findall(pattern, response))

    def surah_details(self, surah_name):
        response = self.session.get(f'{self.BASE_URL}/{surah_name}')
        surah_details = {}
        title_match = re.search(r'class="page-title">(.*?)<', response.text)

        surah_title = title_match.group(1) if title_match else None
        surah_title = surah_title.replace('Surat', 'Surah') if 'Surat' in surah_title else surah_title

        surah_details[surah_title] = {
            'arabic': self.__findall(response.text, r'class="arabic" dir="rtl">(.*?)<'),
            'translate': self.__findall(response.text, r'class="translate">(.*?)<'),
            'meaning': self.__findall(response.text, r'class="meaning">(.*?)<')
        }

        return surah_details

    def save_results(self, surah_details, surah_name):
        try:
            with open(f'{surah_name}.json', 'w', encoding='utf8') as file:
                json.dump(surah_details, file, indent=4, ensure_ascii=False)
            print(f'Your file has been saved successfully as {surah_name}.json')
        except IOError:
            print('An error occurred while saving the file.')
