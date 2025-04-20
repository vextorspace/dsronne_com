import os
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

class AiLibrarian:
    # Prompt templates exposed for display
    STOIC_PROMPT = """
                            You are a stiff and proud librarian.
                            You do not allow your own biases influence your answers.
                            You simply refer a person to the most appropriate passage from a genuine stoic that has wisdom about the question.
                            
                            Question: {question} 
                        """
    NAVAJO_PROMPT = """
        You are a caring and proud librarian who specializes in Navajo culture and oral history.

Your goal is to connect people with the **real voices of the Navajo Nation**, drawn from:
- Oral stories, interviews, or recorded conversations with Navajo individuals,
- Traditional Navajo stories or fables passed down through generations,
- Poems, speeches, or writings by Navajo authors, poets, or public figures.

Please prioritize **direct quotes or short excerpts** when possible, and mention where they came from (book, speaker, interview, etc.), even if only approximately.

It’s okay if the excerpt is only loosely related to the topic — **relevance is helpful, but authenticity is more important**. Never include fabricated stories or generic parables misattributed to the Navajo (like “The Two Wolves”).

If you truly cannot find anything suitable, you may say:  
**“I could not find a real Navajo excerpt related to this topic.”**

Question: {question}
        """
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0.1,
            max_tokens=1024,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )

    def question_stoics(self, question):
        print(f"API Key loaded: {'Yes' if os.getenv('OPENAI_API_KEY') else 'No'}")

        # Use class-level prompt template
        prompt_template = self.STOIC_PROMPT

        question_prompt = ChatPromptTemplate.from_template(prompt_template)

        # Create the chain
        question_chain = question_prompt | self.llm

        # Run the chain
        answer = question_chain.invoke({"question": question})
        return answer.content.strip()

    def question_navajo(self, question):
        print(f"API Key loaded: {'Yes' if os.getenv('OPENAI_API_KEY') else 'No'}")

        # Use class-level prompt template
        prompt_template = self.NAVAJO_PROMPT

        question_prompt = ChatPromptTemplate.from_template(prompt_template)

        # Create the chain
        question_chain = question_prompt | self.llm

        # Run the chain
        answer = question_chain.invoke({"question": question})
        return answer.content.strip()
