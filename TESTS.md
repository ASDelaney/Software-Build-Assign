Manual Tests for NYT Analysis Code
1. Load Data Test:
Test Steps:
Run the analysis script with valid configuration files.
Ensure that the data is loaded successfully from the NYT API.
Expected Result:
No errors during data loading, and the self.dataset attribute is populated.

2. Compute Analysis Test:
Test Steps:
Run the analysis script with a loaded dataset.
Check if the script computes the average word count correctly.
Verify that the average word count is a float.
Expected Result:
The average word count is computed without errors, and the result is of type float.

3. Plot Data Test:
Test Steps:
Run the analysis script with a loaded dataset.
Check if the script generates a bar chart when visualizing word counts.
Verify that the chart is saved as an image file (optional).
Expected Result:
A bar chart is displayed or saved without errors.

4. Exception Handling Test:
Test Steps:
Run the analysis script with incorrect configuration files.
Ensure that the script raises appropriate errors when necessary.
Expected Result:
Errors are raised when loading data or computing analysis under incorrect conditions.

5. Integration Test:
Test Steps:
Run the entire analysis script, including loading data, computing analysis, and plotting data.
Verify that the script completes the analysis process without errors.
Expected Result:
The script successfully loads data, computes analysis, and visualizes data without any issues.
