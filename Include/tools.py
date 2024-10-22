import re

def center_window(currentWin, width=300, height=200):
    # Get the width and height of the screen to center a Dynamic Seism software window
    screen_width = currentWin.winfo_screenwidth()
    screen_height = currentWin.winfo_screenheight()

    # Calculate position to center the window
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    # Set the geometry (size and position) of the window
    currentWin.geometry('%dx%d+%d+%d' % (width, height, x, y))


def create_slug(text:str):
  """Creates a slug from text.

  Args:
    text: The text to create a slug from.

  Returns:
    A slug created from the text.
  """

  # Replace accented characters with their non-accented equivalents
  text = text.replace('Ñ','N').replace('Ú','U').replace('É','E').replace('Ó','O').replace('Á','A').replace('Í','I').replace('ú','u').replace('é','e').replace('ó','o').replace('á','a').replace('í','i').replace('ñ','n')
  # Remove special characters using regular expressions
  text = re.sub(r"[?{}-\"+=()/@;#<>|`~.!,:]", "", text)
  
  # Remove all non-alphanumeric characters except spaces
  text = re.sub(r'[^\w\s]', '', text)

  # Change spaces in text with hyphens
  text = text.replace(' ', '-')

  # Remove any consecutive hyphens
  text = re.sub(r'--+', '-', text)

  return text    