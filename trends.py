"""Visualizing Twitter Sentiment Across America"""

#run_doctests('nome_funcao') -> verifica se função está funcionando

#para verificar todas as funções de uma vez, rode o programa e digite no idle os seguintes comandos:
#import doctest
#doctest.testmod()


from data import word_sentiments, load_tweets
from datetime import datetime
from doctest import run_docstring_examples
from geo import us_states, geo_distance, make_position, longitude, latitude
from maps import draw_state, draw_name, draw_dot, wait, message
from string import ascii_letters
from ucb import main, trace, interact, log_current_line
import string #adicionado, de acordo com o PROBLEMA 3



# Phase 1: The Feelings in Tweets


def make_tweet(text, time, lat, lon):
    """Return a tweet, represented as a python dictionary.


    text      -- A string; the text of the tweet, all in lowercase
    time      -- A datetime object; the time that the tweet was posted
    latitude  -- A number; the latitude of the tweet's location
    longitude -- A number; the longitude of the tweet's location


    >>> t = make_tweet("just ate lunch", datetime(2012, 9, 24, 13), 38, 74)
    >>> tweet_words(t)
    ['just', 'ate', 'lunch']
    >>> tweet_time(t)
    datetime.datetime(2012, 9, 24, 13, 0)
    >>> p = tweet_location(t)
    >>> latitude(p)
    38
    """
    return {'text': text, 'time': time, 'latitude': lat, 'longitude': lon}
#lembrar: os tweets são gerados pela função "make_tweet"
#####PROBLEMA 1.1 ok
def tweet_words(tweet):
    """Return a list of the words in the text of a tweet."""
    "*** YOUR CODE HERE ***"
    return extract_words(tweet['text']) #Usa a função "extract_words" para pegar somente texto (sem pontuação)
                                        #do dicionário com índice 'text', acessando somente o texto do tweet


#####PROBLEMA 1.2 ok
def tweet_time(tweet):
    """Return the datetime that represents when the tweet was posted."""
    "*** YOUR CODE HERE ***"
    return tweet['time'] #acessa o índice "time" de Tweet. retorna com os atributos:
                            #datetime.datetime(year, month, day, hour, minute)


#####PROBLEMA 2 ok
def tweet_location(tweet):
    """Return a position (see geo.py) that represents the tweet's location."""
    "*** YOUR CODE HERE ***"
    return make_position(tweet['latitude'], tweet['longitude']) #usa a função make_position definida em geo.py
                    #acessa o índice 'latitude' e 'longitude' de Tweet


def tweet_string(tweet):
    """Return a string representing the tweet."""
    return '"{0}" @ {1}'.format(tweet['text'], tweet_location(tweet))


#####PROBLEMA 3 ok
def extract_words(text):
    """Return the words in a tweet, not including punctuation.
    >>> extract_words('anything else.....not my job')
    ['anything', 'else', 'not', 'my', 'job']
    >>> extract_words('i love my job. #winning')
    ['i', 'love', 'my', 'job', 'winning']
    >>> extract_words('make justin # 1 by tweeting #vma #justinbieber :)')
    ['make', 'justin', 'by', 'tweeting', 'vma', 'justinbieber']
    >>> extract_words("paperclips! they're so awesome, cool, & useful!")
    ['paperclips', 'they', 're', 'so', 'awesome', 'cool', 'useful']
    """
    "*** YOUR CODE HERE ***"
    '''
    return text.split()  # aqui está apenas retornando o texto de Tweet
                            # mas agr ele quer o texto sem caracter especial
    '''
    p = 0
    i = 0
    n = 0
    palavras_isoladas = text.split() #separa palavras que vieram em "text", ex.: 'oi, tudo bem?' -> ['oi,' , 'tudo', 'bem?']
    palavras_temp = []
    palavras_juntas = []
    while i < len(palavras_isoladas):   #a função deste while (e for) é substituir caracteres não presentes em acsii_letters por um espaço
        for x in palavras_isoladas[p]:  #usando o exemplo acima, ele ficaria ['oi_' , 'tudo', 'bem_'], em que o underscore (_) representa um espaço em branco
            if palavras_isoladas[p][n] in ascii_letters:
                palavras_temp.append(palavras_isoladas[p][n])
            else:
                palavras_temp.append(" ")
            n = n+1
        s = "".join(palavras_temp)  #just to mention: retorna em S a "rejunção" das palavras, fatiadas anteriormente com o uso de palavras_isoladas e palavras_temp
        palavras_juntas.append(s)
        p+=1
        i+=1
        n=0 #zerando n, s e palavras_temp -> variáveis e lista temporárias, apenas para controlar
        s= ""
        palavras_temp = []

    #tirando espaços dados por palavras_juntas e retornando as palavras em lista_nova, que conterá ['oi', 'tudo', 'bem']    
    lista_nova = []
    for x in palavras_juntas:
        x = x.split()
        lista_nova += x
    return lista_nova


