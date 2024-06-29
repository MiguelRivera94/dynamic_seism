import re

def center_window(currentWin, width=300, height=200):
    # get screen width and height
    screen_width = currentWin.winfo_screenwidth()
    screen_height = currentWin.winfo_screenheight()

    # calculate position x and y coordinates
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    currentWin.geometry('%dx%d+%d+%d' % (width, height, x, y))


def create_slug(text:str):
  """Creates a slug from text.

  Args:
    text: The text to create a slug from.

  Returns:
    A slug created from the text.
  """

  # Convert the text to lowercase.
  #text = text.lower()
  #text = re.sub(r"[\~áéíóúñÁÉÍÓÚÑ]", "", text)
  text = text.replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u').replace('Á','A').replace('É','E').replace('Í','I').replace('Ó','O').replace('Ú','U').replace('ñ','n').replace('Ñ','N')
  text = re.sub(r"[-()\"#/@;:<>{}`+=~|.!?,]", "", text)
  # Remove all punctuation characters.
  text = re.sub(r'[^\w\s]', '', text)

  # Replace all spaces with hyphens.
  text = text.replace(' ', '-')

  # Remove any duplicate hyphens.
  text = re.sub(r'--+', '-', text)

  return text    