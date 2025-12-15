from bm25.search import hybrid_search_en, search_with_indexes
import ollama
from agent.prompt_template import SYSTEM_PROMPT, PromptTemplate

def retriever(query):
    results = search_with_indexes(
        query,
        index_dir="indexes",
        top_k=25,
        alpha=0.4,
        verbose=True
    )
    return results
def construct_prompt(query, results):
    template = PromptTemplate()
    prompt = template.create_search_augmented_prompt(
        query,
        results,
        max_results=10
    )
    return prompt

def model_response(prompt):
    model = ollama.Client()
    response = model.generate(prompt=prompt, model='qwen3:8b')    
    return response



if __name__ == "__main__":
    query = "How do I configure multiple OSPF processes on ZebOS?"
    results = retriever(query)
    prompt = construct_prompt(query, results)
    print("=== Prompt ===")
    print(prompt)
    print("=== Model Response ===")
    response = model_response(prompt)
    print(response['response'])

    