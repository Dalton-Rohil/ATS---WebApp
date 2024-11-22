import pandas as pd

def clean_data(text):
    """ Basic text cleaning function. """
    text = text.lower()
    text = text.replace("\n", " ")
    return text

def preprocess_dataset(df, text_column):
    """ Function to preprocess a dataframe for NLP. """
    df[text_column] = df[text_column].apply(clean_data)
    return df