#####PROBLEMA 4.1 ok
def make_sentiment(value):
    """Return a sentiment, which represents a value that may not exist. 


    >>> s = make_sentiment(0.2)
    >>> t = make_sentiment(None)
    >>> has_sentiment(s)
    True
    >>> has_sentiment(t)
    False
    >>> sentiment_value(s)
    0.2
    """
    assert value is None or (value >= -1 and value <= 1), 'Illegal value'  
     ##assert garante uma condição para continuar a execução do código.
     ##Caso a condição não seja atendida, uma exceção é disparada, e a execução é interrompida.
    "*** YOUR CODE HERE ***"
    '''
    if value != None or value == 0: #ou seja, se value estiver entre -1 e 1 ou for 0, retorne esse valor
        return value
    else:
        return None                 #senão, retorne None
    '''
    #estrutura acima foi descartada porque o "assert" já diz que "value" sera None ou >= -1 ^ <=1
    #basta retornar o value
    return value

   
#####PROBLEMA 4.2 ok
def has_sentiment(s):
    """Return whether sentiment s has a value.""" #retornar se tem valor (True) ou nao tem valor (False)
    "*** YOUR CODE HERE ***"
    if s == None:
       return False
    else:
        return True
    #função responsável apenas por verificar se no make_sentiment o 'value' é None
    #se sim, retorna False. Se não for == None, retorna que tem valor (que é True)


#####PROBLEMA 4.3 ok
def sentiment_value(s):
    """Return the value of a sentiment s."""
    assert has_sentiment(s), 'No sentiment value' 
    "*** YOUR CODE HERE ***"        
    return s
    #o proprio ASSERT verifica se tem valor. se não tiver, levanta erro
    #se tiver, somenet retorna S (que é o próprio valor do sentimento)
    #não precisa, portanto, verificar antes "if s != None: return s..."
        

def get_word_sentiment(word):
    """Return a sentiment representing the degree of positive or negative
    feeling in the given word, if word is not in the sentiment dictionary.


    >>> sentiment_value(get_word_sentiment('good'))
    0.875
    >>> sentiment_value(get_word_sentiment('bad'))
    -0.625
    >>> sentiment_value(get_word_sentiment('winning'))
    0.5
    >>> has_sentiment(get_word_sentiment('Berkeley'))
    False
    """
    return make_sentiment(word_sentiments.get(word, None))


#####PROBLEMA 5 ok
def analyze_tweet_sentiment(tweet):
    """ Return a sentiment representing the degree of positive or negative
    sentiment in the given tweet, averaging over all the words in the tweet
    that have a sentiment value.


    If no words in the tweet have a sentiment value, return
    make_sentiment(None).


    >>> positive = make_tweet('i love my job. #winning', None, 0, 0)
    >>> round(sentiment_value(analyze_tweet_sentiment(positive)), 5)
    0.29167
    >>> negative = make_tweet("Thinking, 'I hate my job'", None, 0, 0)
    >>> sentiment_value(analyze_tweet_sentiment(negative))
    -0.25
    >>> no_sentiment = make_tweet("Go bears!", None, 0, 0)
    >>> has_sentiment(analyze_tweet_sentiment(no_sentiment))
    False
    """
    average = make_sentiment(None)
    "*** YOUR CODE HERE ***"
    
    total_palavras_sentimento = 0
    soma = 0
    palavras_tweet = tweet_words(tweet) #atribuindo palavras do tweet nessa variável

    for palavra in palavras_tweet: #para cada palavra nas palavras do tweet
        if has_sentiment(get_word_sentiment(palavra)) == True: #se [[[tem_sentimento(devolve aqui valor do sentimento ou None{ai diz pra get_sentiment que ñ tem})]]] == True:
            soma += get_word_sentiment(palavra) #somo o valor desse sentimento em 'soma'
            total_palavras_sentimento += 1 #e para fazer a media corretamente, vejo quantas palavras têm sentimento (senão iria dividir pelo total de palavras, incluindo as sem sentimento)

    #necessário pôr essa última verificação para saber se há palavras com sentimentos. Caso contrário, retorna direto None
    if total_palavras_sentimento > 0 :  #ou seja, se existe ao menos uma palavra com sentimento (senão dividiria por 0)
        average = soma/total_palavras_sentimento #faz e retorna a média
        return average #aqui é a média do valor dos sentimentos
    else:
        return average  #se total_palavras_sentimento for == 0 (ñ tiver palavras com sentimento), retorna o None de cima (average = make_sentiment(None))


