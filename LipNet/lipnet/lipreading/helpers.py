map = {"eɪ" : 0, "aɪ":1, "oʊ":2, "aʊ":3, "ɔɪ":4, "tʃ":5, "dʒ":6, "ɜr":7, "ər":8}
 
def text_to_labels(text):
    ipaArray = text.split('|')
    label = []
    for ipa in ipaArray:
        if ipa == ' ':
            label.append(26)
        elif len(ipa) > 1:
            label.append(map[ipa])
        else :
            label.append(ord(ipa))
    return label
 
def labels_to_text(labels):
    text = ''
    for label in labels:
        if label < 10 :
            for ipa, number in map.items():
                if(number == label):
                    text += ipa
        elif label == 26:
            text += ' '
        else :
            text += chr(label)
        text += '|'
    return text