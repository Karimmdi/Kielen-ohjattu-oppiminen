clean_words = []

with open("./languages/finnish_words.txt", "r", encoding="utf-8") as file:
    for line in file:
        word =line.split()[0]
        clean_words.append(word)

with open("./languages/finnish_words_clean.txt", "w", encoding="utf-8") as file:
    for word in clean_words:
        file.write(word + "\n")
