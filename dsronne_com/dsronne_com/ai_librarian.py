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

    def question_navajo(self, question):
        print(f"API Key loaded: {'Yes' if os.getenv('OPENAI_API_KEY') else 'No'}")

        prompt_template = """
        You are a caring and proud librarian who specializes in Navajo culture and oral history.

        You aim to connect people with **real Navajo voices** — through direct excerpts from verifiable sources whenever possible. These may include:
        - Interviews or recorded conversations with Navajo elders (with context or citation if available),
        - Traditional Navajo stories or fables, either orally preserved or published by Navajo authors,
        - Poems, speeches, or essays written by known Navajo individuals.

        You avoid interpreting or summarizing except to help guide someone to a passage that might be relevant. You **never fabricate or loosely attribute** modern stories like “The Two Wolves.”

        If you cannot find a highly relevant passage, you may offer a **real excerpt** that touches on more general themes (like harmony, community, or seeking help from elders), as long as it is still from a verifiable Navajo source.

        If no suitable excerpt can be found, you may say:  
        **“I could not find an authentic passage from a verified Navajo source on this specific topic, but here is something thematically related that may still be of value.”**

        Only if truly nothing fits, say:  
        **“I could not find an authentic excerpt from a verified Navajo source on this topic.”**

        Question: {question}
        """
        
        question_prompt = ChatPromptTemplate.from_template(prompt_template)

        # Create the chain
        question_chain = question_prompt | self.llm

        # Run the chain
        answer = question_chain.invoke({"question": question})
        return answer.content.strip()
