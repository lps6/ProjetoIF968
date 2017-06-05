import sys

TODO_FILE = 'todo.txt'
ARCHIVE_FILE = 'done.txt'

RED   = "\033[1;31m"  
BLUE  = "\033[1;34m"
CYAN  = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD    = "\033[;1m"
REVERSE = "\033[;7m"
YELLOW = "\033[0;33m"

ADICIONAR = 'a'
REMOVER = 'r'
FAZER = 'f'
PRIORIZAR = 'p'
LISTAR = 'l'

# Imprime texto com cores. Por exemplo, para imprimir "Oi mundo!" em vermelho, basta usar
#
# printCores('Oi mundo!', RED)
# printCores('Texto amarelo e negrito', YELLOW + BOLD)

def printCores(texto, cor) :
  print(cor + texto + RESET)
  

# Adiciona um compromisso à agenda. Um compromisso tem no mínimo
# uma descrição. Adicionalmente, pode ter, em caráter opcional, uma
# data (formato DDMMAAAA), um horário (formato HHMM), uma prioridade de A a Z, 
# um contexto onde a atividade será realizada (precedido pelo caractere
# '@') e um projeto do qual faz parte (precedido pelo caractere '+'). Esses
# itens opcionais são os elementos da tupla "extras", o segundo parâmetro da
# função.
#
# extras ~ (data, hora, prioridade, contexto, projeto)
#
# Qualquer elemento da tupla que contenha um string vazio ('') não
# deve ser levado em consideração. 
def adicionar(descricao, extras):
  data = '' 
  hora = ''
  pri = ''
  desc = ''
  contexto = ''
  projeto = ''
  # não é possível adicionar uma atividade que não possui descrição. 
  if descricao  == '' :
    return False
  else:
    desc = descricao
    for x in extras:
      if dataValida(x) == True:
        data = x
      elif horaValida(x) == True:
        hora = x       
      elif prioridadeValida(x) == True:
        pri = x       
      elif contextoValido(x) == True:
        contexto = x        
      elif projetoValido(x) == True:
        projeto = x
  
  novaAtividade = data+' '+hora+' '+pri+' '+desc+' '+contexto+' '+projeto
  novaAtividade = novaAtividade.strip()
  # Escreve no TODO_FILE. 
  try: 
    fp = open(TODO_FILE, 'a')
    fp.write(novaAtividade + "\n")
    fp.close()
  except IOError as err:
    print("Não foi possível escrever para o arquivo " + TODO_FILE)
    print(err)
    return False

  return True


# Valida a prioridade.
def prioridadeValida(pri):
  if len(pri) == 3 and pri[0] == '(' and pri[2] == ')':
    alphabet = ['A','B','C','D','E','F','G','H','I','J','K',"L","M","N","O","P","Q","R","S",'T',"U","V","W","","Y","Z"]
    for x in alphabet:
      letra = pri[1].upper()
      if letra == x :
        return True
  return False


# Valida a hora. Consideramos que o dia tem 24 horas, como no Brasil, ao invés
# de dois blocos de 12 (AM e PM), como nos EUA.
def horaValida(horaMin) :
  if len(horaMin) != 4 or not soDigitos(horaMin):
    return False
  else:
    if soDigitos(horaMin) == False:
      return False
    else:
      hora = int(horaMin[0]+horaMin[1])
      minute = int(horaMin[2]+horaMin[3])
      if hora < 0 or hora > 23:
        return False
      elif minute < 0 or minute > 59:
        return False
    return True

# Valida datas. Verificar inclusive se não estamos tentando
# colocar 31 dias em fevereiro. Não precisamos nos certificar, porém,
# de que um ano é bissexto. 
def dataValida(data) :
  if soDigitos(data) == True and len(data) == 8:
    dia = int(data[0]+data[1])
    mes = int(data[2]+data[3])
    ano = int(data[4]+data[5]+data[6]+data[7])
    mes31 = [1, 3, 5, 7, 8, 10, 12]
    mes30 = [4, 6, 9, 11]
    if dia < 0 or mes < 0 or ano < 0 or dia > 32 or mes > 12 or len(data) != 8:
      return False
    elif ((mes == 2) and (dia > 28)):
      return False
    for x in mes31:
      if mes == x:
        if dia > 31:
          return False
    for x in mes30:
      if mes == x:
        if dia > 30:
          return False
    else:
      return True 
  return False

# Valida que o string do projeto está no formato correto. 
def projetoValido(proj):
  if len(proj) > 1 and proj[0] == '+':
    return True
  return False

# Valida que o string do contexto está no formato correto. 
def contextoValido(cont):
  if len(cont) > 1 and cont[0] == '@':
    return True
  return False

# Valida que a data ou a hora contém apenas dígitos, desprezando espaços
# extras no início e no fim.
def soDigitos(numero) :
  if type(numero) != str :
    return False
  for x in numero :
    if x < '0' or x > '9' :
      return False
  return True


