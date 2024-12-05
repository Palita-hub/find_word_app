import openai
import streamlit as st
import requests

# Streamlit app title
st.title("Find Word Meaning")

# Sidebar for API key input
api_key = st.sidebar.text_input("Enter your OpenAI API key:", type="password")
openai.api_key = api_key

# User input for the word
word = st.text_input("What word are you looking for?")

# Function to get word meaning from OpenAI API
def get_word_meaning(word):
    if not api_key:
        st.error("Please enter your API key in the sidebar.")
        return None

    if not word:
        st.warning("Enter a word to search for its meaning.")
        return None

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use "gpt-4" if available
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"What is the meaning of '{word}'?"},
            ],
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        st.error(f"Error: {e}")
        return None

# Display result if the user inputs a word
if st.button("Find Meaning"):
    if word:
        meaning = get_word_meaning(word)
        if meaning:
            st.markdown(f"### Meaning of **{word}**:")
            st.write(meaning)
    else:
        st.warning("Please enter a word!")

# Optional: Add a secondary API for redundancy
def find_word_meaning_api(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Word not found or API issue."}

# Optionally use this function if primary API fails
if st.button("Find Meaning (Alternative API)"):
    result = find_word_meaning_api(word)
    if "error" in result:
        st.error(result["error"])
    else:
        st.write(result)
