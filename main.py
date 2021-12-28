from tika import parser
import pandas as pd

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
rows = []

for tendency in tendencies:
    for word in tendency:
        rows.append({'word': word, 'frequency': content.count(word)})
    
    print(tendency)
    out_df = pd.DataFrame(rows, columns=df_columns)
    print(out_df)