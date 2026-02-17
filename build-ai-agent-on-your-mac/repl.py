from openai import OpenAI
from rich.console import Console
from rich.panel import Panel

from util import render_response, print_messages

def call_llm(messages, client): 
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages 
    )
    return response.choices[0].message.content

def main(show_messages): 
    # Initialize Rich console
    console = Console()

    # Initialize client
    client = OpenAI()
    
    # Initialize context (message history)
    messages = []
    
    # Welcome message
    console.print(Panel.fit(
        "[cyan bold]Chat REPL[/cyan bold]\n[dim]Type 'quit' or 'exit' to end[/dim]",
        border_style="cyan"
    ))
    console.print()
    
    while True:
        # User prompt 
        user_input = console.input("[dim]You ➜ [/dim]")
        
        # Check for exit command
        if user_input.lower().strip() in ['quit', 'exit']:
            console.print("[cyan]Goodbye![/cyan]")
            break
        
        # Skip empty inputs
        if not user_input.strip():
            continue
        
        # Add user message to context
        messages.append({"role": "user", "content": user_input})
        
        # Get LLM response
        try:
            # Show spinner while waiting for response
            with console.status("[bold green]Thinking...", spinner="dots"):
                response = call_llm(messages, client)
            
            # Assistant prompt and response
            console.print("[dim]Assistant ➜[/dim] ", end='')
            render_response(response, console)
            
            # Add assistant response to context
            messages.append({"role": "assistant", "content": response})

            if show_messages: 
                print_messages(messages, console)
            
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")
            messages.pop()
        
        console.print()

if __name__ == '__main__': 
    main(show_messages=False)