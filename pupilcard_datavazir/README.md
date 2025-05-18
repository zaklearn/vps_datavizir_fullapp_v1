# Datavizir EGRA/EGMA Assessment Tool v3.0.2

![Dashboard Icon](https://img.shields.io/badge/🏆-Assessment-yellow)
![Streamlit](https://img.shields.io/badge/Streamlit-1.44.0-FF4B4B)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![License](https://img.shields.io/badge/License-MIT-green)

A comprehensive tool for analyzing and visualizing student performance on Early Grade Reading Assessment (EGRA) and Early Grade Mathematics Assessment (EGMA) tests.

## Features

- **Individual Student Reports**: Generate detailed performance reports for individual students
- **Class Comparison**: Compare performance across different classes within a school
- **School Comparison**: Compare performance across multiple schools
- **Hybrid Interpretation System**: Combines rule-based analysis with AI-assisted insights
- **Export to Word**: Generate professional reports for sharing and printing

## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Data Format](#data-format)
- [Hybrid Interpretation System](#hybrid-interpretation-system)
- [Troubleshooting](#troubleshooting)
- [Development](#development)
- [Deployment](#deployment)
- [License](#license)

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git (optional, for cloning the repository)

### Steps

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

## Configuration

1. Copy the environment template file:
```bash
cp .env.example .env
```

2. Edit the `.env` file and add your Anthropic API key (if you have one):
```bash
ANTHROPIC_API_KEY=your_api_key_here
```

3. Additional configuration options are available in the `.env` file for logging and debugging.

## Usage

1. Start the application:
```bash
streamlit run app.py
```

2. Open your browser and navigate to `http://localhost:8501`

3. Choose a module:
   - **Pupil Report Card**: Analysis of individual student performance
   - **Class Comparison**: Compare performance across classes within a school
   - **School Comparison**: Compare performance across schools

4. Upload your data or use the demo data feature

### Example Workflow

1. Start with the **Pupil Report Card** to analyze individual student performance
2. Use **Class Comparison** to identify performance patterns across classes
3. Use **School Comparison** to benchmark schools against each other
4. Export reports for stakeholders (teachers, administrators, parents)

## Data Format

The application expects an Excel file with the following columns:

### Required Columns

| Column | Description |
|--------|-------------|
| `school` | School name |
| `group` | Class/group name |
| `pupil_id` | Unique student identifier |
| `last_name` | Student's last name |
| `first_name` | Student's first name |
| `language` | Student's language |
| `st_gender` | Student's gender (M/F) |
| `st_age` | Student's age (numeric) |

### EGRA Indicators

| Column | Description | Mastery Threshold |
|--------|-------------|------------------|
| `clpm` | Letters per minute | 44 |
| `phoneme` | Correct phonemes (%) | 41 |
| `sound_word` | Words read correctly (%) | 60 |
| `cwpm` | Correct words per minute | 29 |
| `listening` | Listening comprehension (%) | 75 |
| `orf` | Reading fluency | 50 |
| `comprehension` | Reading comprehension (%) | 75 |

### EGMA Indicators

| Column | Description | Mastery Threshold |
|--------|-------------|------------------|
| `number_id` | Number identification | 56 |
| `discrimin` | Number discrimination (%) | 60 |
| `missing_number` | Missing number (%) | 60 |
| `addition` | Additions per minute | 10 |
| `subtraction` | Subtractions per minute | 10 |
| `problems` | Problems solved (%) | 60 |

## Hybrid Interpretation System

The application features a hybrid interpretation system that combines:

1. **Rule-based analysis**: Systematic evaluation of each indicator against standard thresholds
2. **AI-enhanced insights**: Provides contextual interpretations and recommendations using:
   - Anthropic's Claude API (if configured)
   - Local fallback mechanisms (when API is unavailable)

### Claude API Integration

To enable the AI-enhanced insights with Claude:
1. Create an account at [anthropic.com](https://www.anthropic.com/)
2. Generate an API key in your account dashboard
3. Add the key to your `.env` file

### Fallback Mechanism

If the Claude API is unavailable or not configured:
1. The system will attempt to use a local text generation model
2. If the local model fails, it will use a rule-based fallback message

## Troubleshooting

### Common Issues

1. **Missing Columns Error**
   - Ensure your Excel file includes all required columns
   - Column names must match exactly (case-sensitive)

2. **API Connection Error**
   - Check your internet connection
   - Verify your API key in the `.env` file
   - Ensure your API key has sufficient quota

3. **Report Export Issues**
   - Ensure you have writing permissions in the directory
   - Close any open Word documents using the same filename

### Error Logs

The application logs errors in the following locations:
- Console output
- `app.log` file (if configured in `.env`)

## Development

### Project Structure

```
datavizir-egra-egma/
├── app.py                   # Main application entry point
├── config.py                # Centralized configuration
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables
├── modules/
│   ├── __init__.py
│   ├── anthropic.py         # Claude API integration
│   ├── class_comparison.py  # Class comparison module
│   ├── comparative_common.py # Shared functions for comparisons
│   ├── interpretation.py    # Hybrid interpretation system
│   ├── language.py          # Multilingual support
│   ├── pupil_report_card.py # Individual student reports
│   ├── school_comparison.py # School comparison module
│   ├── standards.py         # Assessment standards
│   └── word_report_template.py # Word export templates
```

### Adding New Features

1. Create a feature branch:
```bash
git checkout -b feature/your-feature-name
```

2. Implement your changes

3. Update tests and documentation

4. Submit a pull request

## Deployment

### Streamlit Sharing

1. Push your code to GitHub
2. Visit [share.streamlit.io](https://share.streamlit.io/) and connect your repository
3. Add environment variables (especially your API key)

### Self-Hosted

For self-hosted deployment:

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables

3. Start the application:
```bash
streamlit run app.py
```


## Acknowledgments

- Powered by Streamlit, Pandas, Plotly, and other open-source libraries
- Claude API by Anthropic for enhanced interpretations
