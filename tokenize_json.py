import pandas as pd
import numpy as np
# Wordcloud
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from PIL import Image
import matplotlib.pyplot as plt
# NLTK
import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.probability import FreqDist

sufx = ["лар","нинг","гача","ган","ларда","моқда",'республика',"республикаси","республикада"]
uzbekistan = ["узбекистан","ўзбекистон"]
tashkent = ["ташкент"]

filename = r'data/domlajon_2020.json'
maskname = r'masks/box.png'
df = pd.read_json(filename)

def tokenize(text, word=True):
    """Text tokenization. By default performs word tokenization"""
    if word:
        from nltk.tokenize import word_tokenize
        return word_tokenize(text)
    else:
        from nltk.tokenize import sent_tokenize
        return sent_tokenize(text)

def remove_swords(text,lang="english"):
    """Removes stop words from the given text."""
    from nltk.corpus import stopwords
    stop_words=set(stopwords.words(lang))
    filtered_sent=[]
    for w in text:
        if w not in stop_words:
            filtered_sent.append(w)
    #print(f"{len(text)-len(filtered_sent)} words removed")
    return filtered_sent

def remove_urls(text):
    urls = ["https","t.me","www.",".uz",".com","p.s.","республик","ўзбекистон", "youtube","youtu"]
    new_text=[]
    for url in urls:
        for word in text:
            if url in word:
                text.remove(word)
    return text

def remove_sufx(text,sufx):
    new_text=[]
    for word in text:
        for suff in sufx:
            if word.endswith(suff):
                word = word[:-len(suff)]
        for prf in uzbekistan:
            if word.startswith(prf):
                word = "ўзбекистон"
        if word.startswith("ташкент"):
            word = "ташкент"
        if word.startswith("город"):
            word = "город"
        if word.startswith("люд"):
            word = "люди"
        if word.startswith("машин"):
            word = "машина"
        if word.startswith("uzam") or word.startswith("uzauto") or word.startswith("узавто"):
            word = "UzAM"

        new_text.append(word)
    return new_text

df["tokenized"] = ""
for ind in df.index:
    if type(df["message"][ind])==str:
        df["tokenized"][ind]=tokenize(df["message"][ind].lower())

df["filtered"] = ""
for ind in df.index:
     df["filtered"][ind]=remove_swords(df["tokenized"][ind],lang="uzbek")

for ind in df.index:
     df["filtered"][ind]=remove_swords(df["filtered"][ind],lang="russian")

df["cleaned"] = ""
for ind in df.index:
     df["cleaned"][ind]=remove_sufx(df["filtered"][ind],sufx)

for ind in df.index:
    df["cleaned"][ind]=remove_urls(df["cleaned"][ind])

df.to_json(r'data/all_cleaned.json')

# Detecting frequent words
text = []
for ind in df.index:
    text = text + df["cleaned"][ind]

comment_words = ""
for i in text:
    i = str(i)
    separate = i.split()
    for j in range(len(separate)):
        separate[j] = separate[j].lower()

    comment_words += " ".join(separate) + " "

stop_words=set(stopwords.words("uzbek"))
final_wordcloud = WordCloud(width = 800, height = 800,
                background_color ='white',
                stopwords = stop_words,
                min_font_size = 10, colormap='Set2').generate(comment_words)

# # Displaying the WordCloud
# plt.figure(figsize=(10, 10), facecolor=None)
# plt.imshow(final_wordcloud, interpolation='bilinear')
# plt.axis("off")
# plt.tight_layout(pad=0)
#
# plt.show()

# Wordcloud with contour and mask
# create coloring from image
stop_words=set(stopwords.words("uzbek"))
mask = np.array(Image.open(maskname))
mask_colors = ImageColorGenerator(mask)
wc = WordCloud(stopwords=stop_words,
               mask=mask,
               background_color="white",
               max_words=1000, #max_font_size=256,
               min_font_size=10, color_func=mask_colors,
               random_state=42, width=mask.shape[1],
               height=mask.shape[0], contour_width=1, contour_color='black')
wc.generate(comment_words)
plt.figure(figsize = (10, 10), facecolor = None)
plt.imshow(wc, interpolation="bilinear")
plt.axis('off')
# plt.savefig("wordcloud/zafarbek.png", format="png")
plt.show()