from dotenv import load_dotenv  # type: ignore
load_dotenv()

import streamlit as st
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
from serpapi import GoogleSearch  # type: ignore
import openai  # type: ignore
import os
import time

# Load environment variables
SERPAPI_KEY = os.getenv("SERPAPI_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Streamlit App Header and Description
st.title("AI Agent Application")
st.write("This app connects to Google Sheets, performs web searches, and extracts specific information based on user-defined prompts.")

# Sidebar for User API Keys
st.sidebar.header("API Key Configuration")
user_serpapi_key = st.sidebar.text_input("Enter your SerpAPI Key")
user_openai_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")

# Use User-Provided Keys if Available
current_serpapi_key = user_serpapi_key or SERPAPI_KEY
current_openai_key = user_openai_key or OPENAI_API_KEY

# Google Sheets Data Input Section
st.header("Google Sheets Data")
sheet_id = st.text_input("Enter Google Sheet ID")
range_name = st.text_input("Enter Range (e.g., 'Sheet1!A1:D10')")

# Initialize an empty DataFrame for the data
sheet_data = pd.DataFrame()

# Load Google Sheets Data
if st.button("Load Google Sheet"):
    if not current_serpapi_key:
        st.error("Missing SerpAPI key. Please add it in the sidebar.")
    elif sheet_id and range_name:
        try:
            credentials = service_account.Credentials.from_service_account_file(
                "credentials.json", 
                scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"]
            )
            service = build("sheets", "v4", credentials=credentials)
            sheet = service.spreadsheets()
            result = sheet.values().get(spreadsheetId=sheet_id, range=range_name).execute()
            values = result.get("values", [])
            sheet_data = pd.DataFrame(values[1:], columns=values[0]) if values else pd.DataFrame()
            st.dataframe(sheet_data)
        except Exception as e:
            st.error(f"Error loading Google Sheet: {e}")
    else:
        st.warning("Please provide both Google Sheet ID and Range.")

# Query Template Input Section
st.header("Query Template")
prompt_template = st.text_area(
    "Enter your query template (e.g., 'Get the contact email and address of {company}')"
)

# Validate Template and Show Example
if prompt_template and "{company}" in prompt_template:
    st.write(f"Example query: '{prompt_template.format(company='SampleCompany')}'")
else:
    st.warning("Include the '{company}' placeholder in your query template.")

# Function to Perform Web Search
def perform_web_search(entity_name):
    if not current_serpapi_key:
        st.error("Missing SerpAPI key. Please provide your key in the sidebar.")
        return []
    try:
        query = prompt_template.format(company=entity_name)
        params = {
            "engine": "google",
            "q": query,
            "api_key": current_serpapi_key,
        }
        search = GoogleSearch(params)
        results = search.get_dict()
        return results.get('organic_results', [])
    except Exception as e:
        st.error(f"Error during web search: {e}")
        return []

# Perform Web Searches
search_results = {}
if not sheet_data.empty and prompt_template and "{company}" in prompt_template:
    for entity in sheet_data.iloc[:, 0].unique():
        search_results[entity] = perform_web_search(entity)
        time.sleep(2)  # Avoid hitting rate limits
    st.write("Search results:")
    st.write(search_results)

# Function to Extract Information Using OpenAI
def extract_info_with_llm(entity_name, search_results):
    if not current_openai_key:
        st.error("Missing OpenAI key. Please provide your key in the sidebar.")
        return "Error"
    try:
        openai.api_key = current_openai_key
        prompt = f"Extract relevant information for {entity_name} from these search results:\n\n"
        for result in search_results:
            prompt += f"- {result.get('title')}: {result.get('link')}\n{result.get('snippet', '')}\n\n"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.7
        )
        return response['choices'][0]['message']['content'].strip()
    except openai.error.RateLimitError:
        return f"Mock data for {entity_name} (quota exceeded)"
    except Exception as e:
        st.error(f"Error during information extraction: {e}")
        return "Error"

# Extract and Display Information
extracted_info = {}
if search_results:
    for entity, results in search_results.items():
        extracted_info[entity] = extract_info_with_llm(entity, results)

    if extracted_info:
        # Notify about mock data usage
        mock_entities = [entity for entity, info in extracted_info.items() if "Mock data" in info]
        if mock_entities:
            st.warning(f"Quota exceeded for OpenAI API. Mock data is used for: {', '.join(mock_entities)}")

        # Enhance extracted information table
        df_results = pd.DataFrame.from_dict(
            {entity: {"Extracted Info": info, "Status": "Mock" if "Mock data" in info else "Real"}
             for entity, info in extracted_info.items()},
            orient="index"
        )
        st.dataframe(df_results)

        # Save enhanced table to CSV
        csv_data = df_results.to_csv().encode("utf-8")
        st.download_button("Download CSV", csv_data, "extracted_info.csv", "text/csv")

        # Google Sheets Output Integration
        if st.button("Write to Google Sheet"):
            try:
                sheet.values().append(
                    spreadsheetId=sheet_id,
                    range=range_name,
                    valueInputOption="RAW",
                    body={"values": df_results.reset_index().values.tolist()}
                ).execute()
                st.success("Results successfully written to Google Sheet.")
            except Exception as e:
                st.error(f"Error writing to Google Sheet: {e}")

        # Suggest retry for quota issues
        if mock_entities:
            st.info("Consider reloading with valid OpenAI API keys to retrieve accurate data.")
    else:
        st.warning("No information extracted. Quota issues or incorrect queries may be the cause.")
