
# Google Scholar Survey Excluder

## About the Project

This code **excludes survey and review papers** from Google Scholar profiles. This tool helps to focus on the **citation statistics** that are directly tied to original research work.

The project implements two levels of exclusion criteria to filter out irrelevant papers:

---

## Exclusion Criteria

### 1. Exclusion of Surveys
Papers are classified as surveys based on the presence of specific keywords in the **Title**. If the title contains any of the following keywords (case-insensitive), the paper is categorized as a survey and excluded:

- **survey**
- **review**
- **directions**
- **challenges**
- **trends**
- **approaches**
- **opportunities**
- **concepts**
- **roadmap**
- **Advances in**
- **Analysis of**

#### Rationale:
These keywords typically indicate that the paper is not an original research article but rather a survey, review, or commentary on a topic. However, this is not a comprehensive list and neither is the ideal way of doing it (see Future Improvements.)

---

## Future Improvements

In the future, I hope to implement a more advanced classification system for identifying survey papers. If you're interested in contributing to this project, feel free to reach out! Some potential approaches to improve classification include:

- **Natural Language Processing (NLP)**: Using machine learning models like BERT or GPT to analyze the full text of the paper for context.

---

## How to Use the Code

### Step 1: Prepare Your Google Scholar Data
1. Go to the **Google Scholar profile** of the researcher.
2. Click on **"SHOW MORE"** until the **entire list of papers** is displayed.
3. Right Click on the Google Scholar page and press **Save As ...** to save the page as an HTML file named `papers.html`.

### Step 2: Run the Code
1. Place the `papers.html` file in the same directory as the script.
2. Open a terminal or command prompt and navigate to the directory.
3. Run the script using the following command:
   ```bash
   python exclude_surveys.py
   ```

### Step 3: Outputs
The script will:
1. Convert the `papers.html` file into a CSV file named `GScholar-profile.csv`, containing the full list of papers.
2. Exclude survey papers based on the keywords and create another CSV file named `Non-Survey-Papers.csv`.
3. Exclude papers with zero citations or missing year and log the number of such exclusions.
4. Print key statistics, including:
   - Total number of papers excluded.
   - Percentage of papers classified as surveys.
   - Percentage of excluded citations.
5. Display a comparison table showing:
   - Total citations.
   - **H-index** and **i10-index** with and without survey papers.

---

## Example Output

After running the script, you will get:

### CSV Files
- `GScholar-profile.csv`: The full list of papers in CSV format.
- `Non-Survey-Papers.csv`: The filtered list without surveys and papers with missing data.

### Statistics
```
Number of entries excluded due to missing citation or year: 3
Number of papers excluded as survey: 5
Percentage of papers excluded as survey: 25.00%
Percentage of excluded citations compared to total: 18.00%
```

### Comparison Table
```
+------------------+---------------+------------------+
| Metric           | With Surveys  | Without Surveys  |
+------------------+---------------+------------------+
| Total Papers     | 40            | 30               |
| Total Citations  | 5000          | 4100             |
| H-Index          | 20            | 18               |
| i10-Index        | 25            | 22               |
+------------------+---------------+------------------+
```

---

## Dependencies

The following Python libraries are required to use this repository:

- **csv**: Standard Python library for reading and writing CSV files.
- **re**: Standard Python library for handling regular expressions.
- **pandas**: Used for data manipulation and analysis. Install it with:
  ```bash
  pip install pandas
  ```
- **BeautifulSoup**: Part of the `bs4` package, used for parsing HTML and XML documents. Install it with:
  ```bash
  pip install beautifulsoup4
  ```
- **tabulate**: Converts tabular data into formatted tables. Install it with:
  ```bash
  pip install tabulate
  ```

Ensure you have Python installed on your system. You can install all required libraries with the following command:

```bash
pip install pandas beautifulsoup4 tabulate
```


---

## Contributions

If you have ideas to improve this project or want to contribute, feel free to open a pull request or contact me. Let’s make research recruitment fairer and more efficient!

---

