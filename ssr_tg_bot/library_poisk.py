import pytesseract
import cv2


class Search_word:
    @staticmethod
    def find_suggestions(text: str) -> list:
        mass_predl = []
        slovo = ''
        for i in range(len(text)):
            if text[i] == ',' or text[i] == ' ' or text[i] == '(' or text[i] == ')':
                slovo += str(text[i])
                continue
            elif text[i].isalpha():
                slovo += str(text[i])
            else:
                mass_predl.append(slovo)
                slovo = ''
        else:
            mass_predl.append(slovo)
        return mass_predl


    @staticmethod
    def find_word_for_percent(word: str, texts: list[str], percent: int = 100,
                              register: bool = False) -> list:  # функция которая находит предложения
        lists_result = []
        for text in texts:
            mass_sentence = Search_word.find_suggestions(text)
            res_sentence = []
            if mass_sentence:
                for i in mass_sentence:
                    if percent != 100:
                        if register == False:
                            mass_word = list(map(lambda x: x.lower(), i.split()))
                            word = word.lower()
                        else:
                            mass_word = i.split()
                        for j in mass_word:
                            if j:
                                if len(word) == len(j):
                                    count_alpha = 100 // len(j)
                                    count_res = 0

                                    for em in range(len(j)):
                                        if j[em] == word[em]:
                                            count_res += count_alpha
                                        if count_res >= percent:
                                            res_sentence.append(i.strip())
                                            break

                    else:
                        if register == False:
                            for i_item in i.split():
                                if word.lower() == i_item.lower():
                                    res_sentence.append(i.strip())
                        else:
                            for i_item in i.split():
                                if word == i_item:
                                    res_sentence.append(i.strip())
            if res_sentence:
                for i in res_sentence:
                    lists_result.append(i)

        return lists_result

    @classmethod
    def download_file_suggestions(cls, word: str, text: str, file: str):
        list_suggestions = cls.find_suggestions(text)
        list_writeline_file = []
        if list_suggestions:
            for i in list_suggestions:
                if word.lower() in i.lower():
                    list_writeline_file.append(i)
            with open(file, 'w', encoding='utf-8') as file:
                file.writelines(list_writeline_file)
                return 'ok'
        else:
            with open(file, encoding='utf-8') as file:
                file.writelines(list_writeline_file)
            return 'ok'

    @staticmethod
    def download_file_after_sound():
        ...

    @staticmethod
    def massiv_word(word: list[str], full_text: str) -> dict:
        slovar = {}
        for i in word:
            lists_predl = Search_word.find_suggestions(full_text)
            vip_predl = []
            if lists_predl:
                for j in lists_predl:
                    if i.lower() in j.lower():
                        vip_predl.append(j)
            slovar[i] = vip_predl
            return slovar

    @staticmethod
    def find_for_file_txt(word: str, files: list[str], register=False) -> list:
        lists_res = []
        for file in files:
            if file.endswith('.txt'):
                with open(file, 'r', encoding='utf-8') as fl:
                    list_for_text = fl.readlines()
                full_text = ''
                for i in list_for_text:
                    full_text += i
                lists_suggestions = Search_word.find_suggestions(full_text)
                if lists_suggestions:
                    if register:
                        res = Search_word.find_word_for_percent(word, lists_suggestions, register=True)
                    else:
                        res = Search_word.find_word_for_percent(word, lists_suggestions, register=False)
                    if res:
                        for r in res:
                            lists_res.append(r)
        return lists_res
    # не работает т.к отключил нейронку
    # @staticmethod
    # def find_for_photo(photos: list[str], word: str, lang: str = 'rus') -> list:
    #     pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    #     lists_result = []
    #     for photo in photos:
    #         image = cv2.imread(photo)
    #         # получаем строку
    #         string = pytesseract.image_to_string(image, lang=lang)
    #         res = Search_word.find_word_for_percent(word, [string], 70, register=True)
    #         if res:
    #             lists_result.append(res)
    #     return lists_result

    @staticmethod
    def copy_text_for_txt(text, name):
        new_text = text.split('.')
        with open(f'file/{name}', 'w', encoding='utf-8') as file:
            file.write('')
        with open(f'file/{name}', 'a+', encoding='utf-8') as file:
            file.writelines(new_text)
        return f'file/{name}'

    @staticmethod
    def replace_word_in_message(word: str, new_word: str, text: str, text_ind: str):
        list_suggestion = Search_word.find_suggestions(text)
        mass_result = ''
        mass_text = []
        for i in range(len(list_suggestion)):

            if word in list_suggestion[i]:
                mass_text.append(list_suggestion[i])
        if text_ind == 'последний':
            list_suggestion[list_suggestion.index(mass_text[-1])] = str(
                list_suggestion[list_suggestion.index(mass_text[-1])]).replace(word, new_word)
        elif text_ind == 'первый':
            list_suggestion[list_suggestion.index(mass_text[0])] = str(
                list_suggestion[list_suggestion.index(mass_text[0])]).replace(word, new_word)
        else:
            for i in range(len(list_suggestion)):
                if word in list_suggestion[i]:
                    list_suggestion[i] = str(list_suggestion[i]).replace(word, new_word)

        for j in list_suggestion:
            mass_result += j
        return mass_result

