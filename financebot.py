import streamlit as st
from openai import OpenAI
from tenacity import retry, wait_random_exponential, stop_after_attempt
from alpha_vantage.openai import tools as openai_tools
from st_clients import AlphaVantageStClient 
import json

GPT_MODEL = "gpt-4o-mini"
openai_client = OpenAI()
client = AlphaVantageStClient()

OPEN_AI_REQUEST_COUNT = "openai_request_count"
ALPHA_VANTAGE_REQUEST_COUNT = "alpha_vantage_request_count"

api_function_mapping = {
    'get_time_series_daily': 'TIME_SERIES_DAILY',
    'get_company_overview': 'OVERVIEW',
    'get_stock_quote': 'GLOBAL_QUOTE'
}

@retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
def chat_completion_request(messages, tools=None, tool_choice=None, model=GPT_MODEL):
    try:
        response = openai_client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice=tool_choice,
        )
        st.session_state[OPEN_AI_REQUEST_COUNT] += 1
        return response
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return e
    
st.title("Finance Bot")
st.caption("A Streamlit chatbot powered by OpenAI and Alpha Vantage")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

if OPEN_AI_REQUEST_COUNT not in st.session_state:
    st.session_state[OPEN_AI_REQUEST_COUNT] = 0
if ALPHA_VANTAGE_REQUEST_COUNT not in st.session_state:
    st.session_state[ALPHA_VANTAGE_REQUEST_COUNT] = 0

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    messages = [{"role": "user", "content": prompt}]
    response = chat_completion_request(
        messages, tools=openai_tools
    )

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    response_message = response.choices[0].message 
    messages.append(response_message)

    tool_calls = response_message.tool_calls
    if tool_calls:
        tool_call_id = tool_calls[0].id
        tool_function_name = tool_calls[0].function.name
        tool_symbol_string = json.loads(tool_calls[0].function.arguments)['symbol']

        chain_of_thought_msg = "Using Alpha Vantage API to fetch data using "
        
        print(tool_function_name)
        if tool_function_name == 'get_company_overview':
            results = str(client.get_company_overview(tool_symbol_string))
        elif tool_function_name == 'get_stock_quote':
            results = str(client.get_stock_quote(tool_symbol_string))
        elif tool_function_name == 'get_time_series_daily':
            results = str(client.get_time_series_daily(tool_symbol_string))
        else: 
            print(f"Error: function {tool_function_name} does not exist")
            exit(2)

        
        messages.append({
            "role":"tool", 
            "tool_call_id":tool_call_id,
            "name": tool_function_name, 
            "content":results
        })

        chain_of_thought_msg += (api_function_mapping[tool_function_name] + " for " + tool_symbol_string) 
        st.chat_message("assistant").write(chain_of_thought_msg)

        response = chat_completion_request(
            messages, tools=openai_tools
        )
        msg = response.choices[0].message.content

        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)
    else: 
        print(messages)
        st.session_state.messages.append({"role": "assistant", "content": response_message.content})
        st.chat_message("assistant").write(response_message.content)


st.sidebar.title("Request Stats")
st.sidebar.write(f"Number of OpenAI requests sent: {st.session_state[OPEN_AI_REQUEST_COUNT]}")
st.sidebar.write(f"Number of AlphaVantage requests sent: {st.session_state[ALPHA_VANTAGE_REQUEST_COUNT]}")



