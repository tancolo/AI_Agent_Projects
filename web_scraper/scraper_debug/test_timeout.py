from deep_translator import GoogleTranslator
import time
import socket

socket.setdefaulttimeout(5)

print("Testing translation with timeout...")
try:
    start = time.time()
    res = GoogleTranslator(source='auto', target='en').translate("你好，世界")
    end = time.time()
    print(f"Result: {res}")
    print(f"Time: {end - start:.2f}s")
except Exception as e:
    print(f"Error: {e}")
