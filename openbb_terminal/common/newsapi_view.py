""" News View """
__docformat__ = "numpy"

import os
import logging
<<<<<<< HEAD
import os
=======
>>>>>>> d4d3207c7a (?)
from typing import Optional

import pandas as pd

from openbb_terminal.common import newsapi_model
<<<<<<< HEAD
from openbb_terminal.decorators import check_api_key, log_start_end
from openbb_terminal.helper_funcs import export_data, print_rich_table
=======
from openbb_terminal.decorators import log_start_end
from openbb_terminal.helper_funcs import export_data
from openbb_terminal.helper_funcs import print_rich_table
>>>>>>> d4d3207c7a (?)

logger = logging.getLogger(__name__)


@log_start_end(log=logger)
@check_api_key(["API_NEWS_TOKEN"])
def display_news(
    query: str,
    limit: int = 3,
    start_date: Optional[str] = None,
    show_newest: bool = True,
    sources: str = "",
    export: str = "",
<<<<<<< HEAD
    sheet_name: Optional[str] = None,
=======
>>>>>>> d4d3207c7a (?)
) -> None:
    """Prints table showing news for a given term. [Source: NewsAPI]

    Parameters
    ----------
    query : str
        term to search on the news articles
    start_date: Optional[str]
        date to start searching articles from formatted YYYY-MM-DD
    limit : int
        number of articles to display
    show_newest: bool
        flag to show newest articles first
    sources: str
        sources to exclusively show news from
    export : str
        Export dataframe data to csv,json,xlsx file
    """
    tables = newsapi_model.get_news(query, limit, start_date, show_newest, sources)
    if tables:
        for table in tables:
            print_rich_table(table[0], title=table[1]["title"])

    export_data(
        export,
        os.path.dirname(os.path.abspath(__file__)),
        f"news_{query}_{'_'.join(sources)}",
        pd.DataFrame(tables),
<<<<<<< HEAD
        sheet_name,
    )
=======
    )
>>>>>>> d4d3207c7a (?)
