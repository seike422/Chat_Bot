# Chat_Bot

This is a chatbot project that utilizes iexfinance api to check for stock price.

## Installation
There are some necessary modules to install.

[spaCy](https://spacy.io/) is an open-source software library for advanced natural language processing. To install spaCy,

```bash
pip install spacy
```

To download the English package,

```bash
python -m spacy download en
```
[Rasa NLU](https://rasa.com/docs/rasa/nlu/about/) is a library for intent recognition and entity extraction. It is based on spaCy, scikit-learn and other libraries. To install Rasa LNU,

```bash
pip install rasa
pip install rasa_nlu
```

[iexfinance](https://addisonlynch.github.io/iexfinance/stable/index.html) is an API for providing stock market information. To install,

```bash
pip install iexfinance
```
The python version is 3.6 for this project.

## Usage

```python
python3 stock_chat.py
```

## Sample Dialogue

## Features

The program uses regular expressions to recognize intents and exercises. Specifically, it uses regex to search to create a pattern if the keywords occur.

In order to train word vectors, it uses the spaCy libraries. 
It provides a training dataset stock_training.json to train the data.
Rasa pipeline is provided by config_spacy.yml.

A state machine is implemented, which contains six states.

## Sample Dialogue

User: Hi

Bot: Hey there, Can I have your name?

User: Jessie

Bot: Hi, Jessie, I can tell you about stock market, such as price, volume and market cap!


User: I'm looking for stock information of companies.

Bot: Which company do you want to know about?

User: apple company

Bot: What information do you want to know from apple company?

User: show me current price

Bot: Current Stock Price is ..., Anything else?

User: how about volume

Bot: The latest Volume is ..., Anything else?

User: No

Bot: goodbye 
