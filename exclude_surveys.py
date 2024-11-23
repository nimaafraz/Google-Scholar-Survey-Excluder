import csv
import re
import pandas as pd
from bs4 import BeautifulSoup
from tabulate import tabulate


def get_researcher_name(input_html):
    """
    Extracts the researcher's name from the HTML title tag.
    """
    with open(input_html, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")
    
    # Extract the title and parse the name
    title = soup.title.string if soup.title else "Unknown"
    name = title.split(" - ")[0].strip() if " - " in title else title.strip()
    return name


def parse_html_to_csv(input_html, output_csv):
    """
    Parses a Google Scholar HTML file into a CSV with columns:
    Title, Authors, Venue, Citation, Year.
    """
    with open(input_html, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    data = []

    # Locate the table containing the papers
    table = soup.find("table", {"id": "gsc_a_t"})  # Match the table ID
    if not table:
        raise ValueError("No table with ID 'gsc_a_t' found in the HTML.")

    for row in table.find_all("tr", {"class": "gsc_a_tr"}):  # Match paper rows
        try:
            # Extract Title
            title_cell = row.find("a", {"class": "gsc_a_at"})
            title = title_cell.get_text(strip=True) if title_cell else "N/A"

            # Extract Authors and Venue (combined in one cell)
            metadata_cell = row.find("div", {"class": "gs_gray"})
            metadata = metadata_cell.get_text(strip=True) if metadata_cell else "N/A"
            authors, venue = metadata.split(" - ") if " - " in metadata else (metadata, "N/A")

            # Extract Citation Count
            citation_cell = row.find("a", {"class": "gsc_a_ac"})
            citation = int(citation_cell.get_text(strip=True)) if citation_cell and citation_cell.get_text(strip=True).isdigit() else 0

            # Extract Year
            year_cell = row.find("span", {"class": "gsc_a_h"})
            year = int(year_cell.get_text(strip=True)) if year_cell and year_cell.get_text(strip=True).isdigit() else "N/A"

            # Append the data
            data.append([title, authors, venue, citation, year])
        except Exception as e:
            print(f"Error processing row: {e}")

    # Save data to CSV
    with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["Title", "Authors", "Venue", "Citation", "Year"])
        csvwriter.writerows(data)

    print(f"CSV file '{output_csv}' has been created with {len(data)} papers.")


def calculate_indices(df):
    """
    Calculates h-index and i10-index from a DataFrame containing citations.
    """
    citations = df['Citation'].sort_values(ascending=False).values
    h_index = sum(c >= (i + 1) for i, c in enumerate(citations))
    i10_index = sum(c >= 10 for c in citations)
    return h_index, i10_index


def exclude_survey_papers(input_csv, output_csv):
    """
    Excludes survey papers from a CSV and computes statistics comparing 
    total citations, h-index, and i10-index before and after exclusion.
    """
    survey_keywords = ["survey", "review", "directions", "challenges",
                       "trends", "approaches", "opportunities", "concepts", "roadmap", "Advances in", "Analysis of"]

    df = pd.read_csv(input_csv)
    is_survey = df['Title'].str.contains('|'.join(survey_keywords), case=False, na=False)
    survey_papers = df[is_survey]
    non_survey_papers = df[~is_survey]
    non_survey_papers.to_csv(output_csv, index=False)

    total_papers = len(df)
    excluded_papers = len(survey_papers)
    excluded_citations = survey_papers['Citation'].sum()
    total_citations = df['Citation'].sum()

    percent_excluded_papers = (excluded_papers / total_papers) * 100 if total_papers > 0 else 0
    percent_excluded_citations = (excluded_citations / total_citations) * 100 if total_citations > 0 else 0

    # Compute indices
    total_h_index, total_i10_index = calculate_indices(df)
    non_survey_h_index, non_survey_i10_index = calculate_indices(non_survey_papers)

    # Print statistics
    print(f"Number of papers excluded: {excluded_papers}")
    print(f"Percentage of papers excluded as survey: {percent_excluded_papers:.2f}%")
    print(f"Percentage of excluded citations compared to total: {percent_excluded_citations:.2f}%")

    # Create and print comparison table
    comparison_data = [
        ["Total Papers", total_papers, len(non_survey_papers)],
        ["Total Citations", total_citations, total_citations - excluded_citations],
        ["H-Index", total_h_index, non_survey_h_index],
        ["i10-Index", total_i10_index, non_survey_i10_index],
    ]
    print("\nComparison Table:")
    print(tabulate(comparison_data, headers=["Metric", "With Surveys", "Without Surveys"], tablefmt="grid"))


# Example usage
input_html = 'papers.html'
intermediate_csv = 'GScholar-profile.csv'
output_csv = 'Non-Survey-Papers.csv'

# Step 1: Get researcher name
researcher_name = get_researcher_name(input_html)
print(f"Researcher Name: {researcher_name}")

# Step 2: Parse HTML to CSV
parse_html_to_csv(input_html, intermediate_csv)

# Step 3: Exclude survey papers and display results
exclude_survey_papers(intermediate_csv, output_csv)

print(f"\nNon-survey papers saved as {output_csv}")