# Phase 2: The Geometry of Maps

#####PROBLEMA 6 ok
def find_centroid(polygon):
    """Find the centroid of a polygon.
    http://en.wikipedia.org/wiki/Centroid#Centroid_of_polygon
    polygon -- A list of positions, in which the first and last are the same
    Returns: 3 numbers; centroid latitude, centroid longitude, and polygon area
    Hint: If a polygon has 0 area, return its first position as its centroid
    >>> p1, p2, p3 = make_position(1, 2), make_position(3, 4), make_position(5, 0)
    >>> triangle = [p1, p2, p3, p1]  # First vertex is also the last vertex
    >>> find_centroid(triangle)
    (3.0, 2.0, 6.0)
    >>> find_centroid([p1, p3, p2, p1])
    (3.0, 2.0, 6.0)
    >>> find_centroid([p1, p2, p1])
    (1, 2, 0)
    """
    #p1 = make_position(1,2)  #a função make_position coloca nessa variável a lat e lon (lat sendo X num plano e lon sendo Y)
    #p2 = make_position(3,4)  #i.e: se chamássemos p2 depois da atribuição, teriamos p2 -> (3,4)
    #p3 = make_position(5,0)

    #triangulo = [p1, p2, p3, p1] #estamos atribuindo a esse polígono esses vértices. ficaria então:
                                #triangulo = [(1,2), (3,4), (5,0), (1,2)] #ATT: contamos 1,2 no final pq
                                                                        #o 1º vertice é tb o último vértice, e vice-versa
    #Usando a formula do centróide em 'triangulo', ele nos devolveria uma tupla com os respectivos valores: (x do centroide, y do centroide, area)
    #Exemplo:
        #find_centroid(triangulo) -> find_centroid([p1, p2, p3, p1]) == find_centroid([(1,2), (3,4), (5,0), (1,2)])
        #o output seria o dicio: (3.0, 2.0, 6.0)

    #-----------------------
    #FIRST THINGS FIRST:
    #para achar o centroide, primeiro é necessário achar a área (ambos dados por somatório):
        # area_basica = (x0*y1 - x1*y0) + (x1*y2 - x2*y1) + ... + (xi * yi+1  -  xi+1 * yi), em que xn e yn representam os vértices (xn, yn) == (lat, long)
        # area = area_basica/2

    #-----------------------
    #CÁLCULO EM SI DO CENTRÓIDE
    #com o valor da área, podemos então calcular o centroide (neste cálculo, encontraremos as coordenadas deste ponto)
    #logo, teremos um cálculo para o X do centroide e um cálculo para o Y do centroide
        #somatorio_vertice_x_centroide = (xi + xi+1) * (xi * yi+1  -  xi+1 * yi) + ... + ...
        #                     (xi + xi+1) * ---reaproveitar calculo feito na area---                  
        #vertice_x_centroide = centroide_basico_x/6*area
        

        #somatorio_vertice_y_centroide = (yi + yi+1) * (xi * yi+1  -  xi+1 * yi) + ... + ...
        #                     (yi + yi+1) * ---reaproveitar calculo feito na area---
        #vertice_y_centroide = centroide_basico_y/6*area

    #------ATENÇÃO!!!-------
        #verifique se o centroide tem area 0. se sim, retorne o dicio desta função como:
            #(x0, y0, 0), sendo respectivamente: (posicao_0_x, posicao_0_y, area)
    #------ATENÇÃO!!!-------
        #retorne a area com a função de valor absoluto 'abs(area)' (já no fim de todos os cálculos) para casos de área negativa (que tem o valor correto, dispensando o sinal)

    #passos:
        #calcular area
        #verificar se area é zero. if so, retornar o que foi especificado acima
        #se não for, continuar para o cálculo das coordenadas do centroide
        #retornar dicio com valores encontrados (centroide_x, centroide_y, abs(area))
    
    area = 0
    for elemento in polygon:
        index = polygon.index(elemento)+1
        area += elemento[0] * polygon[index][1] - polygon[index][0] * elemento[1]

        if index == len(polygon)-1:
            break
    area = area/2

    if area == 0:
        return (polygon[0][0], polygon[0][1], 0)
    else:
        i = 0
        somatorio_vertice_x_centroide = 0
        somatorio_vertice_y_centroide = 0
        for elemento in polygon:
            
            index = polygon.index(elemento)+1
            somatorio_vertice_x_centroide += (elemento[0] + polygon[index][0]) * (elemento[0] * polygon[index][1] - polygon[index][0] * elemento[1])
            somatorio_vertice_y_centroide += (elemento[1] + polygon[index][1]) * (elemento[0] * polygon[index][1] - polygon[index][0] * elemento[1])
            i += 1
            if i == len(polygon)-1:
                break
        vertice_x_centroide = (somatorio_vertice_x_centroide)/(6*area)
        vertice_y_centroide = (somatorio_vertice_y_centroide)/(6*area)
        return (vertice_x_centroide, vertice_y_centroide, abs(area))

       
