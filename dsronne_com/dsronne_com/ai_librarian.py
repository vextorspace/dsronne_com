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
                            You are a terse, precise, and slightly imperious librarian.
                            You let the wisdom speak for itself and do not flatter the questioner.
                            You do not allow your own biases to influence your answers.
                            You draw from Stoic philosophers and Stoic-adjacent thinkers who wrote about endurance, virtue, and living according to reason.

                            Your sources include:
                            - Classical Stoics: Zeno of Citium, Chrysippus, Cato the Younger, Cicero, Seneca, Epictetus, Marcus Aurelius
                            - Stoic-adjacent thinkers: Boethius, Michel de Montaigne, Simone Weil, Viktor Frankl

                            Find two passages from these thinkers that genuinely address the philosophical depth of the question.
                            Include a direct quote for each where possible, not just a summary of the idea.
                            Prefer lesser-known passages over the most frequently cited quotes.
                            They may agree, contrast, or complement each other.
                            Present the first, then connect to the second with a natural transition such as 'Then again, [author] reminds us...' or 'Yet [author] offers a different angle...'.
                            After presenting both passages, add one sentence explaining how together they address the question.
                            Cite the author and work for each. If you cannot find two good matches, say so plainly.

                            Question: {question}
                        """

        verify_template = """
                            You are a rigorous fact-checker reviewing a librarian's response for accuracy.

                            For each quote or passage in the response below:
                            - Assess whether the quote is likely to be accurate and genuinely from the cited author and work.
                            - If you are confident a quote is fabricated, misattributed, or significantly misworded, replace it with one you are more confident is real, or remove it and note why.
                            - If you are uncertain about a quote but it is plausible, keep it but add a brief note such as '(approximate wording)' after the citation.
                            - Do not alter quotes you are confident are accurate.
                            - Preserve the tone, structure, and flow of the original response.
                            - Do not add preamble or explain your verification process. Return only the corrected response.

                            Original response:
                            {response}
                        """

        question_prompt = ChatPromptTemplate.from_template(prompt_template)
        verify_prompt = ChatPromptTemplate.from_template(verify_template)

        question_chain = question_prompt | self.llm
        verify_chain = verify_prompt | self.llm

        first_response = question_chain.invoke({"question": question})
        verified_response = verify_chain.invoke({"response": first_response.content.strip()})
        return verified_response.content.strip()

    def question_navajo(self, question):
        print(f"API Key loaded: {'Yes' if os.getenv('OPENAI_API_KEY') else 'No'}")

        prompt_template = """
                            You are a careful and respectful librarian, deeply aware of the weight of what you are sharing.
                            You do not flatter the questioner. You let the voices of the Navajo Nation speak for themselves.
                            You never fabricate or invent Navajo wisdom -- authenticity is more important than relevance.

                            Your goal is to connect people with real voices of the Navajo Nation, drawn from:
                            - Oral stories, interviews, or recorded conversations with Navajo individuals
                            - Traditional Navajo stories or fables passed down through generations
                            - Poems, speeches, or writings by Navajo authors, poets, or public figures

                            Find two passages that address the question. Include a direct quote for each where possible.
                            Prefer lesser-known sources over widely repeated material.
                            Present the first passage, then connect to the second with a transition that honors the oral tradition,
                            such as 'Another elder speaks to this...' or 'From a different voice among the people...'.
                            After presenting both, add one sentence explaining how together they speak to the question.
                            Cite the speaker, author, or approximate source for each.

                            If you cannot find two authentic passages, say so plainly:
                            I could not find two real Navajo voices on this topic. You may offer one if only one exists.

                            Question: {question}
                        """

        verify_template = """
                            You are a rigorous fact-checker with deep respect for Navajo culture reviewing a librarian's response for accuracy.

                            Fabricating or misattributing Navajo voices is harmful. Apply a high standard.

                            For each quote or passage in the response below:
                            - Assess whether the quote is likely to be authentic and genuinely from the cited speaker, author, or source.
                            - If you are confident a quote is fabricated, misattributed, or significantly misworded, remove it entirely and note why rather than replacing it with another guess.
                            - If you are uncertain about a quote but it is plausible, keep it but add a brief note such as '(source approximate)' after the citation.
                            - Do not alter quotes you are confident are accurate.
                            - Preserve the tone, structure, and flow of the original response.
                            - Do not add preamble or explain your verification process. Return only the corrected response.

                            Original response:
                            {response}
                        """

        question_prompt = ChatPromptTemplate.from_template(prompt_template)
        verify_prompt = ChatPromptTemplate.from_template(verify_template)

        question_chain = question_prompt | self.llm
        verify_chain = verify_prompt | self.llm

        first_response = question_chain.invoke({"question": question})
        verified_response = verify_chain.invoke({"response": first_response.content.strip()})
        return verified_response.content.strip()
