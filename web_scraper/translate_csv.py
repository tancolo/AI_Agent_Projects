import pandas as pd
from deep_translator import GoogleTranslator
import time

def translate_text(text):
    try:
        # Check if text is already mostly ascii/english to save time, but for safety translate all
        # If text is None or empty
        if not text or pd.isna(text):
            return ""
        
        # Simple cache or check could go here, but prompt is simple.
        # Use Google Translator
        translated = GoogleTranslator(source='auto', target='en').translate(text)
        return translated
    except Exception as e:
        print(f"Error translating '{text}': {e}")
        return text

def main():
    input_file = 'articles_data.csv'
    output_file = 'for_medium.csv'

    print(f"Reading {input_file}...")
    df = pd.read_csv(input_file)

    # Required columns: Title, Article URL, Column Name
    # Create new dataframe
    new_df = df[['Title', 'Article URL', 'Column Name']].copy()

    print("Translating Titles and Column Names (this may take a moment)...")
    
    # Translate Title
    # Using apply with a small delay to avoid hitting rate limits too fast if any
    new_df['Title'] = new_df['Title'].apply(lambda x: translate_text(x))
    
    # Translate Column Name
    new_df['Column Name'] = new_df['Column Name'].apply(lambda x: translate_text(x))

    print(f"Saving to {output_file}...")
    new_df.to_csv(output_file, index=False)
    print("Done!")

if __name__ == "__main__":
    main()