#####PROBLEMA 7 ok
def find_center(polygons):
    """Compute the geographic center of a state, averaged over its polygons.


    The center is the average position of centroids of the polygons in polygons,
    weighted by the area of those polygons.


    Arguments:
    polygons -- a list of polygons


    >>> ca = find_center(us_states['CA'])  # California
    >>> round(latitude(ca), 5)
    37.25389
    >>> round(longitude(ca), 5)
    -119.61439


    >>> hi = find_center(us_states['HI'])  # Hawaii
    >>> round(latitude(hi), 5)
    20.1489
    >>> round(longitude(hi), 5)
    -156.21763
    """
    #diferença desta para a anterior é que esta devolve centroide de uma coleção de poligonos
    #obtida por decomposição geométrica (utilizando media poderada)
    #ex: há dois polígonos de coordenadas
        #P1=[(1,2),(3,4),(5,0),(1,2)]
        #P2=[(5,6),(7,8),(9,0),(5,6)]
            #ao aplicar find_centroid(P1 & P2) receberíamos:
            #CentroideP1=(3.0, 2.0, 6.0) -> 3 e 2 são X e Y do centroide, 6 a área
            #CentroideP2= (7.0, 4.6, 10.0) -> 7 e 4.6 são X e Y do centroide, 10 a área

            #find_center faria: (x = latitude, y = longitude)
                        #x de todas essas formas = (xP1*areaP1)+(xP2*areaP2) / (areaP1 + areaP2)
                                        #x_formas = (3*6)+(7*10)/(6+10) = 5.5
                        #y de todas essas formas = (yP1*areaP1)+(yP2*areaP2) / (areaP1 + areaP2)
                                        #y_formas = (2*6)+(4.6*10)/(6+10) = 3.6
                        #o resultado significa as coordenadas do centroide deste conjunto de poligonos:
                        #coordenadas_formas = (x_formas, y_formas) == (5.5, 3.6)

    "*** YOUR CODE HERE ***"
    lista_xs = []
    lista_ys = []
    soma_media = 0
    for poligono in polygons: #pega vertices dos poligonos listados em 'polygons'
        centroide = find_centroid(poligono) #calcula seu centroide (com a formula desenvolvida na função acima)

        x = centroide[0]*centroide[2]   #multiplica o X com a área (pois faz-se média ponderada)
        lista_xs.append(x)              #anexa esse valor a uma lista

        y = centroide[1]*centroide[2]   #agora multiplica o Y com a área
        lista_ys.append(y)              #anexa o valor achado à lista com todos os 'Y*área'

        soma_media += centroide[2]      #acumula áreas encontradas para posteriormente serem divisores (faz-se média ponderada)

    xs = 0 #armazena a soma dos elementos contidos na lista aqui, em xs
    for x in lista_xs:  #percorrerá a lista com todos os valores de x*área gerados, somando-os
        xs += x
    ys = 0 #armazena a soma dos elementos contidos na lista aqui, em ys
    for y in lista_ys:  #mesmo caso de cima, mas somando todos os y*área gerados
        ys += y

    x_poligonos = (xs)/(soma_media) #coordenada X (latitude) do centroide do novo poligono (polígono de poligonos)
    y_poligonos = (ys)/(soma_media) #coordenada Y (longitude do centroide do novo poligono (polígono de poligonos)
    return(x_poligonos, y_poligonos)
        
        
        


