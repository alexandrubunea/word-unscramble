"""
						Phrase Unscramble						
															
				Author: https://github.com/alexandrubunea		
																
																
		Usage:													
				- First data input: the phrase you want to		
			unscramble.											
				- Second data input: the filter level you		
			want to apply. A lower value will offer a more		
			precise result. (Use -1 as value if you want no		
			filter level to be applied)							
																
																
			>>	Feel free to use and improve the code	<<		
																
"""


import urllib.error
import urllib.request

DICTIONARY_URL = 'https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt'


def request_dictionary_data(url):
    try:
        with urllib.request.urlopen(url) as response:
            html_data = response.read()
            raw_data = html_data.decode('utf-8')

            # formatting data before returning it
            raw_data = raw_data.replace("\r", "")
            raw_data = raw_data.lower()
            raw_data = raw_data.split("\n")
            raw_data[:] = [x for x in raw_data if len(x) > 2]  # removing words that have less than two letters

            return raw_data
    except urllib.error.HTTPError as e:
        print(e)

        return


def unscramble(source, lookup_data):
    source_structure = generate_word_structure(source)
    result_list = []

    for word in lookup_data:
        if len(word) <= len(source):
            word_structure = generate_word_structure(word)

            # comparing the two structures
            valid = True
            source_structure_copy = source_structure.copy()
            for letter in word:
                if letter in source_structure:
                    if word_structure[letter] > source_structure[letter]:
                        valid = False
                        break
                    else:
                        source_structure_copy[letter] -= word_structure[letter]
                else:
                    valid = False
                    break

            # formatting the result
            if valid:
                unused = ""
                for key in source_structure_copy:
                    if source_structure_copy[key] > 0:
                        for jjk in range(0, source_structure_copy[key]):
                            unused += str(key)
                r = "\033[32m" + word + "\033[31m" + unused
                result_list.append([r, len(unused)])
    return result_list


def generate_word_structure(word):
    word_structure = {}

    for letter in word:
        if letter in word_structure:
            word_structure[letter] += 1
        else:
            word_structure[letter] = 1

    return word_structure


if __name__ == '__main__':
    input_data = input("Introduce the scrambled phrase: ")
    input_data = input_data.lower()
    input_data = input_data.replace(" ", "")
    filter_level = int(input("Introduce the filter level(-1 for no filter level): "))

    result = unscramble(input_data, request_dictionary_data(DICTIONARY_URL))
    for i in result:
        if filter_level != -1:
            if i[1] == filter_level:
                print(i[0])
        else:
            print(i[0])
