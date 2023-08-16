from PIL import Image

import pytesseract


bel = "/Users/yegorgrigoryev/Documents/PETS/money-project-bot/photo_ami.jpeg"
pol = "/Users/yegorgrigoryev/Documents/PETS/money-project-bot/photo.jpeg"
check = "/Users/yegorgrigoryev/Documents/PETS/money-project-bot/check.jpeg"

pytesseract.pytesseract.tesseract_cmd = (
    "/opt/homebrew/Cellar/tesseract/5.3.2/bin/tesseract"
)
# print(pytesseract.get_languages())
print(
    pytesseract.image_to_string(
        Image.open(check),
        lang="pol",
    )
)
