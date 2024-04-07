# Festival Information Agent Research
In the sixth semester at Fontys, we are creating a group project called [Dverse,](https://fuas-dverse.github.io/) The main goal of this project is to create a system where different agents can work together. Our individual is creating one or more of those agents that can complete tasks in the group project's system. To get a better understanding of what actually is needed to create such an agent, we created a design challenge research question with multiple sub questions. This research paper will be written to search for the answer to a sub question.

## Research
What technology or strategy should the system use to recommend the festival goers a festival with the highest match to their user's preferences?

### Context
Our initial idea was to create an agent that used the Chat-GPT 4 API to search the web for relevant information about a prompted festival. As we already checked if this was possible inside the Chat-GPT 4 interface, which it was. But as we tried to do this via the API of Open AI, it did not seem to work anymore. After doing some searching on the internet why this was the case, we discovered that the feature to search the web with Chat-GPT 4 was only present in the interface (for paying user's). And that they used their own logic to integrate the Bing Search API to get data from the internet.

While looking if we could create a similar function that searches the web, we also tried using the Bing Search API, as this is a free alternative to the Google Search API. But our organization blocked this feature. 

After discovering that creating our own function was not an option, we decided to create a web scrapper in Python that uses Beautiful Soup 4 to get festival information from a website. We then stored the data of the festivals inside our own database. So, the research will specifically look into how we can fetch the data from the database based on a prompt given by the user and then feed it to our Open AI API to return a human like answer.

### Library

#### Available product analysis
To answer this question, I first will ask a question to Perplexity AI, which is an AI that can search the web and summarize the found articles into one complete answer.
- Prompt: Getting data from database based on similarity
- Answer: ([complete answer](https://www.perplexity.ai/search/Getting-data-from-Ie_I8UurQ0mzpLaPCMI0IA))
	- Vector Embeddings
	- Indexing and Similarity Search
	- Querying for Similar Rows

After having a first idea, I will prompt Google the same that I asked Perplexity AI.
- Prompt: Getting data from database based on similarity
- Answer: 
	- [Find Similar Rows in Database](https://stackoverflow.com/questions/3829188/find-similar-rows-in-database)
	- [How vector similarity search works](https://labelbox.com/blog/how-vector-similarity-search-works/)
	- [How Vector Databases Search by Similarity: A Comprehensive Primer](https://medium.com/kx-systems/how-vector-databases-search-by-similarity-a-comprehensive-primer-c4b80d13ce63)
	- [Similarity Search, Part 2: Product Quantization](https://towardsdatascience.com/similarity-search-product-quantization-b2a1a6397701)

These links are the first four articles that I got back from Google, where the first one is ruled out as it is a Stack Overflow question from 13 years ago and is not up-to-date with the whole AI uprising. For me, it's pretty clear that from these search results, the Vector Databases are the most efficient way of similarity searching a database.

So the next questions that I will look into is, how to feed fetched data to the context of a LLM (Large Language Model)?

Again, I will first prompt Perplexity AI, to get a starting point for this question.
- Prompt: How to add up-to-date context to a large language model
- Answer: ([complete answer](https://www.perplexity.ai/search/How-to-add-idPkL9BtQv.BeCxqSU1WAw))
	- Retrieval-Augmented Generation (RAG)
	- In-Context Learning
	- Fine-tuning

Then, after having asked Perplexity AI, I will ask Google again with the same prompt.
- Prompt: How to add up-to-date context to a large language model
- Answer:
	- [Giving Large Language Models Context](https://medium.com/@simon_attard/giving-large-language-models-context-2d1956a6a017)
	- [In-Context Learning Approaches in Large Language Models](https://towardsdatascience.com/in-context-learning-approaches-in-large-language-models-9c0c53b116a1)
	- [Fine-tuning large language models (LLMs) in 2024](https://www.superannotate.com/blog/llm-fine-tuning)
	- [Getting Started with Large Language Models: Key Things to Know](https://flyte.org/blog/getting-started-with-large-language-models-key-things-to-know)

In these results, there are two things that are equally mentioned. The first one being in-Context Learning and the second one being retrieval-augmented generation. So what actually is the difference between these two methods?

“In context learning” is just providing an example to a LLM inside its prompt. While “retrieval-augmented generation” actually fetches data from an external source like a database or file and adds it to the context of a LLM.

After having answered both of these questions it, is pretty clear that for our project and use cases we will be using vector databases in combination with retrieval-augmented generation.

#### Community research
To start our research as specifically as possible, we will continue with the gotten knowledge from the 'available product analysis'. So, for this question, we research online community's that have already tackled the problem of retrieving data via vector and adding it to the context of a LLM.

First, we will search this specific topic in GitHub repository's and look if something there can be of use to this research.

[GitHub](https://github.com/)
- Prompt: Vector RAG
- Answer:
	- [llm-rag-vectordb-python](https://github.com/build-on-aws/llm-rag-vectordb-python)
		- Contains sample applications and tutorials that showcase the power of **Amazon Bedrock with Python** 
	- [atlas-vector-search-rag](https://github.com/mongodb-developer/atlas-vector-search-rag)
		- The Python scripts in this repo use Atlas Vector Search with Retrieval-Augmented Generation (RAG) architecture to build a Question Answering application.
	- [haystack](https://github.com/deepset-ai/haystack)
		- End-to-end LLM framework that allows you to build applications powered by LLMs, Transformer models, vector search and more.
	- [Vector-Search-AI-Assistant-MongoDBvCore](https://github.com/Azure/Vector-Search-AI-Assistant-MongoDBvCore)
		- This solution demonstrates how to design and implement a **RAG Pattern** solution that incorporates Azure Cosmos DB for MongoDB vCore vector database capabilities with Azure Open AI Service to build a vector search solution with an AI assistant user interface.

[LangChain](https://python.langchain.com/)
- [Templates](https://python.langchain.com/docs/templates):
	- [rag-mongo](https://python.langchain.com/docs/templates/rag-mongo)
		- This template performs RAG using MongoDB and Open AI.
	- [rag-conversation](https://python.langchain.com/docs/templates/rag-conversation)
		- This template is used for [conversational](https://python.langchain.com/docs/expression_language/cookbook/retrieval#conversational-retrieval-chain) [retrieval](https://python.langchain.com/docs/use_cases/question_answering/), which is one of the most popular LLM use-cases.
	- [rag-pinecone](https://python.langchain.com/docs/templates/rag-pinecone)
		- This template performs RAG using Pinecone and Open AI.
	- [rag-chroma](https://python.langchain.com/docs/templates/rag-chroma)
		- This template performs RAG using Chroma and Open AI.

### Field

#### Problem analysis
The aim of this problem analysis is to identify the technology or strategy that our system should employ to recommend festivals to users based on their preferences. Due to limitations with the Chat-GPT 4 API and organizational restrictions on using the Bing Search API, we have opted to create a web scraper to gather festival information from websites and store it in our database. The focus of this research is on getting data from the database and using it to generate human-like responses through the Open AI API.

##### Problem
The challenge is to determine the most effective technology or strategy for recommending festivals to users based on their preferences within the Dverse project's system. Specifically, the focus is on fetching festival information from a database and feeding it to the Open AI API to provide personalized recommendations. 

###### **Why?**
Before proceeding with the development of the festival information agent, it's good to know the core of the issue at hand and ensure alignment with project objectives. Moreover, understanding the details of the issue will help in avoiding misdirected efforts towards solving an irrelevant issue.

1. **Improved User Experience:** Finding relevant festivals can be overwhelming for users.
2. **Enhanced Festival Visibility:** For festivals within the database, a well-designed recommendation system can increase their visibility by matching them with interested users.
3. **Increased User Engagement:** Personalized recommendations can lead to higher user satisfaction and encourage them to explore different aspects of Dverse.

###### **How?**
1. **User Preferences:** We need to identify how user preferences are captured within the system. Are there specific categories (genre, location, etc.) or free text descriptions?
2. **Festival Data:** We need to understand the structure of the festival data stored in the database. Are key details like genre, location, and dates accessible?
3. **Recommendation Engine:** We need to determine how to match user preferences with festival data. This could involve keyword matching, weighted scoring based on preference, or a combination of techniques.

#### Task analysis
To get a better understanding about the flow of our application, we need to analyze all the steps that are required by a user to get the recommended festival based on the preferences. To do this, I will create a scenario where I will act as the user wanting to go to a festival in the summer. We will start the desktop of the user's computer.

##### User tasks
- Open up preferred browser on computer.
- Navigate to Dverse UI website.
- Think about what festival I want to go to and make it as specific as possible.
	- Think of things like (name, season, price, date, age etc.)
- Input specific prompt into Dverse application.
- Hit enter to send prompt to system.

##### System tasks
- Send prompt from UI to backend server.
- Send prompt into the agent network.

##### Agent tasks
- Listen for incoming work.
- Check if received work can be done by agent.
- Process work.
- Create result.
- Check if complete prompt is handled.
	- If yes; send back to used.
	- If no; send back to agent network.

### Workshop

#### Brainstorm
This brainstorm session is together with Brett & Reno, the creators of this research paper. For this, we will try to think of as many as possible ideas on how to tackle the problem presented with this question.

##### Session
![Brainstorm Session 05-04-2024 - Result](https://github.com/fuas-dverse/ticket-system-agent/assets/43666923/9e620680-7c67-4b5f-b89d-97da3294b499)

##### Filtering
For this filtering, I will look through all the items created in the brainstorm session, and give a color to each of the items.

<span style="color: lightgreen">Green color:</span>
- Item will be used in current solution.
<span style="color: orange">Orange color:</span>
- Item will be considered for feature expansions.
<span style="color: red">Red color:</span>
- Item will be ignored and no further action required.

![Brainstorm Session 05-04-2024 - Result Filtered](https://github.com/fuas-dverse/ticket-system-agent/assets/43666923/d4f4e5a8-0b66-40cb-9359-a4b6dca628ad)


#### Prototype
Before starting to create a prototype based on the research that we have done this far. Let's start by specifying what we want to learn when creating this prototype.

I think that the main thing that we want to learn is already described in the [context](###Context) of this research.

`How can fetch the data from the database based on a prompt given by the user and then feed it to our Open AI API to return a human like answer.`

##### Early-stage prototype
![WhatsApp Image 2024-04-05 at 10 42 43](https://github.com/fuas-dverse/ticket-system-agent/assets/43666923/982d492b-15e8-4cb6-b648-2b7f02f26bca)

##### Vector Search
Now that I have a more global idea on what needs to happen, I am going to create a low functionality prototype on how to use vector search within the chosen database engine (MongoDB).

So, what is already present from the sketch at this moment? I have already created the 'Python Scrapper' to inserts data into a MongoDB cloud instance and created an embedding using the Open AI embedding models for the name and season of the festivals. This embedding is inserted into the 'embedding' field of the database.
![Pasted image 20240405105943](https://github.com/fuas-dverse/ticket-system-agent/assets/43666923/eb7a1a8f-4769-4d2a-a449-cadd1faeabb3)

Before creating any code, we need to set up the search index inside the MongoDB cloud instance.

1. Navigate to Atlas Search inside your database.
2. Press button 'Create Search Index'.
3. Choose option: Atlas Vector Search → JSON Editor
4. Give it a name, I used the default one and past is the following JSON:
	1. numDimensions: size of the embedding
	2. path: the name of the field the embedding is in
	3. similarity: the algorithm used to search
	4. type: what kind of search it is
```JSON
{
  "fields": [
    {
      "numDimensions": 1536,
      "path": "embedding",
      "similarity": "cosine",
      "type": "vector"
    }
  ]
}
```



Now to search in this embedding in created a new python script and installed the following packages:
```console
pip install pymongo openai python-dotenv
```

After that, we load the .env with the OPENAI_API_KEY & MONGO_URI variables inside of it. And from these variables we create an Open AI client and Mongo client.
```python
open_ai_client = OpenAI(  
    api_key=os.environ.get("OPENAI_API_KEY"),  
)  
  
client = MongoClient(os.environ["MONGO_URI"])  
db = client.festival_database  
collection = db.festivals
```

Now we create a function that actually searches the database based on the vector, once we have the result we remove the embedding as it is quite a large amount of unnecessary data. And last step we insert the results into a JSON file.
```python
def vector_search(query_vector):  
    result = list(db.festivals.aggregate([  
        {  
            "$vectorSearch": {  
                "index": "vector_index",  
                "path": "embedding",  
                "queryVector": query_vector,  
                "numCandidates": 3,  
                "limit": 3  
            }  
        }  
    ]))  
  
    new_result = [{k: v for k, v in item.items() if k != 'embedding'} for item in result]  
  
    with open('output.json', 'w') as json_file:  
        json.dump(new_result, json_file, default=str)
```

The last step is to create a function that runs on python start, where it asks for the user's input on what to search, creates an embedding and fires the vector_search function.
```python
if __name__ == "__main__":  
    user_input = input("> Enter a search query: ")  
  
    vector = name_embedding = open_ai_client.embeddings.create(  
            input=user_input,  
            model="text-embedding-3-small",  
            dimensions=1536  
    ).data[0].embedding  
  
    vector_search(vector)
```

The finished code should look something like this:
```python
import json  
import os  
from dotenv import load_dotenv  
from openai import OpenAI  
from pymongo import MongoClient  
  
load_dotenv()  
  
open_ai_client = OpenAI(  
    api_key=os.environ.get("OPENAI_API_KEY"),  
)  
  
client = MongoClient(os.environ["MONGO_URI"])  
db = client.festival_database  
collection = db.festivals  
  
  
def vector_search(query_vector):  
    result = list(db.festivals.aggregate([  
        {  
            "$vectorSearch": {  
                "index": "vector_index",  
                "path": "embedding",  
                "queryVector": query_vector,  
                "numCandidates": 3,  
                "limit": 3  
            }  
        }  
    ]))  
  
    new_result = [{k: v for k, v in item.items() if k != 'embedding'} for item in result]  
  
    with open('output.json', 'w') as json_file:  
        json.dump(new_result, json_file, default=str)  
  
  
if __name__ == "__main__":  
    user_input = input("> Enter a search query: ")  
  
    vector = name_embedding = open_ai_client.embeddings.create(  
            input=user_input,  
            model="text-embedding-3-small",  
            dimensions=1536  
    ).data[0].embedding  
  
    vector_search(vector)
```

If we run this code, the output should look like this.
- Input: “Summer”
- Output:
```json
[
   {
      "_id":"66013b2598897ab141a14003",
      "name":"Summerlake Festival",
      "description":"Summerlake Festival 2024 vindt plaats op 21 september. Check hier o.a. de line-up, kaartverkoop en meer over Summerlake Outdoor.",
      "city":"Woerden",
      "location":"Stadspark Molenvliet",
      "latitude":"52.0745543",
      "longitude":"4.859841",
      "start_date":"2024-09-21T12:00:00+00:00",
      "end_date":"2024-09-21T12:00:00+00:00",
      "season":"Summer",
      "price":"51.35",
      "age":null
   },
   {
      "_id":"66013b2598897ab141a13f7e",
      "name":"Indian Summer Festival",
      "description":"Check hier alles wat je wilt weten over het Indian Summer Festival 2024. Lees o.a. over de ticketverkoop, Line-up en sfeer.",
      "city":"Noord-Scharwoude",
      "location":"Geestmerambacht",
      "latitude":"52.6915457",
      "longitude":"4.7696867",
      "start_date":"2024-06-29T12:00:00+00:00",
      "end_date":"2024-06-29T12:00:00+00:00",
      "season":"Summer",
      "price":"64.00",
      "age":null
   },
   {
      "_id":"66013b2598897ab141a13fc9",
      "name":"Solar Weekend Festival",
      "description":"Op zoek naar info over het Solar Weekend Festival 2024? Festival Fans heeft de belangrijkste info op een rijtje gezet. Check het hier!",
      "city":"Roermond",
      "location":"Maasplassen",
      "latitude":"51.193243",
      "longitude":"5.9623117",
      "start_date":"2024-08-01T11:00:00+00:00",
      "end_date":"2024-08-04T23:00:00+00:00",
      "season":"Summer",
      "price":"72.50",
      "age":null
   }
]
```

Source:
- [Perform Semantic Search with Atlas Vector Search](https://www.mongodb.com/docs/atlas/atlas-vector-search/vector-search-overview/)
- [PyMongo](https://www.mongodb.com/docs/drivers/pymongo/#pymongo)

### Lab
For the lab section, I will be testing the prototype created in the previous section. Specifically, the `vector_search` function. As this is the only function in the prototype.

#### Unit test
First for the `vector_search` function, I have created some small unit tests. To test the functionality's of this function.
1. Test if result returns only three festivals, as this is the number given in the code.
2. Test if from the result the `embedding` field is removed, as this is quite big.
3. Test if `output.json` file is existing after running this function.
##### Tests
```python
def test_vector_search_results(benchmark, test_vector_object):  
    result = benchmark(vector_search, test_vector_object)  
    assert len(result) == 3  
  
def test_vector_search_removed_embeddings(benchmark, test_vector_object):  
    result = benchmark(vector_search, test_vector_object)  
  
    for i in range(0, len(result)):  
        assert result[i].get('embedding') is None  
  
def test_vector_search_output_created(benchmark, test_vector_object):  
    benchmark(vector_search, test_vector_object)  
  
    assert os.path.exists('output.json') is True
```
##### Results
![Pasted image 20240405132701](https://github.com/fuas-dverse/ticket-system-agent/assets/43666923/2e0a9a68-b4ea-4d91-9945-40d65bcbd15d)

#### Non-functional test

##### Performance tests
For the performance test, I am using a package called `pytest-benchmark`. Where I am running the following command to perform a benchmark test. 
```console
pytest test.py -v -s --benchmark-sort=mean --benchmark-min-rounds=100
```
This command will run 100 rounds of the specified test and get the performance from it.
###### Output
![Pasted image 20240405133602](https://github.com/fuas-dverse/ticket-system-agent/assets/43666923/f8256021-3f14-44bc-b002-225ad5bc213e)


### Reflection
In conducting this research, my primary objective was to identify effective techniques for searching a database based on user's preferences prompted in our Dverse application. I began by create the context of our project's challenges and the need for innovative solutions.

After evaluating various technologies and strategies, we settled on the use of vector databases capable of searching based on AI-generated embeddings. This decision was grounded by an analysis of available approaches and their alignment with our project requirements.

After having figured out what kind of techniques we wanted to use to achieve this goal, I created some unit and performance tests. In these test we can see the min, max and average times that it took for the functions to complete in 100 rounds. All being fast around 21ms and being slow around 55ms.

By completing this research, we can look deeper into the specific technique and implement it in our festival information agent.

This research has contributed to my professional growth, providing valuable insights into new technologies and their practical uses. Moving forward, we aim to integrate the chosen technique into our festival information agent, enhancing its capabilities and user experience.