# Phase 3: The Mood of the Nation

#####PROBLEMA 8 ok
def find_closest_state(tweet, state_centers):
    """Return the name of the state closest to the given tweet's location.


    Use the geo_distance function (already provided) to calculate distance
    in miles between two latitude-longitude positions.


    Arguments:
    tweet -- a tweet abstract data type
    state_centers -- a dictionary from state names to positions.


    >>> us_centers = {n: find_center(s) for n, s in us_states.items()}
    >>> sf = make_tweet("Welcome to San Francisco", None, 38, -122)
    >>> ny = make_tweet("Welcome to New York", None, 41, -74)
    >>> find_closest_state(sf, us_centers)
    'CA'
    >>> find_closest_state(ny, us_centers)
    'NJ'
    """
    "*** YOUR CODE HERE ***"
    
    lista_distancias = []
    for x in state_centers:
        distancia = geo_distance(tweet_location(tweet), state_centers[x]) #atribui a 'distancia' a distancia entre as coordenadas do tweet e de cada estado analisado pelo for
        lista_distancias.append((distancia, x)) #coloca esse valor numa lista 
    lista_distancias.sort() #após inserir todas as distancias entre o tweet_location e todos os estados americanos, dá um sort na lista
    menor_distancia = lista_distancias.pop(0) #retira o primeiro elemento (de índice 0), que consequentemente é o de menor valor (menor distância)
    return menor_distancia[1] #retorna da variavel 'menor_distancia' o elemento de índice 1 (que corresponde ao estado, como atribuido anteriormente) ex: [(270, 'ca')]
    
#####PROBLEMA 9 ok
def group_tweets_by_state(tweets): #alocar tweets correspostendentes a cada estado em sua devida key no dicionário
    """Return a dictionary that aggregates tweets by their nearest state center.


    The keys of the returned dictionary are state names, and the values are
    lists of tweets that appear closer to that state center than any other.


    tweets -- a sequence of tweet abstract data types


    >>> sf = make_tweet("Welcome to San Francisco", None, 38, -122)
    >>> ny = make_tweet("Welcome to New York", None, 41, -74)
    >>> ca_tweets = group_tweets_by_state([sf, ny])['CA']
    >>> tweet_string(ca_tweets[0])
    '"Welcome to San Francisco" @ (38, -122)'
    """
    tweets_by_state = {} #inicia como um dicionário vazio
    "*** YOUR CODE HERE ***"
    centros = {x: find_center(y) for x, y in us_states.items()}
    #o dicionario acima é responsável por armazenar o centroide do poligono de poligonos que compõem um dado estado (cada x representa um estado)
    #e o Y retorna a sigla correspondente ao estado com esse centroide
    #X é a chave e Y o valor

    for z in us_states:
        tweets_by_state[z] = [] #cria-se as chaves dos dicionários
        
    for tw in tweets: #analisaremos agora cada tweet armazenado em 'tweets'
        localizacao = find_closest_state(tw, centros) #atribui a 'localizacao' qual estado é o mais proximo (ex: 'ca'), usando a função 'find_clo...', que pega
                                                                                                       #o tweet (e sua lat & lon) e compara com a menor distancia entre
                                                                                                        #ele e o centro de estado mais próximo (verificar função acima)
        tweets_by_state[localizacao].append(tw) #anexa o tweet a sua chave correspondente (ao seu estado correspondente)
                
    return tweets_by_state


