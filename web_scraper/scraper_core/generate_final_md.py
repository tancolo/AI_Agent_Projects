import pandas as pd
import os

def main():
    # Robust path resolution
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    output_dir = os.path.join(project_root, 'scraper_output')

    try:
        input_path = os.path.join(output_dir, 'merged_articles_final.csv')
        df = pd.read_csv(input_path)
    except:
        print(f"Error: {input_path} not found")
        return

    # Group by Column Name En
    # Expected markdown format:
    # ### Column Name 1
    # #### Title 1 (En)
    # [Title 1 (Cn)](url)
    
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
            md_lines.append(f"[{title_cn}]({url})")
            
        md_lines.append("") # Add space between columns

    output_path = os.path.join(output_dir, 'final_articles_report.md')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(md_lines))
        
    print(f"Markdown report saved to {output_path}")

if __name__ == "__main__":
    main()
