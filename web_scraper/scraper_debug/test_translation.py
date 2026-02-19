from deep_translator import GoogleTranslator
import time

print("Testing translation...")
try:
    start = time.time()
    res = GoogleTranslator(source='auto', target='en').translate("你好，世界")
    end = time.time()
    print(f"Result: {res}")
    print(f"Time: {end - start:.2f}s")
except Exception as e:
    print(f"Error: {e}")
