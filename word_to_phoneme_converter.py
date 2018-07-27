import os
import nltk
import math
from arpabet_to_ipa_mapping import arpabet_to_ipa
import codecs

old_align_file_path = "gridcorpus_dataset/align/align/"
new_align_file_path = "gridcorpus_dataset/align_ipa/"
file_list = os.listdir(old_align_file_path)
nltk.download('cmudict')
arpabet = nltk.corpus.cmudict.dict()

frequency_dict = {}
lengths_dict = {}

def split_line(line):
	split = line.split(' ')
	word = split[2]
	word = word.rstrip('\n')
	return int(split[0]), int(split[1]), word

def get_phonemes(word):
	phonemes = arpabet[word]
	max_length = max([len(p) for p in phonemes])
	for i in phonemes:
		if len(i) == max_length:
			for p in [arpabet_to_ipa(x) for x in i]:
				if p not in frequency_dict:
					frequency_dict[p] = 1
				else:
					frequency_dict[p] += 1
			return i

if not os.path.exists(new_align_file_path):
    os.makedirs(new_align_file_path)

index = 0
for file in file_list:
	f = open(old_align_file_path + file)
	f_new = codecs.open(new_align_file_path + os.path.split(file)[1], 'a', encoding='utf8')
	f_new.seek(0)
	f_new.truncate()
	p_count = 0
	for line in f:
		start_time, end_time, word = split_line(line)
		if not word == "sil" and not word == "sp":
			word_phonemes = get_phonemes(word)
			word_ipa = [arpabet_to_ipa(p) for p in word_phonemes]
			p_count += len(word_ipa)
			phoneme_duration = (float(end_time) - float(start_time)) / len(word_ipa)

			time = start_time
			for phoneme in word_ipa:
				f_new.write(str.format("{} {} {}\n", str(int(time)), str(int(min(round(time + phoneme_duration, 0), int(end_time)))), phoneme))
				time += phoneme_duration
				time = round(time, 0)
		else:
			f_new.write(str.format("{} {} {}\n", str(int(start_time)), str(int(end_time)), '_'))
	if p_count not in lengths_dict:
			lengths_dict[p_count] = 1
	else:
		lengths_dict[p_count] += 1
	index += 1
	if index % 1000 == 0:
		print(index)

f.close()
f_new.close()

#print(frequency_dict)
print(lengths_dict)

file = codecs.open(new_align_file_path + "/../" + "stats.txt", 'a', encoding='utf8')
file.write("IPA CHARACTER FREQUENCY: " + str(frequency_dict) + "\n")
file.write("# of OCCURENCES OF EACH # OF IPA's: " + str(lengths_dict) + "\n")
file.close()

