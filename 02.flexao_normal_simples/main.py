import math
from subrotina import calculaSigmasd

## 1- Entrada de Dados

##Ler as propriedades do Materiais

propriedadesMateriais = {
  'fck': 70,
  'fyk': 500,
  'Es': 200
}

## Ler os coeficientes parciais de segurança

coeficientesSeguranca = {
  'gamac': 1.4,
  'gamas': 1.15,
  'gamaf': 1.4
}

## Ler o coeficiente de redistribuição de momentos

beta = 1

## Ler as dimensões da seção (cm)

dimensoesSecao = {
  'b': 15,
  'h': 40,
  'd': 36,
  'dLinha': 4
}

## Ler o momento fletor de serviço (kN.m)

Mk = 70

## 2 - Parâmetros do diagrama retangular para o concreto e profundidade da linha neutra
vlambda, alfac, eu, qsiLimite = None, None, None, None

if (propriedadesMateriais['fck'] <= 50):
  vlambda = 0.8
  alfac = 0.85
  eu = 3.5
  qsiLimite = 0.8 * beta - 0.35
else:
  vlambda = 0.8 - (((propriedadesMateriais['fck'] - 50)) / 400)
  alfac = 0.85 * ((1 - ((propriedadesMateriais['fck'] - 50)) / 200))
  eu = 2.6 + 35 * (((90 - propriedadesMateriais['fck']) / 100) ** 4)
  qsiLimite = 0.8 * beta - 0.45

## 3 - Conversão de unidades para kN e cm

Mk = Mk * 100
propriedadesMateriais['fck'] = propriedadesMateriais['fck'] / 10
propriedadesMateriais['fyk'] = propriedadesMateriais['fyk'] / 10
propriedadesMateriais['Es'] = propriedadesMateriais['Es'] * 100

## 4 - Resistências e momento de cálculo

fcd = propriedadesMateriais['fck'] / coeficientesSeguranca['gamac']
sigmacd = alfac * fcd
fyd = propriedadesMateriais['fyk'] / coeficientesSeguranca['gamas']
Md = coeficientesSeguranca['gamaf'] * Mk

## 5 - Parâmetros geométricos

delta = dimensoesSecao['dLinha'] / dimensoesSecao['d']

## 6 - Momento Limite

miLimite = vlambda * qsiLimite * (1 - 0.5 * vlambda * qsiLimite)

## 7 - Momento Reduzido Solicitante

mi = Md / (dimensoesSecao['b'] * (dimensoesSecao['d'] ** 2) * sigmacd)

## 8 - Solução com armadura simples

qsi, As, AsLinha, esLinha = None, None, None, None
if (mi <= miLimite):
  qsi = (1 - math.sqrt(1 - 2 * mi)) / vlambda
  As = vlambda * qsi * dimensoesSecao['b'] * dimensoesSecao['d'] * (sigmacd / fyd)
  AsLinha = 0

## Solução com armadura dupla
else:
  qsia = eu / (eu + 10)
  if(qsiLimite < qsia):
     raise Exception('Aumentar as dimensões da seção transversal')
  if(qsiLimite <= delta):
    raise Exception('Armadura de compressão está tracionada, aumente a dimensão da seção transversal')
  esLinha = eu * ((qsiLimite - delta) / qsiLimite)

  ## Chamar uma sibrotina para calcular a tensão sigmasdLinha
  sigmasdLinha = calculaSigmasd(propriedadesMateriais['Es'], esLinha, fyd)

  AsLinha = ((mi - miLimite) * dimensoesSecao['b'] * dimensoesSecao['d'] * sigmacd) / ((1 - delta) * sigmasdLinha)
  As = ((vlambda * qsiLimite) + ((mi - miLimite) / (1 - delta))) * dimensoesSecao['b'] * dimensoesSecao['d'] * (sigmacd / fyd)

## 10- Cálculo da armadura mínima
propriedadesMateriais['fck'] = propriedadesMateriais['fck'] * 10
fyd = fyd * 10

romin = None
if (propriedadesMateriais['fck'] <= 50):
  romin = (0.078 * (propriedadesMateriais['fck'] ** (2/3))) / fyd
else:
  romin = (0.5512 * math.log(1 + (0.11 * propriedadesMateriais['fck']))) / fyd

Asmin = None
if (romin < (0.15 / 100)):
  romin = 0.15 / 100

Asmin = romin * dimensoesSecao['b'] * dimensoesSecao['h']

if(As < Asmin):
  As = Asmin

print({
  'As': As,
  'AsLinha': AsLinha,
})








