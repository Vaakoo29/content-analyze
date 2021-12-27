from tika import parser 

raw = parser.from_file('strategies/Strategia_Danii.pdf')

content = raw['content']

count = 0

content = content.split()

for i in content:
    if i == 'ecology':
        count+=1

print(count)