# Dadas as linhas de texto obtidas a partir do arquivo texto todo.txt, devolve
# uma lista de tuplas contendo os pedaços de cada linha, conforme o seguinte
# formato:
#
# (descrição, prioridade, (data, hora, contexto, projeto))
#
# É importante lembrar que linhas do arquivo todo.txt devem estar organizadas de acordo com o
# seguinte formato:
#
# DDMMAAAA HHMM (P) DESC @CONTEXT +PROJ
#
# Todos os itens menos DESC são opcionais. Se qualquer um deles estiver fora do formato, por exemplo,
# data que não tem todos os componentes ou prioridade com mais de um caractere (além dos parênteses),
# tudo que vier depois será considerado parte da descrição.  
def organizar(linhas):
  itens = []

  for l in linhas:
    data = '' 
    hora = ''
    pri = ''
    desc = ''
    contexto = ''
    projeto = ''
  
    l = l.strip() # remove espaços em branco e quebras de linha do começo e do fim
    tokens = l.split() # quebra o string em palavras

    # Processa os tokens um a um, verificando se são as partes da atividade.
    # Por exemplo, se o primeiro token é uma data válida, deve ser guardado
    # na variável data e posteriormente removido a lista de tokens. Feito isso,
    # é só repetir o processo verificando se o primeiro token é uma hora. Depois,
    # faz-se o mesmo para prioridade. Neste ponto, verifica-se os últimos tokens
    # para saber se são contexto e/ou projeto. Quando isso terminar, o que sobrar
    # corresponde à descrição. É só transformar a lista de tokens em um string e
    # construir a tupla com as informações disponíveis. 

    for x in tokens:
      if dataValida(x) == True:
        data = x
       # tokens.remove(x)
      elif horaValida(x) == True:
        hora = x
       # tokens.remove(x)
      elif prioridadeValida(x) == True:
        pri = x
       # tokens.remove(x)
      elif contextoValido(x) == True:
        contexto = x
        #tokens.remove(x)
      elif projetoValido(x) == True:
        projeto = x
        #tokens.remove(x)
      else:
        desc = desc + str(x) + ' '

    if desc != '':
      itens.append((desc, (data, hora, pri, contexto, projeto)))

  return itens


# Datas e horas são armazenadas nos formatos DDMMAAAA e HHMM, mas são exibidas
# como se espera (com os separadores apropridados). 
#
# Uma extensão possível é listar com base em diversos critérios: (i) atividades com certa prioridade;
# (ii) atividades a ser realizadas em certo contexto; (iii) atividades associadas com
# determinado projeto; (vi) atividades de determinado dia (data específica, hoje ou amanhã). Isso não
# é uma das tarefas básicas do projeto, porém. 

def listar():
  fp = open(TODO_FILE, 'r')
  lista = organizar(fp.readlines())
  ordenarPorDataHora(lista)
  ordenarPorPrioridade(lista)
  fp.close
 
  return lista

def formatoPrint(item):
  texto = str(item[1][0]+' '+item[1][1]+' '+item[1][2]+' '+item[0]+' '+item[1][3]+' '+item[1][4])
  texto = texto.strip()
  return texto

def esquemaCor(item):
  cor = YELLOW
  extras = item[1]
  for x in extras:    
    if prioridadeValida(x) == True:
      prioridade = x[1]
      if prioridade == 'A':
               cor = RED + BOLD
      elif prioridade == 'B':
               cor = CYAN
      elif prioridade == 'C':
               cor = BLUE
      elif prioridade == 'D':
               cor = GREEN
  return cor
              
               
def ordenarPorDataHora(itens):  
  for i in range(0, len(itens)-1):
       for j in range(0, len(itens)-1-i):
               if ano(itens[j]) > ano(itens[j + 1]):
                       itens[j], itens[j + 1] = itens[j + 1], itens[j]
               elif ano(itens[j]) == ano(itens[j + 1]) and mes(itens[j]) > mes(itens[j + 1]):
                       itens[j], itens[j + 1] = itens[j + 1], itens[j]
               elif ano(itens[j]) == ano(itens[j + 1]) and mes(itens[j]) == mes(itens[j + 1]) and dia(itens[j]) > dia(itens[j + 1]):
                       itens[j], itens[j + 1] = itens[j + 1], itens[j]
               elif ano(itens[j]) == ano(itens[j + 1]) and mes(itens[j]) == mes(itens[j + 1]) and dia(itens[j]) == dia(itens[j + 1]) and hora(itens[j]) > hora(itens[j + 1]):
                       itens[j], itens[j + 1] = itens[j + 1], itens[j]
               elif ano(itens[j]) == ano(itens[j + 1]) and mes(itens[j]) == mes(itens[j + 1]) and dia(itens[j]) == dia(itens[j + 1]) and hora(itens[j]) == hora(itens[j + 1]) and minuto(itens[j]) > minuto(itens[j + 1]) :
                       itens[j], itens[j + 1] = itens[j + 1], itens[j]
    
  return itens

#funções de data para comparação no bubblesort
def ano(item):
  for x in item[1]:
    if dataValida(x) == True:
      ano = int(x[4]+x[5]+x[6]+x[7])
      return ano
    else:
      return 8999

