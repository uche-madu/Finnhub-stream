from unittest.mock import patch
from finnhub_producer import create_news_dict, stream_company_news


def test_create_news_dict():
    news_item = {
        "category": "tech",
        "datetime": 1609502400,
        "headline": "Test Headline",
        "id": 12345,
        "image": "http://example.com/image.jpg",
        "related": "AAPL",
        "source": "Test Source",
        "summary": "Test Summary",
        "url": "http://example.com/news",
    }

    expected_result = news_item.copy()
    result = create_news_dict(news_item)
    assert result == expected_result


@patch("finnhub.Client", spec=True)
def test_stream_company_news(mock_finnhub_client):
    mock_finnhub_client.return_value.company_news.return_value = [
        {
            "category": "tech",
            "datetime": 1609502400,
            "headline": "Test Headline",
            "id": 12345,
            "image": "http://example.com/image.jpg",
            "related": "AAPL",
            "source": "Test Source",
            "summary": "Test Summary",
            "url": "http://example.com/news",
        }
    ]

    companies = ["AAPL"]
    news_generator = stream_company_news(companies)
    news_list = list(news_generator)

    assert len(news_list) == 1
    assert news_list[0]["category"] == "tech"
    assert news_list[0]["datetime"] == 1609502400
