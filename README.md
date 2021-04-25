HOW TO USE:
    first of you download this file 
    img_to_str convert image to string using pytesseract 
    you have to download tesseract and pytesseract and neccessay modules that are imported(numpy,pillow,requests,io,beautifulsoup,base64)
    
    In webscraping.py you have to give your anna university register number and date of birth
    [REGISTER_NUMBER,DOB]

    for solving captcha, img_to_str file is used if the captcha detection was failure it will make the another request until 5 request

    we can change the trying request by changing the TRY value in web_scraping.py

    You can use my captcha trained data for tesseract by pasting captcha.traineddata to '/usr/share/tesseract/4.00/tessdata

    if you dont want my trained data you can remove lang='captcha' in 52-nd line of img_to_str.py as,
    text = pytesseract.image_to_string(out)[:6]

    you can run web_scraping.py you will get your result