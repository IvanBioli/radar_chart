README.txt

## Radar Chart Generation Script

This script generates a **radar chart** from an Excel file using Plotly. The input Excel file should follow a specific format, and the resulting radar chart will be saved as a PDF file with the same name as the input file (but with a `.pdf` extension).

---

### Requirements

To run this script, ensure you have the following installed on your system:

1. **Python** (version 3.6 or above)
2. **pip** (Python package manager)

Required Python libraries:
- pandas
- plotly
- openpyxl
- kaleido (for saving the figure as PDF)

---

### Installation

1. **Install Python (IF YOU ALREADY HAVE PYTHON SKIP THIS STEP)**:  
   Download and install Python from https://www.python.org/.  
   Ensure that Python and pip are added to your system PATH.

2. **Install the required libraries**:  
   Open a terminal or command prompt and run the following command:

```
python3 -m pip install pandas plotly openpyxl kaleido
```
---

### Input File Format

The input file should be an Excel file (`.xlsx`) **with no spaces in the name** with the following structure:

1. **First Row**:  
Contains the title of the radar chart.

2. **Second Row**:  
Contains the names of the data series (e.g., **Cytotoxicity**, **Transfection efficiency**, etc.).

3. **First Column** (starting from the third row):  
Contains the categories (labels) for the radar chart.

4. **Data Columns** (starting from the second column, third row onwards):  
Contains the values corresponding to each series and category.

**Example**: Provided in `data/radar_DoE.xlsx`.


---

### Usage

1. **Prepare the Excel file**:  
 - Format your Excel file as described above and save it with a `.xlsx` extension.
 - Make sure you deleted additional rows at the bottom of the file
 - Make sure you deleted additional columns at the right of the file

2. **Update the script**:  
- Replace the `file_path` variable in the script with the path to your Excel file. Example

```python
file_path = 'data/radar_DoE_RSM.xlsx'
```
- Adjust the figure size with the variables `figure_width_cm` and `figure_height_cm`.
3. **Run the script**:
Open a terminal or command prompt in the folder where the script is saved and run:
```
python3 generate_radar_chart.py
```

The radar chart will be displayed interactively in your browser or environment.
The script will save the radar chart as a PDF file in the same directory as the input file.
Example:
```
Input: data/radar_DoE.xlsx
Output: data/radar_DoE.pdf
```
