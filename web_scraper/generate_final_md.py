import pandas as pd

def main():
    try:
        df = pd.read_csv('merged_articles_final.csv')
    except:
        print("Error: merged_articles_final.csv not found")
        return

    # Group by Column Name En
    # Expected markdown format:
    # ### Column Name 1
    # #### Title 1 (En)
    # ![Title 1 (Cn)](url)
    
    md_lines = []
    
    # Get duplicates check just in case
    # Print distinct columns
    columns = df['Column Name En'].unique()
    
    for col in columns:
        if pd.isna(col): continue
        
        md_lines.append(f"### {col}")
        
        # Get articles for this column
        articles = df[df['Column Name En'] == col]
        
        for _, row in articles.iterrows():
            title_en = row['Title En']
            title_cn = row['Title']
            url = row['Article URL']
            
            md_lines.append(f"#### {title_en}")
            md_lines.append(f"![{title_cn}]({url})")
            
        md_lines.append("") # Add space between columns

    with open('final_articles_report.md', 'w', encoding='utf-8') as f:
        f.write("\n".join(md_lines))
        
    print("Markdown report saved to final_articles_report.md")

if __name__ == "__main__":
    main()
