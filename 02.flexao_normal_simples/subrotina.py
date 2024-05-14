def calculaSigmasd(Es, es, fyd):

  ## Trabalhar com o valor absoluto da deformação
  ess = abs(es)

  ## Deformação de escoamento de cálculo do aço
  eyd = fyd / Es

  ## Cálculo da tensão
  sigmasd = None
  if (ess < eyd):
    sigmasd = Es * ess
  else:
    sigmasd = fyd
  
  ##Acertando o sinal da tensão
  if (es < 0):
    sigmasd = - sigmasd

  return sigmasd
