from django.core.exceptions import ValidationError
import re
#Verifica se o CPF está no formato correto

def valida_CPF(cpf_original):
    if not(all(char.isdigit() or char == '.' or char == '-' for char in cpf_original)):
        return "CPF do pagador contém caractere inválido"
    
    # Valida CPF  803.767.152-12 
    try:
        numeros = cpf_original.split('.') #['803', '767', '152-12']
        dois_ultimos = numeros[-1].split('-') #['152', '12']
        numeros.pop() #Retira '152-12'
        lista_numeros_cpf = numeros + dois_ultimos #['803', '767', '152', '12']

    except ValidationError as e:
        return "CPF com formato inválido!"
    
    if len(lista_numeros_cpf) != 4:
            return "CPF com formato inválido!"
    for i in range(4):
        if i < 3 and len(lista_numeros_cpf[i]) != 3:
            return "CPF com formato inválido!"
        
        if i == 3 and len(lista_numeros_cpf[i]) != 2:
            return "CPF com formato inválido!"
    
    
    cpf = cpf_original.replace('.', '').replace('-', '')
    
    # Validação do 1º dígito de verificação
    soma = 0
    k = 0
    for i in range(10, 1, -1):
        soma += int(cpf[k]) * i
        k += 1
    
    soma *= 10
    resto = soma % 11
    if resto == 10:
        resto = 0
    if resto != int(cpf[-2]):
        return "CPF inválido!"
    
    # Validação do 2º dígito de verificação
    soma = 0
    k = 0
    for i in range(11, 1, -1):
        soma += int(cpf[k]) * i
        k += 1
    
    soma *= 10
    resto = soma % 11

    if resto == 10:
        resto = 0
    
    if resto != int(cpf[-1]):
        return "CPF inválido!"
    
    if len(set(cpf)) == 1:
        return "CPF inválido"
    
    return True 

#Verifica email no formato correto
def valida_email(email):
    padrao = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(padrao, email) is not None

def valida_numero(numero):
    return len(numero) == 11