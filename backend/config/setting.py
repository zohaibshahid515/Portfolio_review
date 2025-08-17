# config/setting.py

import os

from dotenv import load_dotenv
load_dotenv()

# Azure Document Intelligence (Layout Model)
DOCUMENT_INTELLIGENCE_KEY = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY", "your-doc-intelligence-key")
DOCUMENT_INTELLIGENCE_ENDPOINT = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT", "https://<your-region>.cognitiveservices.azure.com/")

# Azure OpenAI (Foundry)



import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
OPENAI_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")


TITLES_CONFIG_PATH = r"C:\usama\dynamic_profile_rev\config\titles_config.json"