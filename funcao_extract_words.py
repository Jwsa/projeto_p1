from string import ascii_letters
import string #adicionado, de acordo com o PROBLEMA 3

text = input('digite aqui: ')
def extract_words(text):
    p = 0
    i = 0
    n = 0
    palavras_isoladas = text.split()
    palavras_temp = []
    palavras_juntas = []
    palavras_resultado = []
    while i < len(palavras_isoladas):
        for x in palavras_isoladas[p]:
            if palavras_isoladas[p][n] in ascii_letters:
                palavras_temp.append(palavras_isoladas[p][n])
            else:
                palavras_temp.append(" ")
            n = n+1
        s = "".join(palavras_temp)
        palavras_juntas.append(s)
        p+=1
        i+=1
        n=0
        s= ""
        palavras_temp = []
        return palavras_juntas
print(extract_words(text))
