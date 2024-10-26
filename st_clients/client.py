from alpha_vantage import AlphaVantageClient 
import streamlit as st

ALPHA_VANTAGE_REQUEST_COUNT = "alpha_vantage_request_count"

class AlphaVantageStClient:

    def __init__(self):
        self.client = AlphaVantageClient()
    
    def update_request_counter(self):
        st.session_state[ALPHA_VANTAGE_REQUEST_COUNT] += 1 

    @st.cache_data(ttl=86400)
    def get_time_series_daily(_self, symbol):
        """
        Fetches the time series data for a given stock symbol.
        """
        _self.update_request_counter()
        return _self.client.get_time_series_daily(symbol)

    @st.cache_data(ttl=86400)
    def get_company_overview(_self, symbol):
        """
        Fetches the company overview for a given stock symbol.
        """
        _self.update_request_counter()
        return _self.client.get_company_overview(symbol)

    @st.cache_data(ttl=86400)
    def get_stock_quote(_self, symbol):
        """
        Fetches the stock quote for a given stock symbol.
        """
        _self.update_request_counter()
        return _self.client.get_stock_quote(symbol)