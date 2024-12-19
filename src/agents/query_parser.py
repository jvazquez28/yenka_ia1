# src/agents/query_parser.py
import re
from typing import Dict, Tuple
import logging
from langchain.llms.openai import OpenAI
from langchain.prompts import PromptTemplate

logger = logging.getLogger(__name__)

class QueryParser:
    def __init__(self, llm: OpenAI):
        logger.info("Initializing QueryParser")
        self.llm = llm
        self.prompt_template = PromptTemplate(
            template="""
            Extract the following information from the user's query:
            1. Stock ticker symbol (e.g., AAPL)
            2. Start date (YYYY-MM-DD)
            3. End date (YYYY-MM-DD)
            4. Timeframe (daily, weekly, monthly)

            Date may be specified as last week, last month, etc. In such cases, convert to YYYY-MM-DD format the best you can
            considering the first and last date of either last week, last month, last year as required.

            Date may also be specified as current month, current year, etc. In such cases, convert to YYYY-MM-DD format the best you can
            considering the first and last date of either current month, current year as required.

            Query: "{query}"
            """,
            input_variables=["query"]
        )
        logger.debug("QueryParser initialized with prompt template")


    def parse_query(self, query: str) -> Dict[str, str]:
        logger.info(f"Parsing query: {query}")
        try:
            logger.debug("Invoking LLM with query")
            response = self.llm.invoke(self.prompt_template.format(query=query))

            if not response:
                logger.error("Empty response from LLM")
                raise ValueError("Failed to parse query - empty response")
            
            logger.debug(f"LLM response: {response}")
                
            ticker = self.extract_ticker(response)
            start_date, end_date = self.extract_dates(response)
            timeframe = self.extract_timeframe(response)
            
            if not ticker:
                logger.error("No valid ticker found in query")
                raise ValueError("No valid ticker found in query")
                
            parsed_result = {
                "ticker": ticker,
                "start_date": start_date,
                "end_date": end_date,
                "timeframe": timeframe
            }
            logger.info(f"Successfully parsed query: {parsed_result}")
            return parsed_result
        
        except Exception as e:
            logger.error(f"Error parsing query: {str(e)}")
            raise

    def extract_ticker(self, text: str) -> str:
        match = re.search(r'\b[A-Z]{1,5}\b', text)
        return match.group(0) if match else ""

    def extract_dates(self, text: str) -> (str, str):
        dates = re.findall(r'\d{4}-\d{2}-\d{2}', text)
        return dates[0] if len(dates) > 0 else "", dates[1] if len(dates) > 1 else ""

    def extract_timeframe(self, text: str) -> str:
        match = re.search(r'\b(daily|weekly|monthly)\b', text.lower())
        return match.group(0) if match else "daily"