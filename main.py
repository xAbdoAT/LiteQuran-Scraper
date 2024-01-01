import json
import os

from api import LiteQuran


def main():
    litequran = LiteQuran()
    surah_name = litequran.surah_select()
    print(f'Your choice: {surah_name}')

    surah_details = litequran.surah_details(surah_name)
    print(json.dumps(surah_details, indent=4, ensure_ascii=False))

    save_to_file = input('Do you want to save the results? (y/n): ').lower()
    if save_to_file == 'y':
        if os.path.exists(f'{surah_name}.json'):
            print('Already saved!')
        else:
            litequran.save_results(surah_details, surah_name)
    else:
        print('Bye')


if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear')
    main()
