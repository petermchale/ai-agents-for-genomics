from openai import OpenAI

def call_llm(messages, client): 
    print(client.chat.completions.create(
        model="gpt-4",
        messages=messages 
    ).choices[0].message.content)

def main(): 
    # Initialize client
    client = OpenAI()

    print('Too little context:')
    print('-------------------')
    call_llm(
        messages=[
            {"role": "user", "content": "What is its population?"}
        ],
        client=client
    )
    print()

    print('Sufficient context:')
    print('-------------------')
    call_llm(
        messages=[
            {"role": "user", "content": "What's the capital of France?"},
            {"role": "assistant", "content": "The capital of France is Paris."},
            {"role": "user", "content": "What is its population?"}
        ],
        client=client
    ) 
    print()   

if __name__ == '__main__': 
    main()