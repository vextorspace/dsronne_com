import os
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

class AiLibrarian:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0.1,
            max_tokens=1024,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )

    def question_stoics(self, question):
        print(f"API Key loaded: {'Yes' if os.getenv('OPENAI_API_KEY') else 'No'}")

        prompt_template = """                                                                                                                                                             
                            You are a stiff and proud librarian.
                            You do not allow your own biases influence your answers.
                            You simply refer a person to the most appropriate passage from a genuine stoic that has wisdom about the question.
                            
                            Question: {question} 
                        """

        question_prompt = ChatPromptTemplate.from_template(prompt_template)

        # Create the chain
        question_chain = question_prompt | self.llm

        # Run the chain
        answer = question_chain.invoke({"question": question})
        return answer.content.strip()
