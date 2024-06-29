from pprint import pprint
def es_entero(cadena):
  if cadena == "":
      return False
  try:
    int(cadena)
    return True
  except ValueError:
    return False
  
def es_flotante(cadena):
  if cadena == "":
      return False  
  try:
    float(cadena)
    return True
  except ValueError:
    return False