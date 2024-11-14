# ATS System

## Overview
**ATS System** is an advanced, cloud-ready Applicant Tracking System designed to evaluate resumes against specific job descriptions (JDs) using Natural Language Processing (NLP). It leverages skill extraction, keyword matching, and provides insightful comparisons to help recruiters make data-driven decisions. The system is designed to handle various JDs and process thousands of resumes efficiently.

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

Prerequisites
Python 3.8+
Docker
Azure Account (for cloud deployment)
API Key for OpenAI or Google Gemini AI in config/settings.py (replace YOUR_API_KEY with your actual key)
