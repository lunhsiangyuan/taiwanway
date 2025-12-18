#!/usr/bin/env python3
"""
Generate a PDF report for the Sep-Nov 2025 Revenue Analysis.
Includes:
- Summary Table
- Total Revenue Plot
- Median Revenue Plot
"""
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.image as mpimg
from pathlib import Path

def generate_pdf_report():
    output_pdf = "analysis_output/revenue_report_sep_nov_2025.pdf"
    img_total_path = "analysis_output/revenue_hourly_total_sep_nov.png"
    img_median_path = "analysis_output/revenue_hourly_median_sep_nov.png"
    
    # Data for the table (hardcoded from previous analysis output for simplicity/reliability in this step)
    # In a production pipeline, we would pass this data or read it from a file.
    columns = ('Hour', 'Sep Total', 'Sep Avg', 'Sep Med', 
                       'Oct Total', 'Oct Avg', 'Oct Med', 
                       'Nov Total', 'Nov Avg', 'Nov Med')
    
    cell_text = [
        ["10:00", "$228", "$13", "$0", "$57", "$3", "$0", "$23", "$2", "$0"],
        ["11:00", "$1474", "$82", "$62", "$1583", "$93", "$74", "$1424", "$102", "$70"],
        ["12:00", "$2957", "$164", "$138", "$2985", "$176", "$152", "$2706", "$193", "$205"],
        ["13:00", "$2574", "$143", "$153", "$2059", "$121", "$95", "$1489", "$106", "$101"],
        ["14:00", "$1734", "$96", "$98", "$1638", "$96", "$75", "$1157", "$83", "$64"],
        ["15:00", "$1701", "$95", "$75", "$1344", "$79", "$69", "$1010", "$72", "$60"],
        ["16:00", "$1554", "$86", "$53", "$1543", "$91", "$73", "$958", "$68", "$57"],
        ["17:00", "$2424", "$135", "$134", "$2041", "$120", "$88", "$1622", "$116", "$101"],
        ["18:00", "$1830", "$102", "$87", "$1711", "$101", "$104", "$1092", "$78", "$67"],
        ["19:00", "$205", "$11", "$0", "$24", "$1", "$0", "$58", "$4", "$0"]
    ]

    with PdfPages(output_pdf) as pdf:
        # --- Page 1: Title and Table ---
        fig, ax = plt.subplots(figsize=(11.69, 8.27)) # A4 Landscape roughly
        ax.axis('tight')
        ax.axis('off')
        
        # Title
        plt.title("Revenue Analysis Report: Sep - Nov 2025", fontsize=20, y=0.95)
        
        # Table
        the_table = ax.table(cellText=cell_text, colLabels=columns, loc='center', cellLoc='center')
        the_table.auto_set_font_size(False)
        the_table.set_fontsize(10)
        the_table.scale(1.2, 1.5)
        
        pdf.savefig(fig, bbox_inches='tight')
        plt.close()

        # --- Page 2: Total Revenue Plot ---
        if Path(img_total_path).exists():
            fig, ax = plt.subplots(figsize=(11.69, 8.27))
            img = mpimg.imread(img_total_path)
            ax.imshow(img)
            ax.axis('off')
            plt.title("Total Revenue per Hour", fontsize=16)
            pdf.savefig(fig, bbox_inches='tight')
            plt.close()
        else:
            print(f"Warning: {img_total_path} not found.")

        # --- Page 3: Median Revenue Plot ---
        if Path(img_median_path).exists():
            fig, ax = plt.subplots(figsize=(11.69, 8.27))
            img = mpimg.imread(img_median_path)
            ax.imshow(img)
            ax.axis('off')
            plt.title("Median Daily Revenue per Hour", fontsize=16)
            pdf.savefig(fig, bbox_inches='tight')
            plt.close()
        else:
            print(f"Warning: {img_median_path} not found.")
            
    print(f"PDF Report generated at: {output_pdf}")

if __name__ == "__main__":
    generate_pdf_report()
