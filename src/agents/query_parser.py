# src/agents/query_parser.py
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
import re
from typing import Dict

class QueryParser:
    def __init__(self, llm: OpenAI):
        self.llm = llm
        self.prompt_template = PromptTemplate(
            template="""
Extract the following information from the user's query:
1. Stock ticker symbol (e.g., AAPL)
2. Start date (YYYY-MM-DD)
3. End date (YYYY-MM-DD)
4. Timeframe (daily, weekly, monthly)

Query: "{query}"
""",
            input_variables=["query"]
        )

    def parse_query(self, query: str) -> Dict[str, str]:
        response = self.llm(self.prompt_template.format(query=query))
        ticker = self.extract_ticker(response)
        start_date, end_date = self.extract_dates(response)
        timeframe = self.extract_timeframe(response)
        return {
            "ticker": ticker,
            "start_date": start_date,
            "end_date": end_date,
            "timeframe": timeframe
        }

    def extract_ticker(self, text: str) -> str:
        match = re.search(r'\b[A-Z]{1,5}\b', text)
        return match.group(0) if match else ""

    def extract_dates(self, text: str) -> (str, str):
        dates = re.findall(r'\d{4}-\d{2}-\d{2}', text)
        return dates[0] if len(dates) > 0 else "", dates[1] if len(dates) > 1 else ""

    def extract_timeframe(self, text: str) -> str:
        match = re.search(r'\b(daily|weekly|monthly)\b', text.lower())
        return match.group(0) if match else "daily"