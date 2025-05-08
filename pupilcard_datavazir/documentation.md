# Datavizir EGRA/EGMA Assessment Tool v3.0.2

## Table of Contents

1. [Introduction](#introduction)
2. [Architecture Overview](#architecture-overview)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Module Documentation](#module-documentation)
   - [5.1 Pupil Report Card Module](#51-pupil-report-card-module)
   - [5.2 Class Comparison Module](#52-class-comparison-module)
   - [5.3 School Comparison Module](#53-school-comparison-module)
   - [5.4 Interpretation Module](#54-interpretation-module)
   - [5.5 Common Utilities](#55-common-utilities)
6. [Data Format](#data-format)
7. [API Integration](#api-integration)
8. [Report Export](#report-export)
9. [Troubleshooting](#troubleshooting)
10. [Future Development](#future-development)
11. [License & Credits](#license--credits)

## 1. Introduction

The Datavizir EGRA/EGMA Assessment Tool is a comprehensive web application for analyzing and visualizing student performance on Early Grade Reading Assessment (EGRA) and Early Grade Mathematics Assessment (EGMA) tests. Designed for educators, administrators, and educational organizations, this tool provides individual student reports, class-level comparisons, and school-level comparisons with AI-enhanced interpretations.

### Key Features

- **Individual Student Analysis**: Detailed performance reports for each student
- **Class Comparison**: Compare performance across classes within a school
- **School Comparison**: Benchmark multiple schools against each other
- **Hybrid Interpretation System**: Combines rule-based analysis with AI-assisted insights
- **Professional Report Export**: Generate Word documents for sharing and printing
- **Interactive Visualizations**: Dynamic charts and tables for performance metrics
- **Multilingual Support Framework**: Currently optimized for English with expansion capability

### Purpose & User Roles

| User Role | Primary Use Cases |
|-----------|-------------------|
| Teachers | Individual student assessment, parent conferences, personalized learning plans |
| School Administrators | Class performance evaluation, resource allocation, teacher support |
| District/Ministry Officials | School comparison, policy implementation monitoring, system-wide analysis |
| NGOs & Educational Partners | Program impact assessment, targeted intervention design |

## 2. Architecture Overview

The Datavizir EGRA/EGMA Assessment Tool is built on a modular architecture using Python and Streamlit as the primary technologies. This section provides an overview of the system components and their interactions.

### Technology Stack

- **Frontend**: Streamlit (Python-based web application framework)
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly, Plotly Express
- **Document Generation**: python-docx
- **AI Integration**: Anthropic Claude API (optional)
- **Fallback Mechanisms**: Local text generation models or rule-based approaches

### System Components

![System Architecture Diagram](https://example.com/architecture_diagram.png)

The application consists of the following main components:

1. **Core Application (app.py)**: Entry point and navigation handler
2. **Module System**: Separate modules for different analysis features
3. **Data Processing Layer**: Handles data import, validation, and transformation
4. **Visualization Engine**: Generates interactive charts and tables
5. **Interpretation System**: Provides insights using rule-based and AI approaches
6. **Export System**: Generates Word documents for reporting

### Data Flow

1. User uploads Excel data or selects demo data
2. Data is validated and processed by the appropriate module
3. Visualizations are generated based on processed data
4. Interpretation system analyzes results and generates insights
5. User can export reports in Word format

## 3. Installation

### System Requirements

- **Python**: 3.8 or higher
- **Operating System**: Windows, macOS, or Linux
- **RAM**: 4GB minimum, 8GB recommended
- **Disk Space**: 500MB for application and dependencies
- **Internet Connection**: Required for AI-enhanced interpretations (optional)

### Installation Steps

1. Clone the repository or download the source code:
```bash
git clone https://github.com/yourusername/datavizir-egra-egma.git
cd datavizir-egra-egma
```

2. Create a virtual environment:
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure the application (see [Configuration](#configuration) section)

5. Start the application:
```bash
streamlit run app.py
```

6. Open the application in your web browser at http://localhost:8501

### Docker Installation (Optional)

If you prefer using Docker, follow these steps:

1. Build the Docker image:
```bash
docker build -t datavizir-egra-egma .
```

2. Run the container:
```bash
docker run -p 8501:8501 datavizir-egra-egma
```

3. Access the application at http://localhost:8501

## 4. Configuration

### Environment Variables

The application uses environment variables for configuration. These can be set in a `.env` file in the project root:

```
# Anthropic API Configuration
ANTHROPIC_API_KEY=your_api_key_here

# Application Settings
DEPLOYMENT_ENV=development  # or production
DEBUG_MODE=false

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=app.log
```

### Configuration Files

The main configuration is stored in `config.py`. Key settings include:

- **Application Paths**: Directories for data, temporary files, etc.
- **Application Constants**: Version, name, default language
- **Standards**: Evaluation thresholds for EGRA and EGMA indicators
- **Translations**: Text labels and messages
- **API Configurations**: Model names, token limits, etc.

### Anthropic API Setup

To enable AI-enhanced interpretations:

1. Create an account at [anthropic.com](https://www.anthropic.com/)
2. Generate an API key in your account dashboard
3. Add the key to your `.env` file:
```
ANTHROPIC_API_KEY=your_actual_api_key
```

If no valid API key is provided, the application will use fallback mechanisms to generate interpretations.

## 5. Module Documentation

### 5.1 Pupil Report Card Module

The Pupil Report Card module provides detailed analysis of individual student performance, with visualizations, status indicators, and interpretations.

#### Entry Point: `pupil_report_card.py`

```python
def main():
    """
    Main function for the pupil report card module
    """
```

#### Key Components

- **Student List View**: Displays all students with basic information
- **Search Functionality**: Allows finding students by school, class, and name
- **Profile Display**: Shows detailed student information and performance metrics
- **Performance Visualization**: Charts comparing student scores to standards
- **Interpretation Section**: Provides rule-based and AI-enhanced insights
- **Report Export**: Generates Word document reports

#### UI Flow

1. User selects data source (upload or demo)
2. User navigates student list or searches for a specific student
3. Student profile displays with performance metrics
4. Interpretation is generated and displayed
5. User can export a Word report

#### Key Functions

| Function | Description |
|----------|-------------|
| `display_student_profile()` | Renders all student data and visualizations |
| `style_dataframe()` | Formats tables with color-coded status indicators |
| `export_to_word()` | Generates Word document reports |
| `get_status()` | Determines performance status based on scores |

### 5.2 Class Comparison Module

The Class Comparison module allows comparing performance across different classes within a selected school.

#### Entry Point: `class_comparison.py`

```python
def main():
    """
    Main function for the class comparison module
    """
```

#### Key Components

- **School Selector**: Dropdown to select a school for analysis
- **EGRA Results**: Table and chart comparing class performance on reading indicators
- **EGMA Results**: Table and chart comparing class performance on math indicators
- **Class Insights**: Systematic summary and AI-enhanced interpretation
- **Report Export**: Generates Word document with comparison data

#### UI Flow

1. User selects data source (upload or demo)
2. User selects a school from the dropdown
3. Class comparison tables and charts are displayed
4. Class insights are generated and displayed
5. User can export a comparison report

#### Key Functions

| Function | Description |
|----------|-------------|
| `calculate_class_comparison()` | Processes data for class comparison |
| `plot_comparison()` | Creates visualization charts for comparison |
| `export_comparison_to_word()` | Generates Word document reports |

### 5.3 School Comparison Module

The School Comparison module provides benchmarking and comparison across multiple schools.

#### Entry Point: `school_comparison.py`

```python
def main():
    """
    Main function for the school comparison module
    """
```

#### Key Components

- **School Selector**: Multi-select dropdown to choose schools for comparison
- **EGRA Results**: Expandable sections for each reading indicator
- **EGMA Results**: Expandable sections for each math indicator
- **School Insights**: Systematic summary and AI-enhanced interpretation
- **Report Export**: Generates Word document with comparison data

#### UI Flow

1. User selects data source (upload or demo)
2. User selects multiple schools from the dropdown
3. Indicator sections display comparison data
4. School insights are generated and displayed
5. User can export a comparison report

#### Key Functions

| Function | Description |
|----------|-------------|
| `calculate_school_comparison()` | Processes data for school comparison |
| `export_comparison_to_word()` | Generates Word document reports |

### 5.4 Interpretation Module

The Interpretation module provides the core functionality for generating insights from student performance data.

#### Key Components

- **Rule-Based Interpretation**: Systematic analysis based on predefined thresholds
- **AI-Enhanced Interpretation**: Natural language insights using Claude API
- **Fallback Mechanisms**: Local models or templated responses when API is unavailable

#### Key Functions

| Function | Description |
|----------|-------------|
| `generate_rule_based_interpretation()` | Creates structured analysis based on scores |
| `create_llm_prompt()` | Formats prompts for AI interpretation |
| `generate_llm_message()` | Handles API communication and fallbacks |
| `generate_group_summary()` | Creates summaries for class/school groups |

### 5.5 Common Utilities

The application includes several shared utility modules:

#### Language Module (`language.py`)

Handles multilingual support and translations.

| Function | Description |
|----------|-------------|
| `t(key)` | Translates a text key to the current language |
| `get_label(indicator)` | Gets translated label for an indicator |
| `language_selector()` | Adds language selection dropdown to sidebar |

#### Comparative Common Module (`comparative_common.py`)

Provides shared functionality for comparison modules.

| Function | Description |
|----------|-------------|
| `get_labels()` | Gets translated labels for all indicators |
| `get_status()` | Determines status based on score and category |
| `plot_comparison()` | Creates charts for comparisons |
| `export_comparison_to_word()` | Generates Word documents |

#### Anthropic Module (`anthropic.py`)

Handles integration with the Claude API.

| Function | Description |
|----------|-------------|
| `generate_llm_message()` | Sends prompts to Claude API |
| `generate_fallback_message()` | Creates fallback responses when API fails |

## 6. Data Format

### Required Format

The application expects Excel files with the following structure:

#### Required Columns

| Column | Description | Type |
|--------|-------------|------|
| `school` | School name | String |
| `group` | Class/group name | String |
| `pupil_id` | Unique student identifier | Numeric |
| `last_name` | Student's last name | String |
| `first_name` | Student's first name | String |
| `language` | Student's language | String |
| `st_gender` | Student's gender (M/F) | String |
| `st_age` | Student's age | Numeric |

#### EGRA Indicators

| Column | Description | Type | Mastery Threshold |
|--------|-------------|------|------------------|
| `clpm` | Letters per minute | Numeric | 44 |
| `phoneme` | Correct phonemes (%) | Numeric | 41 |
| `sound_word` | Words read correctly (%) | Numeric | 60 |
| `cwpm` | Correct words per minute | Numeric | 29 |
| `listening` | Listening comprehension (%) | Numeric | 75 |
| `orf` | Reading fluency | Numeric | 50 |
| `comprehension` | Reading comprehension (%) | Numeric | 75 |

#### EGMA Indicators

| Column | Description | Type | Mastery Threshold |
|--------|-------------|------|------------------|
| `number_id` | Number identification | Numeric | 56 |
| `discrimin` | Number discrimination (%) | Numeric | 60 |
| `missing_number` | Missing number (%) | Numeric | 60 |
| `addition` | Additions per minute | Numeric | 10 |
| `subtraction` | Subtractions per minute | Numeric | 10 |
| `problems` | Problems solved (%) | Numeric | 60 |

### Sample Data

The application includes demo data generation functionality in each module for testing and demonstration purposes.

#### Demo Data Generation

```python
def generate_demo_data():
    """
    Generate demo data for testing
    
    Returns:
        dict: Dictionary with demo data
    """
```

## 7. API Integration

### Anthropic Claude API

The application integrates with the Anthropic Claude API to provide AI-enhanced interpretations of student performance.

#### Configuration

API settings are configured in `config.py`:

```python
API_CONFIG = {
    "anthropic_model": "claude-3-haiku-20240307",
    "max_tokens": 500,
    "temperature": 0.7
}
```

#### Integration Flow

1. Generate rule-based interpretation from scores
2. Create prompt with scores and rule-based interpretation
3. Send prompt to Claude API
4. Display AI-generated response
5. If API fails, use fallback mechanisms

#### Fallback Mechanisms

1. **Primary Fallback**: Local text generation model (if available)
2. **Secondary Fallback**: Template-based response generation

## 8. Report Export

### Word Document Generation

The application uses `python-docx` to generate professional reports for students, classes, and schools.

#### Student Report

Generated by `export_student_report()` in `word_report_template.py`:

- **Student Information**: Name, age, gender, language, ID, school, class
- **EGRA Results**: Table and chart for reading indicators
- **EGMA Results**: Table and chart for math indicators
- **Interpretation**: Rule-based analysis and AI-enhanced insights

#### Class Comparison Report

Generated by `export_comparison_to_word()` in `comparative_common.py`:

- **EGRA Results**: Table and chart comparing classes
- **EGMA Results**: Table and chart comparing classes
- **Interpretation**: Class-level insights

#### School Comparison Report

Generated by `export_comparison_to_word()` in `comparative_common.py`:

- **EGRA Results**: Table and chart comparing schools
- **EGMA Results**: Table and chart comparing schools
- **Interpretation**: School-level insights

## 9. Troubleshooting

### Common Issues and Solutions

#### Data Import Issues

| Issue | Solution |
|-------|----------|
| Missing required columns | Check data format against requirements |
| Incorrect data types | Ensure numeric columns contain valid numbers |
| Empty data | Verify data source has content |

#### Visualization Errors

| Issue | Solution |
|-------|----------|
| Charts not displaying | Check for valid data in relevant indicators |
| Error in chart generation | Verify data types are appropriate for visualization |

#### API Integration Issues

| Issue | Solution |
|-------|----------|
| Invalid API key | Check `.env` file for correct key |
| API connection error | Verify internet connection |
| API rate limit | Reduce frequency of calls or increase quota |

#### Report Export Issues

| Issue | Solution |
|-------|----------|
| Error generating report | Check file permissions |
| Missing content in report | Verify all data is available before export |
| Formatting issues | Update Word templates if necessary |

### Error Logging

The application uses comprehensive error logging with traceback for debugging:

```python
try:
    # Operation that might fail
except Exception as e:
    st.error(f"Error message: {str(e)}")
    st.error(traceback.format_exc())
```

Logs can be found in:
- Console output
- `app.log` file (if configured)

## 10. Future Development

### Planned Enhancements

#### Short-term Roadmap (3-6 months)

- Additional language support
- Improved data import options (CSV, API)
- Enhanced mobile responsiveness
- Performance optimizations for large datasets

#### Medium-term Roadmap (6-12 months)

- Longitudinal analysis for tracking progress over time
- Custom threshold configuration
- Advanced data visualization options
- User account management

#### Long-term Roadmap (12+ months)

- Integration with school management systems
- Machine learning for predictive analytics
- Real-time collaboration features
- Regional benchmarking database

### Extension Points

The application is designed with extensibility in mind:

| Component | Extension Possibilities |
|-----------|-------------------------|
| Language Support | Add new languages in translation dictionaries |
| Data Sources | Implement additional importers for different formats |
| Visualizations | Add new chart types for alternative analysis |
| Interpretation | Integrate additional AI models or rule sets |
| Reporting | Create custom report templates for specific needs |

## 11. License & Credits

### License

This project is licensed under the MIT License.

### Credits

- **Developer**: Datavizir Team
- **Technologies**:
  - [Streamlit](https://www.streamlit.io/)
  - [Pandas](https://pandas.pydata.org/)
  - [Plotly](https://plotly.com/)
  - [Anthropic Claude](https://www.anthropic.com/)
  - [python-docx](https://python-docx.readthedocs.io/)

---

## Appendix: Code Structure

```
datavizir_pupil_clsch_v3_0_2/
├── app.py                   # Main application entry point
├── config.py                # Centralized configuration
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables
├── README.md                # Project documentation
├── modules/
│   ├── __init__.py
│   ├── anthropic.py         # Claude API integration
│   ├── class_comparison.py  # Class comparison module
│   ├── comparative_common.py # Shared comparison functions
│   ├── interpretation.py    # Hybrid interpretation system
│   ├── language.py          # Language and translation support
│   ├── pupil_report_card.py # Individual student reports
│   ├── school_comparison.py # School comparison module
│   ├── standards.py         # Assessment standards
│   └── word_report_template.py # Word export templates
└── data/                    # Directory for data files
```
