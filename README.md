# Finance LLM Bot

This bot uses OpenAI `GPT-4o-mini` that answers finance-specific questionsusing [function calling](https://platform.openai.com/docs/guides/function-calling) to utilize [Alpha Vantage API](https://www.alphavantage.co/documentation/) 

Built with [Streamlit](https://streamlit.io/).

## Requirements

It uses the [finance-llm-tool](https://github.com/RohanNankani/finance_llm_tools) for Alpha Vantage Client and also the function tools for the llm to use. 

```bash
cd finance_llm_tools 
pip install -e .
```


## Usage 

```bash
pip install -f requirements.txt
streamlit run financebot.py
```