#####PROBLEMA 10 ok
def most_talkative_state(term):
    """Return the state that has the largest number of tweets containing term.


    >>> most_talkative_state('texas')
    'TX'
    >>> most_talkative_state('sandwich')
    'NJ'
    """
    tweets = load_tweets(make_tweet, term)  # A list of tweets containing term
    "*** YOUR CODE HERE ***"

    tweets_by_state = group_tweets_by_state(tweets) #atribui a essa variavel o que fizemos no problema anterior
    maximo = 0
    
    for x in tweets_by_state: #tweets_by_state contem todos os estados e seus respectivos tweets
        if len(tweets_by_state[x]) > maximo: #faz atividade abaixo se o tamanho (quantidade de tweets) para estado X for maior que o maximo (inicia como 0)
            maximo = len(tweets_by_state[x]) #atualiza-se o maximo para o tamanho da quantidade de tweets no estado que mais se citou o termo
            estado_mais_termos = x #e logo depois retorna qual estado foi esse (x)

    return estado_mais_termos #após o fim de todas as iterações do for, retorna o estado 


    
    

#####PROBLEMA 11 ok
def average_sentiments(tweets_by_state):
    """Calculate the average sentiment of the states by averaging over all
    the tweets from each state. Return the result as a dictionary from state
    names to average sentiment values (numbers).


    If a state has no tweets with sentiment values, leave it out of the
    dictionary entirely.  Do NOT include states with no tweets, or with tweets
    that have no sentiment, as 0.  0 represents neutral sentiment, not unknown
    sentiment.


    tweets_by_state -- A dictionary from state names to lists of tweets
    """
    averaged_state_sentiments = {}
    "*** YOUR CODE HERE ***"
    for x in tweets_by_state: #para cada elemento (estado) em tweets_by_state (dicionário)
        contador = 0
        valor_total_sentimentos = 0
        for n in tweets_by_state[x]: #para cada tweet nesse estado
            aleatorio = 0 #essa varivael serve apenas para caso o estado não tenha tweets com valor de sentimento
                        #O problema pede para não adicioná-lo ao dicionário (ñ atribuir 0, pois 0 significa sentimento neutro)
                        # e o cinza representa sentimento desconhecido
            if has_sentiment(analyze_tweet_sentiment(n)) == False:
                aleatorio +=1  
            else: #se tiver sentimento relacionado (ou seja, valor sentimento != 0)
                valor_total_sentimentos = valor_total_sentimentos + analyze_tweet_sentiment(n) #adicione o valor deste sentimento em 'valor_total_sentimentos'
                contador +=1 #para dividir pelo número correto de elementos levados em conta
                averaged_state_sentiments[x] = (valor_total_sentimentos)/(contador) #para estado X, atribuir valor médio e armazenar em averaged_state_sentiments
    return averaged_state_sentiments




# Phase 4: Into the Fourth Dimension

#####PROBLEMA 12 ok
def group_tweets_by_hour(tweets):
    """Return a dictionary that groups tweets by the hour they were posted.


    The keys of the returned dictionary are the integers 0 through 23.


    The values are lists of tweets, where tweets_by_hour[i] is the list of all
    tweets that were posted between hour i and hour i + 1. Hour 0 refers to
    midnight, while hour 23 refers to 11:00PM.


    To get started, read the Python Library documentation for datetime objects:
    http://docs.python.org/py3k/library/datetime.html#datetime.datetime


    tweets -- A list of tweets to be grouped
    """
    tweets_by_hour = {}
    "*** YOUR CODE HERE ***"

    for n in range(24):
        tweets_by_hour[n] = [] #criando as chaves no dicionario, pois dava erro anteriormente da forma que eu estava fazendo: KeyError: 19

    for x in tweets:    #percorrendo os tweets
        horario = tweet_time(x).hour #lembrar oq a função tweet_time faz (Return the datetime that represents when the tweet was posted)
                                                #neste caso acima nós pegamos em tweet_time do (tweet) apenas a .hour (pois ficará
                                                #armazenado no dicionario de acordo com as horas). No objeto datetime temos os seguintes elementos:
                                                #(year, month, day, hour=0, minute=0, second=0, microsecond=0, tzinfo=None)
        tweets_by_hour[horario].append(x) #no dicio 'tweets_by_hour', na chave [horario], adicionar o (tweet)
            
    return tweets_by_hour




