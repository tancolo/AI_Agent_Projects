import subprocess
import sys
import time
import os

def run_script(script_name, description):
    print(f"\n{'='*50}")
    print(f"Starting: {description}")
    print(f"Script: {script_name}")
    print(f"{'='*50}")
    
    start_time = time.time()
    
    # Check if script exists
    if not os.path.exists(script_name):
        print(f"Error: Script {script_name} not found!")
        return False

    try:
        # Run the script and wait for it to complete
        result = subprocess.run([sys.executable, script_name], check=True)
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"\n{'-'*50}")
        print(f"Finished: {description}")
        print(f"Duration: {duration:.2f} seconds")
        print(f"Status: Success")
        print(f"{'-'*50}\n")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\n{'!'*50}")
        print(f"Error executing {script_name}")
        print(f"Exit code: {e.returncode}")
        print(f"{'!'*50}\n")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False

def main():
    print("Starting Web Scraper V0.2 Pipeline...")
    
    # Step 1: Scrape CSDN
    if not run_script(os.path.join("scraper_core", "csdn_scraper.py"), "Scraping CSDN Blog"):
        print("Pipeline aborted due to CSDN scraper failure.")
        return

    # Step 2: Scrape Jianshu
    if not run_script(os.path.join("scraper_core", "jianshu_scraper.py"), "Scraping Jianshu Blog"):
        print("Pipeline aborted due to Jianshu scraper failure.")
        return

    # Step 3: Scrape Juejin
    if not run_script(os.path.join("scraper_core", "juejin_scraper.py"), "Scraping Juejin Blog"):
        print("Pipeline aborted due to Juejin scraper failure.")
        return

    # Step 4: Merge Data
    if not run_script(os.path.join("scraper_core", "merge_articles_data.py"), "Merging, Deduplicating, Translating, and Sorting Data"):
        print("Pipeline aborted due to merge failure.")
        return

    # Step 5: Generate Final Report
    if not run_script(os.path.join("scraper_core", "generate_final_md.py"), "Generating Markdown Report"):
        print("Pipeline aborted due to report generation failure.")
        return

    print("\n" + "*"*50)
    print("Web Scraper V0.2 Pipeline Completed Successfully!")
    print("Output file: scraper_output/final_articles_report.md")
    print("*"*50)

if __name__ == "__main__":
    main()
