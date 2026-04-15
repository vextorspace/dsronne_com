import os
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from tavily import TavilyClient

class AiLibrarian:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-5",
            temperature=0.1,
            max_tokens=2048,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        self.verifier_llm = ChatOpenAI(
            model="gpt-5",
            temperature=0.1,
            max_tokens=2048,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        self.tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

    def _search(self, query, max_results=5):
        results = self.tavily.search(query=query, max_results=max_results)
        excerpts = []
        for r in results.get("results", []):
            excerpts.append(f"- {r.get('title', '')}: {r.get('content', '')}")
        return "\n".join(excerpts)

    def question_stoics(self, question):
        print(f"API Key loaded: {'Yes' if os.getenv('OPENAI_API_KEY') else 'No'}")

        retrieval_context = self._search(f"stoic philosophy quotes {question}")

        prompt_template = """
                            You are a terse, precise, and slightly imperious librarian.
                            You let the wisdom speak for itself and do not flatter the questioner.
                            You do not allow your own biases to influence your answers.
                            You draw from Stoic philosophers and Stoic-adjacent thinkers who wrote about endurance, virtue, and living according to reason.

                            Your sources include:
                            - Classical Stoics: Zeno of Citium, Chrysippus, Cato the Younger, Cicero, Seneca, Epictetus, Marcus Aurelius
                            - Stoic-adjacent thinkers: Boethius, Michel de Montaigne, Simone Weil, Viktor Frankl

                            The following search results may help you find real passages. Use them as a guide but apply your own judgment:
                            {context}

                            Find five candidate passages from these thinkers that address the philosophical depth of the question.
                            Include a direct quote for each where possible, not just a summary of the idea.
                            Prefer lesser-known passages over the most frequently cited quotes.
                            Number each passage and cite the author and work.
                            Do not connect them yet -- just list all five candidates.

                            Question: {question}
                        """

        verify_template = """
                            You are a rigorous fact-checker reviewing a librarian's list of candidate passages for accuracy.

                            The following search results are provided to help you verify the quotes:
                            {context}

                            For each of the five candidate passages below:
                            - If search results confirm the quote, mark it as verified.
                            - If you are confident a quote is fabricated, misattributed, or significantly misworded, remove it.
                            - If you are uncertain but it is plausible, keep it and add '(approximate wording)' after the citation.

                            From the passages that survive verification, select the best two that together most deeply address the question.
                            They may agree, contrast, or complement each other.
                            Present the first, then connect to the second with a natural transition such as 'Then again, [author] reminds us...' or 'Yet [author] offers a different angle...'.
                            After presenting both, add one sentence explaining how together they address the question.
                            If fewer than two survive, present what remains honestly.

                            Do not add preamble or explain your verification process. Return only the final response.

                            Candidate passages:
                            {response}
                        """

        question_prompt = ChatPromptTemplate.from_template(prompt_template)
        verify_prompt = ChatPromptTemplate.from_template(verify_template)

        question_chain = question_prompt | self.llm
        verify_chain = verify_prompt | self.verifier_llm

        first_response = question_chain.invoke({"question": question, "context": retrieval_context})

        verify_context = self._search(f"verify stoic quote {first_response.content.strip()[:200]}")
        verified_response = verify_chain.invoke({
            "response": first_response.content.strip(),
            "context": verify_context
        })
        return verified_response.content.strip()

    def question_navajo(self, question):
        print(f"API Key loaded: {'Yes' if os.getenv('OPENAI_API_KEY') else 'No'}")

        retrieval_context = self._search(f"Navajo Nation quotes wisdom oral history {question}")

        prompt_template = """
                            You are a careful and respectful librarian, deeply aware of the weight of what you are sharing.
                            You do not flatter the questioner. You let the voices of the Navajo Nation speak for themselves.
                            You never fabricate or invent Navajo wisdom -- authenticity is more important than relevance.

                            Your goal is to connect people with real voices of the Navajo Nation, drawn from:
                            - Oral stories, interviews, or recorded conversations with Navajo individuals
                            - Traditional Navajo stories or fables passed down through generations
                            - Poems, speeches, or writings by Navajo authors, poets, or public figures

                            The following search results may help you find real passages. Use them as a guide but apply your own judgment:
                            {context}

                            Find five candidate passages that address the question. Include a direct quote for each where possible.
                            Each candidate must come from a named real person or a specifically identified traditional source.
                            Never include a general description of Navajo philosophy as a candidate.
                            Number each passage and cite the speaker, author, or approximate source.
                            Do not connect them yet -- just list all five candidates.
                            If you cannot find five, list as many as you can find from real named sources.

                            Question: {question}
                        """

        verify_template = """
                            You are a rigorous fact-checker with deep respect for Navajo culture reviewing a librarian's list of candidate passages.

                            Fabricating or misattributing Navajo voices is harmful. Apply a high standard.

                            The following search results are provided to help you verify the quotes:
                            {context}

                            For each candidate passage below:
                            - If search results confirm the quote, mark it as verified.
                            - If a passage comes from a named real person and is plausible, keep it and add '(approximate wording)' after the citation.
                            - If a passage is a general description of Navajo philosophy with no named real person, remove it.
                            - If a passage is clearly invented or wildly misattributed, remove it.

                            From the passages that survive verification, select the best two that together most meaningfully address the question.
                            Present the first passage, then connect to the second with a transition that honors the oral tradition,
                            such as 'Another elder speaks to this...' or 'From a different voice among the people...'.
                            After presenting both, add one sentence explaining how together they speak to the question.
                            If fewer than two survive, present what remains honestly.

                            Do not add preamble or explain your verification process. Return only the final response.

                            Candidate passages:
                            {response}
                        """

        question_prompt = ChatPromptTemplate.from_template(prompt_template)
        verify_prompt = ChatPromptTemplate.from_template(verify_template)

        question_chain = question_prompt | self.llm
        verify_chain = verify_prompt | self.verifier_llm

        first_response = question_chain.invoke({"question": question, "context": retrieval_context})

        verify_context = self._search(f"verify Navajo quote {first_response.content.strip()[:200]}")
        verified_response = verify_chain.invoke({
            "response": first_response.content.strip(),
            "context": verify_context
        })
        return verified_response.content.strip()
