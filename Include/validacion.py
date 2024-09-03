from pprint import pprint
def es_entero(cadena):
  # Check if the input string is empty
  if cadena == "":
      return False
  try:
    # Attempt to convert the string to an integer
    int(cadena)
    return True
  except ValueError:
    # Return False if conversion to integer raises a ValueError
    return False
  
def es_flotante(cadena):
  # Check if the input string is empty
  if cadena == "":
      return False  
  try:
    # Attempt to convert the string to a float
    float(cadena)
    return True
  except ValueError:
    # Return False if conversion to float raises a ValueError
    return False