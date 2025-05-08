# Educational Assessment Analytics

## Overview

Educational Assessment Analytics is a comprehensive web application designed for analyzing Early Grade Reading Assessment (EGRA) and Early Grade Mathematics Assessment (EGMA) data. The platform enables educators, researchers, and policymakers to gain actionable insights from educational assessment data through interactive visualizations, statistical analyses, and detailed reports.

![Educational Assessment Analytics](https://via.placeholder.com/800x400?text=Educational+Assessment+Analytics)

## Key Features

- **Multilingual Interface**: Full support for English, French, and Arabic
- **Interactive Visualizations**: Dynamic charts and graphs powered by Plotly
- **Comprehensive Analysis Modules**: Eight specialized analysis modules
- **Automated Reporting**: Generate detailed Word reports with interpretations and recommendations
- **Data Import Flexibility**: Support for Excel, CSV, JSON, and Stata formats
- **Statistical Robustness**: Employs appropriate statistical methods for educational data

## Analysis Modules

### 1. Statistical Overview
Provides comprehensive descriptive statistics for assessment variables.

**Key Features:**
- Calculates mean, median, standard deviation, and percentiles
- Generates histograms with distribution visualizations
- Organizes EGRA and EGMA variables separately
- Exports detailed statistical tables

### 2. Zero Scores Analysis
Identifies students scoring zero on assessment tasks to highlight critical skill gaps.

**Key Features:**
- Calculates percentage of zero scores per task
- Categorizes tasks by severity level (critical, concerning, watch, satisfactory)
- Provides skill-specific recommendations for intervention
- Visualizes zero score distribution with threshold indicators

### 3. School Comparison
Compares performance across schools to identify disparities and success factors.

**Key Features:**
- Calculates mean scores by school for each assessment variable
- Identifies highest and lowest performing schools
- Performs statistical significance testing using Kruskal-Wallis H-test
- Visualizes performance distribution by school

### 4. Language Effect Analysis
Analyzes the impact of language of instruction on student performance.

**Key Features:**
- Compares performance between students taught in different languages
- Tests statistical significance using Mann-Whitney U test
- Visualizes language-based performance differences
- Provides language-specific instructional recommendations

### 5. Correlation Analysis
Examines relationships between different assessment variables.

**Key Features:**
- Generates correlation matrix with interactive heatmap visualization
- Identifies significant correlations (>|0.5|)
- Creates interactive scatterplots with regression lines
- Provides educational interpretations of skill relationships

### 6. Test Reliability (Cronbach's Alpha)
Assesses internal consistency reliability of assessment instruments.

**Key Features:**
- Calculates Cronbach's Alpha coefficient for selected variables
- Interprets reliability levels with clear thresholds
- Visualizes reliability comparison across test groups
- Provides recommendations based on reliability analysis

### 7. Gender Effect Analysis
Examines performance differences between boys and girls.

**Key Features:**
- Compares mean scores by gender
- Tests statistical significance of gender differences
- Visualizes gender-based performance patterns
- Provides gender-responsive teaching recommendations

### 8. International Standards Comparison
Benchmarks local performance against established international standards.

**Key Features:**
- Compares local means with international benchmarks
- Calculates gaps and percentage of benchmark achieved
- Categorizes performance (critical, concerning, approaching, meeting)
- Provides recommendations based on benchmark comparison

## Installation

### Requirements
- Python 3.7 or higher
- Required packages are listed in `requirements.txt`

### Setup Instructions

1. Clone the repository
   ```
   git clone https://github.com/yourusername/educational-assessment-analytics.git
   cd educational-assessment-analytics
   ```

2. Create and activate a virtual environment (recommended)
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies
   ```
   pip install -r requirements.txt
   ```

4. Run the application
   ```
   streamlit run main.py
   ```

5. Access the application in your web browser at `http://localhost:8501`

## Usage Guide

### 1. Initial Setup
- Select your preferred language from the dropdown in the sidebar
- Upload your data file (supported formats: Excel, CSV, JSON, Stata DTA)
- For CSV files, you can configure encoding and separator options

### 2. Select Analysis Type
Choose from the eight analysis modules in the sidebar:
- Statistical Overview
- Zero Scores Analysis
- Correlation Analysis
- Test Reliability (Cronbach's Alpha)
- School Performance Analysis
- Gender Effect Analysis
- International Standards Comparison
- Language of Instruction Comparison

### 3. Configure Analysis
- Select variables to include in the analysis
- Adjust any analysis-specific parameters
- View the results and visualizations

### 4. Export Results
- Download reports in Word format
- Download charts and visualizations 
- Export data tables to CSV

## Data Format

The application expects assessment data with the following variable types:

### Assessment Variables
- **EGRA Variables**: clpm, phoneme, sound_word, cwpm, listening, orf, comprehension
- **EGMA Variables**: number_id, discrimin, missing_number, addition, subtraction, problems

### Demographic Variables
- **school**: School identifier
- **stgender**: Student gender (can be coded in various formats)
- **language_teaching**: Language of instruction
- **language_home**: Home language (optional)

## Project Structure

```
educational-assessment-analytics/
├── main.py                   # Main application entry point
├── config.py                 # Configuration and translation settings
├── language_utils.py         # Utilities for language handling
│
├── analyse1.py               # Statistical Overview module
├── analyse2.py               # Zero Scores Analysis module
├── analyse5.py               # Correlation Analysis module
├── analyse6.py               # Test Reliability module
├── analyse7.py               # School Performance Analysis module
├── analyse10.py              # Gender Effect Analysis module
├── analyse12.py              # International Standards Comparison module
├── analyse13.py              # Language Effect Comparison module
│
├── report/                   # Report generation system
│   ├── report_base.py
│   ├── report_statistical.py
│   ├── report_zero_scores.py
│   ├── report_correlation.py
│   ├── report_reliability.py
│   ├── report_school.py
│   ├── report_gender.py
│   ├── report_international.py
│   ├── report_language.py
│   ├── report_utils.py
│   └── report_wrapper.py
│
├── correlation_modules/       # Modules for correlation analysis
│   ├── matrix.py
│   ├── interactive.py
│   ├── significant.py
│   ├── interpretation.py
│   └── report.py
│
└── requirements.txt          # Python dependencies
```

## Extending the Application

### Adding a New Analysis Module
1. Create a new Python file (e.g., `analyse_new.py`)
2. Implement the main analysis function following the pattern in existing modules
3. Add the module to the `ANALYSES` dictionary in `main.py`
4. Create a corresponding report generator in the `report/` directory if needed

### Adding a New Language
1. Add the language to the `AVAILABLE_LANGUAGES` dictionary in `config.py`
2. Create a new translation dictionary in the `translations` variable

### Customizing Reports
Modify the report generator classes in the `report/` directory to change the format, content, or styling of the generated reports.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Developed for educational assessment professionals worldwide
- Built with Streamlit, Pandas, Plotly, and Python-docx
- Inspired by global best practices in early grade assessment

## Contact

For questions, feedback, or support, please contact [your-email@example.com](mailto:your-email@example.com)
