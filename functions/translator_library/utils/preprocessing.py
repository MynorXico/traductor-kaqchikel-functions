def clean(sentence):
    sentence = sentence.lower()
    sentence = sentence.strip()
    sentence = sentence.replace("’", "'")
    sentence = sentence.replace('"', "")
    sentence = sentence.replace("’", "'")  # r"[\s]+[\n]+")
    sentence = sentence.replace(r"\t", " ")
    sentence = sentence.replace(r"[\s]+[\n]+", " ")
    sentence = sentence.replace(r"\s", " ")
    return sentence

def detokenize(sentence):
    return sentence.replace("@@ ", "")