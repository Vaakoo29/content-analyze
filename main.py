from tika import parser
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Словари для проверки определенных тендеций
economics = ['business', 'economic', 'economics', 'development', 'resources', 'exploitation', 'project', 'projects']
humans = ['human', 'humans', 'indigenous', 'people', 'peoples', 'rights', 'nation', 'nations', 'folk', 'folks', 'social', 'welfare', 'safety', 'education', 'educational']
politics = ['politics', 'cooperation', 'international', 'political', 'policy', 'management']
ecology = ['ecology', 'pollution', 'environment', 'climate', 'security', 'safety', 'science']

tendencies = [economics, humans, politics, ecology]

# Страны
countries = {'китай':'china', 'дания':'denmark', 'канада': 'canada', 'финляндия':'finland', 'iceland':'исландия', 'норвегия':'norway', 'швеция':'sweden', 'сша':'usa', 'россия':'russia'}

print("Cтраны, входящие в Арктический Союз: Канада, Китай, Дания, Финляндия, Исландия, Норвегия, Швеция, США, Россия")
country = input("Выберите страну: ")
country = countries[country.lower()]

raw = parser.from_file('strategies/' + country +'.pdf')
content = raw['content'].split()

df_columns = ['word', 'frequency']

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