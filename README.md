# AI Agent Application

## Project Description
This project automates web searches and extracts information based on user-defined prompts. It enables users to:
- Load data from a Google Sheet or upload a CSV file.
- Perform web searches for entities using SerpAPI.
- Extract relevant information from search results using OpenAI's GPT API.
- View extracted data, download it as a CSV, or write it back to Google Sheets.

The application is built using Python and Streamlit, ensuring a user-friendly interface and efficient processing.

---

## Setup Instructions

### Prerequisites
1. **Install Python 3.8 or above**:
   Download and install Python from [python.org](https://www.python.org/).
2. **Install pip**:
   Ensure pip (Python package manager) is installed with Python.

### Steps
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/<your-username>/AI-Agent-Project.git
   cd AI-Agent-Project

2. **Install Dependencies**: Run the following command to install all required packages:
pip install -r requirements.txt

3. **Set Up Environment Variables**:

Create a .env file in the project directory with the following content:

SERPAPI_KEY=your-serpapi-key

OPENAI_API_KEY=your-openai-key

Replace your-serpapi-key and your-openai-key with your actual API keys.

4.**Add Google Sheets Credentials**:

Download your Google Sheets credentials JSON file (instructions in the Google Sheets API Guide).

Place the file in the project directory and name it credentials.json.

5.**Run the Application**: Start the Streamlit app with:

streamlit run app.py

6.**Open in Browser**: The app will run on http://localhost:8501/ by default. Open this URL in your browser.

### Usage Guide
**Step 1: Load Data**

**Google Sheets**:

Enter the Google Sheet ID and range (e.g., Sheet1!A1:D10).

Click Load Google Sheet to preview the data.

**CSV File**:

Drag and drop a CSV file into the upload area.

**Step 2: Define Query Template**

Input a query template like Get the CEO of {company}.

Ensure the {company} placeholder matches the column with the entities to search.

**Step 3: Extract Information**

The app will perform searches for each entity and use OpenAI's GPT API to extract relevant data.

**Step 4: View and Download Results**

View results in a table.

Download as a CSV file or write results back to Google Sheets.

### API Keys and Environment Variables

**Required API Keys**

**SerpAPI Key:**

Sign up at SerpAPI to get your API key.

**OpenAI Key:**

Get an API key from OpenAI.

**Adding Keys**

Add your API keys to the .env file:

SERPAPI_KEY=your-serpapi-key

OPENAI_API_KEY=your-openai-key

### Optional Features

**Advanced Query Templates:**

Support for extracting multiple fields in a single query (e.g., Get the CEO and address of {company}).

**Google Sheets Write-Back:**

Write the extracted data directly back to the connected Google Sheet.

**Robust Error Handling:**

Mock data is used when API quotas are exceeded, ensuring the app remains functional.

**User-Provided API Keys:**

Users can input their own SerpAPI and OpenAI API keys via the app interface.

## Loom Video
Check out the project demo here: [Watch the video] https://www.loom.com/share/838cafc36160432ea8f03ab3058a2770?sid=24137364-7f8c-4e6b-b02c-d5e5d67cadfa
