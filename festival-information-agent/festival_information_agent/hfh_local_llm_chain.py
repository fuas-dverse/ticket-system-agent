from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_huggingface import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

load_dotenv()

prompt = PromptTemplate.from_template(
    """Answer the question based only on the following context: {context}
    Question: {question}"""
)

# model_id = "google/flan-t5-large"
# tokenizer = AutoTokenizer.from_pretrained(model_id)
# model = AutoModelForSeq2SeqLM.from_pretrained(model_id)
#
# pipe = pipeline(
#     "text2text-generation",
#     model=model,
#     tokenizer=tokenizer,
#     max_length=100
# )
#
# local_llm = HuggingFacePipeline(pipeline=pipe)

hf = HuggingFacePipeline.from_model_id(
    model_id="google/flan-t5-large",
    task="text2text-generation",
    pipeline_kwargs={"max_new_tokens": 100},
)

chain = (
        RunnableParallel({
            "context": str,
            "question": RunnablePassthrough()
        })
        | prompt
        | hf
        | StrOutputParser()
)

print(chain.invoke({
    "context": "Paris is the capitol of France",
    "question": "What is the capitol of France?"
}))
