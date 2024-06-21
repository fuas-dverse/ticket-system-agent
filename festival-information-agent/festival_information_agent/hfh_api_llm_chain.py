from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_huggingface import HuggingFaceEndpoint

load_dotenv()

prompt = PromptTemplate.from_template(
    """Answer the question based only on the following context: {context}
    Question: {question}"""
)

model = HuggingFaceEndpoint(
    repo_id="google/flan-t5-xxl",
    temperature=0.8,
    top_k=50,
)

chain = (
        RunnableParallel({
            "context": str,
            "question": RunnablePassthrough()
        })
        | prompt
        | model
        | StrOutputParser()
)

print(chain.invoke({
    "context": "Paris is the capitol of France",
    "question": "What is the capitol of France?"
}))