def dia(item):
  for x in item[1]:
    if dataValida(x) == True:
      dia = int(x[0]+x[1])
      return dia
    else:
      return 99

def mes(item):
  for x in item[1]:
    if dataValida(x) == True:
      mes = int(x[2]+x[3])
      return mes
    else:
      return 99

def hora(item):
   for x in item[1]:
    if horaValida(x) == True:
      hora = int(x[0]+x[1])
      return hora
    else:
      return 99

def minuto(item):
   for x in item[1]:
    if horaValida(x) == True:
      minuto = int(x[2]+x[3])
      return minuto
    else:
      return 99
   
def ordenarPorPrioridade(itens):
  for i in range(0, len(itens)-1):
        for j in range(0, len(itens)-1-i):
                if valorPrioridade(itens[ j ]) > valorPrioridade(itens[j + 1]):
                        itens[j], itens[j + 1] = itens[j + 1], itens[j]
  return itens

def valorPrioridade(item):
  alphabet = ['A','B','C','D','E','F','G','H','I','J','K',"L","M","N","O","P","Q","R","S",'T',"U","V","W","","Y","Z"]
  extras = item[1]
  valor = 99
  for x in extras:    
    if prioridadeValida(x) == True:
      prioridade = x[1]
      valor = 0
      for y in alphabet:        
        if y == prioridade:
          return valor
        else:
          valor = valor+1
  return valor

## NUM é o índice de cada elemento na lista resultante da função listar
def fazer(num):

  todo = listar()
  d = open(ARCHIVE_FILE, 'a+')
  d.write(formatoPrint(todo[num])+'\n')
  d.close
  todo.pop(num)
  t = open(TODO_FILE, 'w')
  for x in todo:
    t.write(formatoPrint(x)+'\n')
  t.close
  
  return 'Item marcado como feito!'

def remover(num):
  todo = listar()
  todo.pop(num)
  t = open(TODO_FILE, 'w')
  for x in todo:
    t.write(formatoPrint(x)+'\n')
  t.close

  return 'Item removido'

# prioridade é uma letra entre A a Z, onde A é a mais alta e Z a mais baixa.
# num é o número da atividade cuja prioridade se planeja modificar, conforme
# exibido pelo comando 'l'. 
def priorizar(num, prioridade):
  todo = listar()
  prioridade = prioridade.upper()
  oldItem = todo.pop(num)
  desc = oldItem[0]
  data = oldItem[1][0]
  hora = oldItem[1][1]
  pri = str('('+prioridade+')')
  contexto = oldItem[1][3]
  projeto = oldItem[1][4]
  todo.append((desc, (data, hora, pri, contexto, projeto)))
  t = open(TODO_FILE, 'w')
  for x in todo:
    t.write(formatoPrint(x)+'\n')
  t.close
  
  return 'Item Priorizado'



# Esta função processa os comandos e informações passados através da linha de comando e identifica
# que função do programa deve ser invocada. Por exemplo, se o comando 'adicionar' foi usado,
# isso significa que a função adicionar() deve ser invocada para registrar a nova atividade.
# O bloco principal fica responsável também por tirar espaços em branco no início e fim dos strings
# usando o método strip(). Além disso, realiza a validação de horas, datas, prioridades, contextos e
# projetos. 
def processarComandos(comandos) :
  if comandos[1] == ADICIONAR:
    comandos.pop(0) # remove 'agenda.py'
    comandos.pop(0) # remove 'adicionar'
    itemParaAdicionar = organizar([' '.join(comandos)])[0]
    # itemParaAdicionar = (descricao, prioridade, (data, hora, contexto, projeto))
    adicionar(itemParaAdicionar[0], itemParaAdicionar[1]) # novos itens não têm prioridade
  elif comandos[1] == LISTAR:
    lista = listar()
    i = 0
    while i < len(lista):
      item = str(i)+'.'+formatoPrint(lista[i])
      printCores(item, esquemaCor(lista[i]))
      i = i+1

  elif comandos[1] == REMOVER:
    comandos.pop(0) # remove 'agenda.py'
    comandos.pop(0) # remove 'remover'
    
    num = int(comandos[0])
    remover(num)
        

  elif comandos[1] == FAZER:
    comandos.pop(0) # remove 'agenda.py'
    comandos.pop(0) # remove 'fazer'
    
    num = int(comandos[0])
    fazer(num)

  elif comandos[1] == PRIORIZAR:
    comandos.pop(0) # remove 'agenda.py'
    comandos.pop(0) # remove 'priorizar'
    
    lista = comandos.split()
    priorizar(lista[0], lista[1])
    

  else :
    print("Comando inválido.")
    
  
# sys.argv é uma lista de strings onde o primeiro elemento é o nome do programa
# invocado a partir da linha de comando e os elementos restantes são tudo que
# foi fornecido em sequência. Por exemplo, se o programa foi invocado como
#
# python3 agenda.py a Mudar de nome.
#
# sys.argv terá como conteúdo
#
# ['agenda.py', 'a', 'Mudar', 'de', 'nome']

processarComandos(sys.argv)
