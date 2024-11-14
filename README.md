# chat-web
Making chatbots better.


# How to run this?
1. Clone this repository. 
2. Install all the required python libraries using the command given below.
```pip install -r requirements.txt```

3. Export the OPENAI API key to your os environment. 
```export OPENAPI_KEY = "YOUR KEY HERE"```
4. Run the following code from your terminal.
```streamlit run main.py``` 
5. If you want to serve the model locally and the project. Please follow the steps mentioned below.



# Serve models locally
We can serve models locally using Ollama. 
1. Download the Ollama of your OS. Currently, it is not available for Windows. 
https://ollama.com/download
```curl -fsSL https://ollama.com/install.sh | sh```

2. Check the documentation below to find out how to download the model that is required. 
https://github.com/ollama/ollama
Example, running the command below will downloadn the llama2 model the first time and host it in the locahost. 
```ollama run llama2```
3. The models are hosted in the port mentioned below: 
 http://localhost:11434/api/generate
 Enjoy!


