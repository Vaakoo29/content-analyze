# новые библиотеки: pip install nltk
from tika import parser
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.stem import SnowballStemmer

stemmer = SnowballStemmer(language='russian')

# Словари для проверки определенных тендеций
economics = ['business', 'economic', 'economics', 'development', 'resources', 'exploitation', 'project', 'projects']
humans = ['human', 'humans', 'indigenous', 'people', 'peoples', 'rights', 'nation', 'nations', 'folk', 'folks', 'social', 'welfare', 'safety', 'education', 'educational']
politics = ['politics', 'cooperation', 'international', 'political', 'policy', 'management']
ecology = ['ecology', 'pollution', 'environment', 'climate', 'security', 'safety', 'science']

# economics_ru = ['бизнес', 'экономика', 'экономики', 'экономику', 'развитие', 'развития', 'ресурсы', 'ресурсов', 'освоение', 'освоения', 'проект', 'проекта', 'проекте', 'проекты', 'проектов']
# humans_ru = ['человек', 'люди', 'коренной', 'коренные', 'коренных', 'корреного', 'людей', 'права', 'нация', 'нации', 'социальный', 'социальная', 'социальную', 'безопасность', 'образование', 'образования', 'образовании', 'образовательный', 'образовательной', 'образовательного']
# politics_ru =['политика', 'политику', 'политики', 'сотрудничество', 'сотрудничества', 'международное', 'международный', 'международного', 'политический', 'политического', 'упрваление', 'упрваления']
# ecology_ru = ['экология', 'экологии', 'экологию', 'загрязнение', 'загрязнения', 'окружающая среда', 'окружающей среды', 'окружающую среду', 'климат', 'климата', 'изменение климата', 'охрана', 'охраны', 'охрану', 'безопасность', 'безопасности', 'наука', 'науки', 'науку']

economics_ru = {'бизнес':'бизнеса', 'экономик':'экономика', 'развит':'развитие', 'ресурс':'ресурсы', 'освоен':'освоение', 'проект':'проект'}
humans_ru = {'человек':'человек', 'люд':'люди', 'коренн':'корреной', 'прав':'права', 'нац':'нация', 'социальн':'социальный', 'безопасн':'безопасность', 'образован':'образование', 'образовательн':'образовательный'}
politics_ru ={'политик':'политика', 'сотрудничеств':'сотрудничество', 'международн':'международный', 'политическ':'политический', 'управлен':'управление'}
ecology_ru = {'эколог':'экология', 'загрязнен':'загрязнение', 'окружающая сред':'окружающая среда', 'климат':'климат', 'изменение климат':'изменение климата', 'охран':'охрана', 'безопасн':'безопасность', 'наук':'наука'}

tendencies = [economics, humans, politics, ecology]
tendencies_ru = [economics_ru, humans_ru, politics_ru, ecology_ru]

# Страны
countries = {'китай':'china', 'дания':'denmark', 'канада': 'canada', 'финляндия':'finland', 'исландия':'iceland', 'норвегия':'norway', 'швеция':'sweden', 'сша':'usa', 'россия':'russia'}

print("Cтраны, входящие в Арктический Союз: Канада, Китай, Дания, Финляндия, Исландия, Норвегия, Швеция, США, Россия")
country = input("Выберите страну: ")
country = countries[country.lower()]

raw = parser.from_file('strategies/' + country +'.pdf')

content = raw['content'].split()

df_columns = ['word', 'frequency']

if country == 'russia':

    for tendency in tendencies_ru:
        rows = []
        for word in tendency:
            rows.append({'word': word, 'frequency': content.count(word)})
    
        print(tendency)
        print(pd.DataFrame(rows, columns=df_columns))
        out_df = pd.DataFrame(rows, columns=df_columns)

    text = ''
    for i in content:

        stemmed_token = stemmer.stem(i)

        if stemmed_token in economics_ru.keys():
            text = text + economics_ru[stemmed_token] + ' '
        elif stemmed_token in ecology_ru.keys():
            text = text + ecology_ru[stemmed_token] + ' '
        elif stemmed_token in politics_ru.keys():
            text = text + politics_ru[stemmed_token] + ' '
        elif stemmed_token in humans_ru.keys():
            text = text + humans_ru[stemmed_token] + ' '

    cloud = WordCloud().generate(text)
    plt.imshow(cloud)
    plt.axis('off')
    plt.show()
    plt.close()

else:

    for tendency in tendencies:
        rows = []
        for word in tendency:
            rows.append({'word': word, 'frequency': content.count(word)})
    
        print(tendency)
        print(pd.DataFrame(rows, columns=df_columns))
        out_df = pd.DataFrame(rows, columns=df_columns)


    text = ''
    for i in content:
        if i in economics or i in ecology or i in politics or i in humans:
            text = text + i + ' '

    cloud = WordCloud().generate(text)
    plt.imshow(cloud)
    plt.axis('off')
    plt.show()
    plt.close()