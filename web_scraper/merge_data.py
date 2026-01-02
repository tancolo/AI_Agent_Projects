import pandas as pd
from deep_translator import GoogleTranslator
import time

def translate_text(text):
    if not text or pd.isna(text) or text == "":
        return "Uncategorized"
    try:
        # Simple cache or check if already english? No, just translate.
        # But wait, Column Names might need consistent translation.
        # This is simple script.
        return GoogleTranslator(source='auto', target='en').translate(text)
    except Exception as e:
        print(f"Error translating '{text}': {e}")
        return text

def main():
    # 1. Read Data
    # Priority: Jianshu > Juejin > CSDN
    try:
        df_jianshu = pd.read_csv('jianshu_articles_data.csv')
        df_jianshu['Source'] = 'Jianshu'
    except:
        df_jianshu = pd.DataFrame()
        print("Warning: jianshu_articles_data.csv not found")

    try:
        df_juejin = pd.read_csv('juejin_articles_data.csv')
        df_juejin['Source'] = 'Juejin'
    except:
        df_juejin = pd.DataFrame()
        print("Warning: juejin_articles_data.csv not found")

    try:
        df_csdn = pd.read_csv('articles_data.csv')
        df_csdn['Source'] = 'CSDN'
    except:
        df_csdn = pd.DataFrame()
        print("Warning: articles_data.csv not found")

    # 2. Merge
    # Order matters for drop_duplicates keep='first'
    df_merged = pd.concat([df_jianshu, df_juejin, df_csdn], ignore_index=True)
    
    print(f"Total rows before dedup: {len(df_merged)}")

    # 3. Deduplicate
    # Removing duplicates based on 'Title'. Keeping first (Jianshu -> Juejin -> CSDN)
    df_clean = df_merged.drop_duplicates(subset=['Title'], keep='first')
    
    print(f"Total rows after dedup: {len(df_clean)}")

    # 4. Translate
    print("Translating Titles and Column Names...")
    
    # Titles
    df_clean['Title En'] = df_clean['Title'].apply(translate_text)
    
    # Column Names
    # Get unique columns to save calls
    unique_cols = df_clean['Column Name'].unique()
    col_map = {col: translate_text(col) for col in unique_cols}
    df_clean['Column Name En'] = df_clean['Column Name'].map(col_map)

    # 5. Sort
    df_clean = df_clean.sort_values(by=['Column Name En'])

    # 6. Save
    df_clean.to_csv('merged_articles_final.csv', index=False)
    print("Saved to merged_articles_final.csv")

if __name__ == "__main__":
    main()
