import pandas as pd
from deep_translator import GoogleTranslator
import time

def translate_text(text):
    try:
        if not text or pd.isna(text):
            return ""
        translated = GoogleTranslator(source='auto', target='en').translate(text)
        return translated
    except Exception as e:
        print(f"Error translating '{text}': {e}")
        return text

def main():
    input_file = 'articles_data.csv'
    output_file = 'articles_report_sorted.md'

    print(f"Reading {input_file}...")
    df = pd.read_csv(input_file)

    # We need: Title (CN), Title (EN), URL, Column (EN for sorting)
    
    print("Translating Columns for sorting (this may take a moment)...")
    # Translate Column Name first for sorting
    df['Column Name En'] = df['Column Name'].apply(lambda x: translate_text(x))
    
    # Sort by English Column Name
    df = df.sort_values(by='Column Name En', na_position='last')
    
    print("Translating Titles and generating markdown...")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        # Iterate through the sorted dataframe
        # To avoid re-translating everything if we run multiple times, 
        # or just simply process row by row.
        
        count = 0
        total = len(df)
        
        for index, row in df.iterrows():
            cn_title = row['Title']
            url = row['Article URL']
            
            # Translate Title to English
            en_title = translate_text(cn_title)
            
            # Write to markdown matching new sample format:
            # ### Column Name
            # #### Title of the article (in English)
            # ![Title of the article (in Chinese)](Article URL)
            
            column_en = row['Column Name En']
            
            f.write(f"### {column_en}\n")
            f.write(f"#### {en_title}\n")
            f.write(f"![{cn_title}]({url})\n\n")
            
            count += 1
            if count % 5 == 0:
                print(f"Processed {count}/{total} articles...")
                
    print(f"Done! Saved to {output_file}")

if __name__ == "__main__":
    main()
