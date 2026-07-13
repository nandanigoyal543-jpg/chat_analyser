import re
import pandas as pd

from wordcloud import WordCloud
from urlextract import URLExtract
extractor = URLExtract()
def fetch_stats(selected_user,df):
    if selected_user=='Overall':
        num_messages=df.shape[0]
        num_media_messages=df[df['message']=='<Media omitted>\n'].shape[0]
        words=[]
        for message in df['message']:
            words.extend(message.split())
        num_words=len(words)
        links=[]
        for message in df['message']:
            links.extend(extractor.find_urls(message))
        num_links=len(links)

    else:
        newdf=df[df['user']==selected_user]
        num_messages=newdf.shape[0]
        words=[]
        for message in newdf['message']:
            words.extend(message.split())
        num_words=len(words)
        num_media_messages=newdf[newdf['message']=='<Media omitted>\n'].shape[0]
        links=[]
        for message in newdf['message']:
            links.extend(extractor.find_urls(message))
        num_links=len(links)
    return num_messages, num_words, num_media_messages,num_links
def most_busy_users(df):
    x=df['user'].value_counts().head()
    y=round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'count':'percentage'})
    return x, y
def create_wordcloud(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    wc = WordCloud(
        width=500,
        height=500,
        min_font_size=10,
        background_color='white'
    )

    text = df['message'].str.cat(sep=" ")
    text = text.replace("<Media omitted>\n", "")
    df_wc = wc.generate(text)

    return df_wc
def most_common_words(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['user'] != 'Meta AI']
    temp = temp[temp['message'] != '<Media omitted>\n']

    hinglish_stopwords = {

# Common pronouns
"mai","main","me","mein","maii","m","hum","ham","hamara","hamari","hamare",
"tu","tum","tumhe","tumko","tumhara","tumhari","tumhare",
"aap","ap","apko","aapko","apka","aapka","apki","aapki","apke","aapke",
"wo","woh","vo","ye","yeh","yah","yeha","yaha","yahaan","waha","wahaan",
"us","usse","uska","uski","uske","iska","iski","iske",
"in","inka","inki","inke","un","unka","unki","unke",

# Question words
"kya","kyu","kyun","kyon","kab","kaise","kaha","kahan","kidhar",
"kis","kisko","kiski","kiska","kiski","kisne","kon","kaun","kaunsa",
"kaunsi","kaunsa",

# Connectors
"to","toh","tho","tohh","aur","ya","yaa","yaar","fir","phir","agar",
"magar","lekin","par","per","kyuki","kyunki","isliye","isliyee",
"jab","tab","ab","abhi","phle","pehle","baad","baadme","baadmein",

# Common verbs
"hai","h","ha","haa","haan","han","hn","hnn","ho","hu","hun","hua",
"hui","hue","hona","hoja","hojaye","hojayega","tha","thi","the",
"rha","rhaa","raha","rahaa","rhi","rahi","rhee","rhe","rahe",
"kar","kr","krr","karna","krna","krke","karke","krdia","krdiya",
"kiya","kia","kiye","ki","ka","ke","ko","se","par","tak",
"de","do","di","dia","diya","dene","dena","dega","degi",
"le","lo","li","lia","liya","lene","lena","lega","legi",
"bol","bola","boli","bolna","bolte","bolti","sun","suno","dekh","dekho",
"aaya","aya","aayi","ayi","gaya","gya","gyi","gayi","gye","gaye",
"aana","jana","ja","jaa","jao","jao","jaise","jaisa","jaisi",
"chal","chalo","chalna","nikal","rakha","rakhi","rakhe",

# Fillers
"na","ni","nhi","nahi","nahi","nai","nah","mat","mt","bhi","hi","he",
"ji","re","are","abe","oye","arre","accha","acha","achha","theek","thik",
"sahi","galat","bas","bus","bhai","bhaiya","behen","beta","yar","yaar",
"yr","bro","bros","bruh","sis","buddy","dude",

# Time words
"aaj","aj","kal","kl","subah","shaam","sham","raat","din","roz",
"abhi","ab","tab","kabhi","hamesha","baar","bar","baarbaar",

# Casual chat
"ok","okay","okk","okkk","oky","k","kk","hmm","hm","hmmm","hmmmm",
"haha","hahaha","hehe","hehehe","lol","lmao","rofl","xd","yo","sup",
"hello","hi","bye","good","morning","night","gn","gm","tc",
"pls","plz","please","thx","thanks","thankyou","welcome",

# Roman Hindi variants
"toh","to","ha","haa","han","haan","mai","mein","me","maii",
"ye","yeh","wo","woh","vo","jo","jis","jise","jisko","jiska",
"waise","vaise","aisa","aisi","aise","itna","itni","itne",
"utna","utni","utne","sab","sabka","sabki","sabke",
"kuch","kisi","kisiko","bahut","bohot","bahot","zyada","jyada","kam",

# Chat abbreviations
"bt","bcz","bcz","coz","coz","cz","bc","fr","idk","imo","ikr","btw","omg",

# Media words
"media","omitted","deleted","message","messages",
"gif","video","image","photo","sticker","forwarded",

# URLs
"http","https","www","com","net","org","co","in"
}
    words = []
    for message in temp['message']:
        message = message.lower()
        message = re.sub(r'[^\w\s]', '', message)
        for word in message.split():
            if word not in hinglish_stopwords:
                words.append(word)

    from collections import Counter 
    return pd.DataFrame(Counter(words).most_common(20), columns=['Word', 'Frequency'])
def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time
    return timeline
def weekly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['dayname'].value_counts()
        