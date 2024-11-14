import os

import openai
from dotenv import load_dotenv

load_dotenv()


_PROMPT_TEMPLATE = """You are an expert in Nepali law. You will answer user queries in Nepali language. Please provide clear, concise, and accurate information. You should give useful legal advice and references. 
Only use your knowledge to craft the answer from the given context, add details if you know any and make it clear and comprehensive.
If you need full context to answer some questions, respectfully respond with that but don't try to give incomplete answer. The answer should strictly be given in Nepali. 
Context: {context}

Customer Question is listed in triple backticks.

```{question}```

Your Helpful Answer:

"""


_PROMPT_TEMPLATE_MARKDOWN = """
    CONTEXT: {context}
    You are a helpful assistant, above is some context, 
    Please answer the question, and make sure you follow ALL of the rules below:
    1. Answer the questions only based on context provided, do not make things up
    2. Answer questions in a helpful manner that straight to the point, with clear structure & all relevant information that might help users answer the question
    3. If there are relevant images, video, links, they are very important reference data, please include them as part of the answer
    4. The answer should strictly be given in Japanese. 

    QUESTION: {question}
    ANSWER (formatted in bullet points):
    """

class ResponseLLM:

    def __init__(
            self, 
            context: str, 
            question: str,
            prompt: str = _PROMPT_TEMPLATE_MARKDOWN,
            prompt_markdown: str = _PROMPT_TEMPLATE_MARKDOWN
            ) :
        

        prompt = prompt.format(
            context=context,
            question=question

        )

        self.prompt_markdown = prompt_markdown.format(
            context=context,
            question=question
        )

        self.knowledge = context
        self.prompt = prompt
        


    
    def _generate(self):
        """Call out to OpenAI's endpoint."""
  
        if len(os.environ["OPENAI_API_KEY"])>0:


            openai.api_key = os.environ["OPENAI_API_KEY"]
            response = openai.chat.completions.create(
                                        model="gpt-4o",
                                        messages=[
                                            {"role": "user", "content": (self.prompt)},        
                                        ], 
                                        temperature=0.5,
                                        )

        
        return response.choices[0].message.content
    
    def generate_markdown(self):
        """Call out to OpenAI's endpoint."""
  
        if len(os.environ["OPENAI_API_KEY"])>0:


            openai.api_key = os.environ["OPENAI_API_KEY"]
            response = openai.chat.completions.create(
                                        model="gpt-3.5-turbo",
                                        messages=[
                                            {"role": "user", "content": (self.prompt_markdown)},        
                                        ], 
                                        temperature=0.5,
                                        )

        
        return response.choices[0].message.content

if __name__=="__main__":

    context = 'ram studies in tai inc.'
    question = "where do ram study?"

    llm = ResponseLLM(
        context=context,
        question=question,
    )
    print(llm._generate())
