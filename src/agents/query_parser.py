# src/agents/query_parser.py
import logging
from typing import Dict, Optional
import re
from dateutil import parser as date_parser
from openai import OpenAI
from config.settings import OPENAI_API_KEY

logger = logging.getLogger(__name__)

class QueryParser:
    def __init__(self):
        logger.info("Initializing QueryParser with OpenAI API")
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def parse_query(self, query: str) -> Dict[str, str]:
        logger.info(f"Parsing query: {query}")
        try:
            logger.debug("Invoking OpenAI ChatCompletion API")
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": """
                    You are a financial query parser that extracts and translates information from natural language queries.
                    You must interpret relative date references and convert them to actual dates in YYYY-MM-DD format.
                    You must be able to find the ticker if instead of the stock symbol, the company name is mentioned.
                    
                    Examples of date translations:
                    - "last month" -> Start: First day of previous month, End: Last day of previous month
                    - "this year" -> Start: First day of current year, End: Today
                    - "last 6 months" -> Start: Date 6 months ago, End: Today
                    - "2023" -> Start: 2023-01-01, End: 2023-12-31
                     
                    If you are unable to determine the exact date, return the closest possible date range.
                     
                    If you are unable to determine the Timeframe, return the default Timeframe as "daily".
                    
                    Return information in this exact format:
                    - Ticker: [SYMBOL]
                    - Start Date: [YYYY-MM-DD]
                    - End Date: [YYYY-MM-DD]
                    - Timeframe: [daily/weekly/monthly]
                    """},
                    {"role": "user", "content": query}
                ],
                max_tokens=150,
                temperature=0.5
            )

            if not response or not response.choices:
                logger.error("Empty response from OpenAI ChatCompletion API")
                raise ValueError("Failed to parse query - empty response")

            logger.debug(f"OpenAI response: {response.choices[0].message.content}")

            extracted_info = response.choices[0].message.content.strip()

            parsed_result = {
                "ticker": self.extract_ticker(extracted_info),
                "start_date": self.extract_start_date(extracted_info),
                "end_date": self.extract_end_date(extracted_info),
                "timeframe": self.extract_timeframe(extracted_info)
            }

            # Validate parsed results
            if not parsed_result["ticker"]:
                logger.error("No valid ticker found in query")
                raise ValueError("No valid ticker found in query")

            logger.info(f"Successfully parsed query: {parsed_result}")
            return parsed_result

        except Exception as e:
            logger.error(f"Error parsing query: {str(e)}")
            raise

    def extract_ticker(self, response: str) -> Optional[str]:
        logger.debug("Extracting ticker from response")
        match = re.search(r'\b[A-Z]{1,5}\b', response)
        ticker = match.group(0) if match else None
        logger.debug(f"Extracted ticker: {ticker}")
        return ticker

    def extract_start_date(self, response: str) -> Optional[str]:
        logger.debug("Extracting start date from response")
        try:
            dates = re.findall(r'\b\d{4}-\d{2}-\d{2}\b', response)
            return dates[0] if dates else None
        except Exception as e:
            logger.error(f"Error extracting start date: {str(e)}")
            return None

    def extract_end_date(self, response: str) -> Optional[str]:
        logger.debug("Extracting end date from response")
        try:
            dates = re.findall(r'\b\d{4}-\d{2}-\d{2}\b', response)
            return dates[1] if len(dates) > 1 else None
        except Exception as e:
            logger.error(f"Error extracting end date: {str(e)}")
            return None

    def extract_timeframe(self, response: str) -> Optional[str]:
        logger.debug("Extracting timeframe from response")
        match = re.search(r'\b(daily|weekly|monthly)\b', response, re.IGNORECASE)
        timeframe = match.group(0).lower() if match else None
        logger.debug(f"Extracted timeframe: {timeframe}")
        return timeframe