import pandas as pd
from deep_translator import GoogleTranslator
import time
import os
import socket
# Monkey-patch to force IPv4
old_getaddrinfo = socket.getaddrinfo
def new_getaddrinfo(*args, **kwargs):
    responses = old_getaddrinfo(*args, **kwargs)
    return [response for response in responses if response[0] == socket.AF_INET]
socket.getaddrinfo = new_getaddrinfo

# Manual mapping for Column Names
COLUMN_MAP = {
    "Android 5.0": "Android 5.0",
    "Android App": "Android App",
    "Android Studio": "Android Studio",
    "Android开发": "Android Development",
    "Git": "Git",
    "Java拾遗": "Java Review",
    "Mongodb": "Mongodb",
    "Uncategorized": "Uncategorized",
    "Web App": "Web App",
    "ZXing分析": "ZXing Analysis",
    "java拾遗": "Java Review",
    "函数式用心学": "Functional Programming Study",
    "函数式编程": "Functional Programming",
    "前端开发": "Frontend Development",
    "前端探索": "Frontend Exploration",
    "工具类Tips": "Tool Tips",
    "杂谈": "Miscellaneous",
    "视频教程": "Video Tutorials",
    "随笔": "Essays",
    "雕虫小技": "Small Tricks",
    "项目思考": "Project Reflections"
}

def translate_text(text, is_column=False):
    if not text or pd.isna(text) or text == "":
        return "Uncategorized"
    
    # 1. Check Manual Map first
    if is_column and text in COLUMN_MAP:
        return COLUMN_MAP[text]
        
    # 2. Try API with strict timeout
    try:
        # With IPv4 forced, this should be fast.
        return GoogleTranslator(source='auto', target='en').translate(text)
    except Exception as e:
        # print(f"Translation failed for '{text}': {e}")
        return text

def main():
    # Set global timeout for translation API
    import socket
    socket.setdefaulttimeout(3) # 3 seconds timeout
    
    # 1. Read Data
    # Priority: Jianshu > Juejin > CSDN
    try:
        df_jianshu = pd.read_csv(os.path.join('scraper_output', 'jianshu_articles_data.csv'))
        df_jianshu['Source'] = 'Jianshu'
    except:
        df_jianshu = pd.DataFrame()
        print("Warning: jianshu_articles_data.csv not found")

    try:
        df_juejin = pd.read_csv(os.path.join('scraper_output', 'juejin_articles_data.csv'))
        df_juejin['Source'] = 'Juejin'
    except:
        df_juejin = pd.DataFrame()
        print("Warning: juejin_articles_data.csv not found")

    try:
        df_csdn = pd.read_csv(os.path.join('scraper_output', 'csdn_articles_data.csv'))
        df_csdn['Source'] = 'CSDN'
    except:
        df_csdn = pd.DataFrame()
        print("Warning: csdn_articles_data.csv not found")

    # 2. Merge
    # Order matters for drop_duplicates keep='first'
    if df_jianshu.empty and df_juejin.empty and df_csdn.empty:
        print("No data found to merge.")
        return

    df_merged = pd.concat([df_jianshu, df_juejin, df_csdn], ignore_index=True)
    
    print(f"Total rows before dedup: {len(df_merged)}")

    # 3. Deduplicate
    # Removing duplicates based on 'Title'. Keeping first (Jianshu -> Juejin -> CSDN)
    df_clean = df_merged.drop_duplicates(subset=['Title'], keep='first')
    
    print(f"Total rows after dedup: {len(df_clean)}")

    # 4. Translate
    print("Translating Titles and Column Names...")
    
    # Titles
    print(f"Translating {len(df_clean)} titles...")
    titles_en = []
    for i, title in enumerate(df_clean['Title']):
        if (i + 1) % 10 == 0:
            print(f"Translating title {i + 1}/{len(df_clean)}")
        titles_en.append(translate_text(title, is_column=False))
    df_clean['Title En'] = titles_en
    
    # Column Names
    # Get unique columns to save calls
    unique_cols = df_clean['Column Name'].unique()
    print(f"Translating {len(unique_cols)} unique column names...")
    col_map = {}
    for i, col in enumerate(unique_cols):
        print(f"Translating column {i + 1}/{len(unique_cols)}: {col}")
        col_map[col] = translate_text(col, is_column=True)
    
    df_clean['Column Name En'] = df_clean['Column Name'].map(col_map)

    # 5. Sort
    df_clean = df_clean.sort_values(by=['Column Name En'])

    # 6. Save
    output_path = os.path.join('scraper_output', 'merged_articles_final.csv')
    df_clean.to_csv(output_path, index=False)
    print(f"Saved to {output_path}")

if __name__ == "__main__":
    main()
