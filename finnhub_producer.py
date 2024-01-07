import argparse
import os
from typing import Any, Dict, Generator, List
import finnhub
from utils import logger
from dotenv import load_dotenv
import confluent_kafka  # noqa: F401

load_dotenv()

logger = logger(log_file="news.log", stream=False)

finnhub_api_key = os.getenv("FINNHUB_API_KEY")


def create_news_dict(news_item: Dict[str, Any]) -> Dict[str, Any]:
    """Create a dictionary representation of a news item.

    Args:
        news_item (Dict[str, Any]): A dictionary containing news item details.

    Returns:
        Dict[str, Any]: A dictionary with structured news item data.
    """
    return {
        "category": news_item.get("category"),
        "datetime": news_item.get("datetime"),
        "headline": news_item.get("headline"),
        "id": news_item.get("id"),
        "image": news_item.get("image"),
        "related": news_item.get("related"),
        "source": news_item.get("source"),
        "summary": news_item.get("summary"),
        "url": news_item.get("url"),
    }


def stream_company_news(
    companies: List[str], start_date: str = "2023-06-01", end_date: str = "2024-06-10"
) -> Generator[Dict[str, Any], None, None]:
    """Stream news data for given companies within a specified date range.

    Args:
        companies (List[str]): A list of company symbols.
        start_date (str): The start date for news retrieval.
        end_date (str): The end date for news retrieval.

    Yields:
        Generator[Dict[str, Any], None, None]: A generator yielding news data dictionaries.
    """
    try:
        finnhub_client = finnhub.Client(api_key=finnhub_api_key)
        for company in companies:
            company_news = finnhub_client.company_news(
                company, _from=start_date, to=end_date
            )
            # Yield all news items for each company at once
            yield from (create_news_dict(news) for news in company_news)

            logger.info(f"Retrieved {len(company_news)} news events for {company}.")
    except Exception as e:
        logger.exception(
            f"An exception occurred while trying to retrieve data from the Finnhub API: {e}"
        )


def main():
    """Main function to parse arguments and stream company news."""
    parser = argparse.ArgumentParser(description="Stream company news from Finnhub.")
    parser.add_argument("companies", nargs="+", help="List of company symbols")
    parser.add_argument(
        "--start_date", default="2023-06-01", help="Start date for news retrieval"
    )
    parser.add_argument(
        "--end_date", default="2024-06-10", help="End date for news retrieval"
    )

    args = parser.parse_args()

    for news_dict in stream_company_news(
        args.companies, args.start_date, args.end_date
    ):
        # Process each news_dict here
        # For example, you can save it to a database, send it to another service, etc.
        # Here, just printing as an example
        logger.info(news_dict)


if __name__ == "__main__":
    main()
