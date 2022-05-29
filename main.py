# новые библиотеки: pip install nltk
from tika import parser
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.stem import SnowballStemmer
import os

stemmer = SnowballStemmer(language='russian')

# Словари для проверки определенных тендеций
economics = ['business', 'economic', 'economics', 'development', 'resources', 'exploitation', 'project', 'projects']
humans = ['human', 'humans', 'indigenous', 'people', 'peoples', 'rights', 'nation', 'nations', 'folk', 'folks', 'social', 'welfare', 'safety', 'education', 'educational']
politics = ['politics', 'cooperation', 'international', 'political', 'policy', 'management']
ecology = ['ecology', 'pollution', 'environment', 'climate', 'security', 'safety', 'science']

economics_ru = {'бизнес': 'бизнес', 'экономик': 'экономика', 'развит': 'развитие', 'ресурс':'ресурсы', 'освоен': 'освоение',
                'проект': 'проект', 'финансировани': 'финансирование', 'бюджет': 'бюджет', 'инвестици': 'инвестиции', 'политик':'политика'}
social_ru = {'человек': 'человек', 'люд': 'люди', 'коренн': 'коренной', 'прав': 'права', 'нац': 'нация', 'социальн': 'социальный',
             'безопасн': 'безопасность', 'образован': 'образование', 'обществ': 'общество',
             'культур': 'культура', 'здравоохранени': 'здравоохранение', 'программ': 'программа', 'наук':'наука'}
foreign_ru ={'международная политик': ' международная политика', 'сотрудничеств':'сотрудничество', 'международн':'международный',
             'миров': 'мировой', 'договор': 'договор', 'двусторонн': 'двусторонний', 'иностранн': 'иностранный'}
ecology_ru = {'эколог':'экология', 'загрязнен':'загрязнение', 'окружающая сред':'окружающая среда', 'климат':'климат',
              'изменение климат':'изменение климата', 'охран':'охрана', 'природ': 'природа', 'экологическ': 'экологический'}

# Для дальнейшей удобного обращения к словарям, я их пронумеровала
# экономика - 1
# социалка -2
# форейн - 3
# экология - 4

tendencies_ru = [economics_ru, social_ru, foreign_ru, ecology_ru]

# функция очистки текста от знаков препинания
def remove_punc(inp_string):
    s = '''!()-[]{};?@#$%:'"\,./^&amp;*_'''
    nums = '1234567890'
    for i in inp_string:
        if i in s or i in nums:
            inp_string = inp_string.replace(i, "")
    
    return inp_string

economics_tendency = []
social_tendency = []
foreign_tendency = []
ecology_tendency = []

# Вставить свою ссылку ria_news
# ссылка к файлу
link = '/Users/sarantuaa/Documents/content-analyze/ria_news'

for file in os.listdir(link):
    
    print("Открыт файл: " + file)
    raw = parser.from_file('/Users/sarantuaa/Documents/content-analyze/ria_news/' + file) # Вставить свою ссылку ria_news

    content_nofilter = raw['content'].split()

    content = []
    for i in content_nofilter:
        i = remove_punc(i)
        if i != "":
            content.append(i)

    all_words = len(content)
    print(all_words)

    df_columns = ['word', 'frequency', 'frequency (%)']

    tendency_count = 1 # какой словарь, начинается с экономики, поэтому экономика - 1 (там по порядку считаются эти словари в списке)
    for tendency in tendencies_ru:
        rows = []
        count_tendency = 0 # считаем сколько слов словаря в общем занимает в тексте
        for word in tendency.keys():

            count = 0
            for i in content:
                stemme_token = stemmer.stem(i)
                if stemme_token == word:
                    count+=1
                    count_tendency+=1
    
            rows.append({'word': tendency[word], 'frequency': count, 'frequency (%)': (count/all_words)*100})
    
        print(tendency)
        print(pd.DataFrame(rows, columns=df_columns))
        out_df = pd.DataFrame(rows, columns=df_columns)
        # Вставить свою ссылку csv_files
        out_df.to_csv(path_or_buf='/Users/sarantuaa/Documents/content-analyze/csv_files/' + str(tendency_count) + '_' + file +'.csv', index=False, mode='w', header=True) 

        if tendency_count == 1:
            economics_tendency.append({'year': file, 'frequency': (count_tendency/all_words)*100})
        elif tendency_count == 2:
            social_tendency.append({'year': file, 'frequency': (count_tendency/all_words)*100})
        elif tendency_count == 3:
            foreign_tendency.append({'year': file, 'frequency': (count_tendency/all_words)*100})
        elif tendency_count == 4:
            ecology_tendency.append({'year': file, 'frequency': (count_tendency/all_words)*100})
        
        tendency_count+=1

    text = ''
    for i in content:

        stemmed_token = stemmer.stem(i)

        if stemmed_token in economics_ru.keys():
            text = text + economics_ru[stemmed_token] + ' '
        elif stemmed_token in ecology_ru.keys():
            text = text + ecology_ru[stemmed_token] + ' '
        elif stemmed_token in foreign_ru.keys():
            text = text + foreign_ru[stemmed_token] + ' '
        elif stemmed_token in social_ru.keys():
            text = text + social_ru[stemmed_token] + ' '

    cloud = WordCloud(collocations=False).generate(text)
    plt.imshow(cloud)
    plt.axis('off')
    plt.savefig('/Users/sarantuaa/Documents/content-analyze/wordclouds/' + file + '.png') # Вставить свою ссылку wordclouds
    plt.close()

# df_columns = ['year', 'frequency']

# out_df = pd.DataFrame(economics_tendency, columns=df_columns)
# print(out_df)
# out_df.plot(x="year", y="frequency")
# plt.savefig('/Users/sarantuaa/Documents/content-analyze/graphs/economics_tendency.png') # Вставить свою ссылку graphs, но то, что идет после graphs оставить

# out_df = pd.DataFrame(social_tendency , columns=df_columns)
# print(out_df)
# out_df.plot(x="year", y="frequency")
# plt.savefig('/Users/sarantuaa/Documents/content-analyze/graphs/social_tendency.png') # Вставить свою ссылку graphs

# out_df = pd.DataFrame(foreign_tendency, columns=df_columns)
# print(out_df)
# out_df.plot(x="year", y="frequency")
# plt.savefig('/Users/sarantuaa/Documents/content-analyze/graphs/foreign_tendency.png') # Вставить свою ссылку graphs

# out_df = pd.DataFrame(ecology_tendency, columns=df_columns)
# print(out_df)
# out_df.plot(x="year", y="frequency")
# plt.savefig('/Users/sarantuaa/Documents/content-analyze/graphs/ecology_tendency.png') # Вставить свою ссылку graphs

# for file in os.listdir('/Users/sarantuaa/Documents/content-analyze/graphs'):
    
#     print("Открыт файл: " + file)
#     df = pd.read_csv('/Users/sarantuaa/Documents/content-analyze/graphs/' + file)
#     df.plot(x="year", y="frequency")
#     plt.savefig('/Users/sarantuaa/Documents/content-analyze/graphs/' + file[:file.find('.')] + '.png') # Вставить свою ссылку graphs