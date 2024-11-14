# ATS System

## Overview
**ATS System** is an advanced, cloud-ready Applicant Tracking System designed to evaluate resumes against specific job descriptions (JDs) using Natural Language Processing (NLP). It leverages skill extraction, and keyword matching, and provides insightful comparisons to help recruiters make data-driven decisions. The system is designed to handle various JDs and process thousands of resumes efficiently.

## Key Features
- **Skill Extraction**: Uses NLP to analyze JDs and resumes, extracting key skills and requirements.
- **Suitability Scoring**: Dynamically scores resumes based on JD requirements.
- **Automated Evaluation**: Continuously learns and improves based on user data.
- **Dashboard for Results**: Presents a concise, clear evaluation for recruiters.
- **Cloud-Ready Deployment**: Deployed on Azure, with Docker containers for ease of scalability and maintenance.

## Project Structure
```plaintext
ATS System/
├── app/
│   ├── prompts.py             # Dynamic prompt generation for JD and resume analysis
│   └── utils.py               # Utility functions including PDF handling, API requests, and scoring logic
├── config/
│   └── settings.py            # Configuration settings (e.g., API keys)
├── data/
│   ├── jd_samples/            # Sample job descriptions for testing
│   └── resume_samples/        # Sample resumes for testing
├── models/
│   ├── spacy_ner_model/       # Folder for fine-tuned spaCy NER model
│   └── transformers/          # Transformer-based NLP models for advanced processing
├── scripts/
│   ├── data_preprocessing.py  # Script for preparing and cleaning data
│   ├── incremental_train_ner.py # Script for incremental NER model training
│   └── nlp_extraction.py      # NLP-based extraction logic for JD and resumes
├── tests/
│   ├── test_extraction.py     # Test cases for NLP extraction
│   └── test_integration.py    # Integration tests for end-to-end functionality
├── main.py                    # Main application script for the ATS system
├── Dockerfile                 # Dockerfile for containerizing the application
├── requirements.txt           # List of dependencies for the project
└── README.md                  # Project documentation
```
## Prerequisites
- Python 3.8+
- Docker (for containerization)
- Azure or Local Database (optional for long-term storage of results)

## Installation and Setup

### 1. Clone the Repository:
```bash
git clone https://github.com/yourusername/ATS-System.git
cd ATS-System
```
### 2. Configure API Keys:
- Add your OpenAI API key in config/settings.py:
```python
API_KEY = "your_openai_api_key"
```
### 3. Install Dependencies:

- Using requirements.txt:
```bash
pip install -r requirements.txt
```
### 4. Database Setup (optional):
- Configure the SQLite database to store results in data/ats_data.db.

## Usage Guide
1. Uploading JDs and Resumes:
   - Go to the main ATS app interface.
   - Enter a job description and upload resumes (PDF format).
2. Evaluation:
   - Click Evaluate to analyze the match between JDs and resumes.
3. View Results:
   - See matched results with scores, matching and missing skills, and a final assessment.

## Project Components
### Data Storage
- SQLite is used to store processed data, including job descriptions, resumes, and evaluation results.
### Continuous Training
- Automatically improves NLP models with usage, using data from JD and resume samples in the data/ folder.

## Customizing for Your Own Use
- API Key: Replace the API key in config/settings.py with your own.
- Model Training: Customize and train spacy_ner_model and transformers in the models folder for improved entity extraction.
## Contributing
Please feel free to fork this project, submit issues, and contribute by opening pull requests.

License
This project is licensed under the MIT License.
```kotlin

In this structured format, GitHub should recognize headings, code blocks, and lists without issue. Let me know if this displays as intended for you!
```
