from langdetect import detect
respond = "hello, how are you?"
if detect(respond) in ["fa","ar"]:
    dir = "rtl"
else:   
    dir = "ltr"
print(respond)
print(dir)
print(detect(respond))