# Interaction.  You don't need to read this section of the program.


def print_sentiment(text='Are you virtuous or verminous?'):
    """Print the words in text, annotated by their sentiment scores."""
    words = extract_words(text.lower())
    assert words, 'No words extracted from "' + text + '"'
    layout = '{0:>' + str(len(max(words, key=len))) + '}: {1:+}'
    for word in extract_words(text.lower()):
        s = get_word_sentiment(word)
        if has_sentiment(s):
            print(layout.format(word, sentiment_value(s)))


def draw_centered_map(center_state='TX', n=10):
    """Draw the n states closest to center_state."""
    us_centers = {n: find_center(s) for n, s in us_states.items()}
    center = us_centers[center_state.upper()]
    dist_from_center = lambda name: geo_distance(center, us_centers[name])
    for name in sorted(us_states.keys(), key=dist_from_center)[:int(n)]:
        draw_state(us_states[name])
        draw_name(name, us_centers[name])
    draw_dot(center, 1, 10)  # Mark the center state with a red dot
    wait()


def draw_state_sentiments(state_sentiments={}):
    """Draw all U.S. states in colors corresponding to their sentiment value.


    Unknown state names are ignored; states without values are colored grey.


    state_sentiments -- A dictionary from state strings to sentiment values
    """
    for name, shapes in us_states.items():
        sentiment = state_sentiments.get(name, None)
        draw_state(shapes, sentiment)
    for name, shapes in us_states.items():
        center = find_center(shapes)
        if center is not None:
            draw_name(name, center)


def draw_map_for_term(term='my job'):
    """Draw the sentiment map corresponding to the tweets that contain term.


    Some term suggestions:
    New York, Texas, sandwich, my life, justinbieber
    """
    tweets = load_tweets(make_tweet, term)
    tweets_by_state = group_tweets_by_state(tweets)
    state_sentiments = average_sentiments(tweets_by_state)
    draw_state_sentiments(state_sentiments)
    for tweet in tweets:
        s = analyze_tweet_sentiment(tweet)
        if has_sentiment(s):
            draw_dot(tweet_location(tweet), sentiment_value(s))
    wait()


def draw_map_by_hour(term='my job', pause=0.5):
    """Draw the sentiment map for tweets that match term, for each hour."""
    tweets = load_tweets(make_tweet, term)
    tweets_by_hour = group_tweets_by_hour(tweets)


    for hour in range(24):
        current_tweets = tweets_by_hour.get(hour, [])
        tweets_by_state = group_tweets_by_state(current_tweets)
        state_sentiments = average_sentiments(tweets_by_state)
        draw_state_sentiments(state_sentiments)
        message("{0:02}:00-{0:02}:59".format(hour))
        wait(pause)


def run_doctests(names):
    """Run verbose doctests for all functions in space-separated names."""
    g = globals()
    errors = []
    for name in names.split():
        if name not in g:
            print("No function named " + name)
        else:
            if run_docstring_examples(g[name], g, True) is not None:
                errors.append(name)
    if len(errors) == 0:
        print("Test passed.")
    else:
        print("Error(s) found in: " + ', '.join(errors))


@main
def run(*args):
    """Read command-line arguments and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Run Trends")
    parser.add_argument('--print_sentiment', '-p', action='store_true')
    parser.add_argument('--run_doctests', '-t', action='store_true')
    parser.add_argument('--draw_centered_map', '-d', action='store_true')
    parser.add_argument('--draw_map_for_term', '-m', action='store_true')
    parser.add_argument('--draw_map_by_hour', '-b', action='store_true')
    parser.add_argument('text', metavar='T', type=str, nargs='*',
                        help='Text to process')
    args = parser.parse_args()
    for name, execute in args.__dict__.items():
        if name != 'text' and execute:
            globals()[name](' '.join(args.text))






