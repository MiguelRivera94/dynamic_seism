from pprint import pprint
def es_entero(cadena):
  # Logic to check if the user did not enter any data in the software
  if cadena == "":
      return False
  try:
    # Convert a string of characters to integers
    int(cadena)
    return True
  except ValueError:
    # Close the logic if there is an error when converting from string to integers
    return False
  
def es_flotante(cadena):
  # Logic to check if the user did not enter any data in the software
  if cadena == "":
      return False  
  try:
    # Convert a string of characters to floats
    float(cadena)
    return True
  except ValueError:
    # Close the logic if there is an error when converting from string to floats
    return False