from openai import OpenAI
from rich.console import Console
from rich.panel import Panel
import json

from util import call_llm, render_response, print_messages, execute_tool_call
from tools.translate_dna import translate_dna, translate_dna_schema
from tools.analyze_protein import analyze_protein, analyze_protein_schema

def main(show_messages): 
    # Initialize Rich console
    console = Console()

    # Initialize client
    client = OpenAI()
    
    # Initialize context (message history)
    messages = []
    
    # Define the mapping of function names to function objects
    tool_functions = {
        "translate_dna": translate_dna,
        "analyze_protein": analyze_protein
    }
    
    # Define the tool schemas
    tool_schemas = [
        translate_dna_schema, 
        analyze_protein_schema
    ]
    
    # Welcome message
    console.print(Panel.fit(
        "[cyan bold]Chat REPL with DNA Translation & Protein Analysis[/cyan bold]\n"
        "[dim]Type 'quit' or 'exit' to end[/dim]\n"
        "[yellow]Try: 'Translate this DNA and analyze the protein: ATGGCCATTGTAATGGGCCGC'[/yellow]",
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
        
        try:
            # Show spinner while waiting for initial response
            with console.status("[bold green]Thinking...", spinner="dots"):
                response_message = call_llm(messages, client, tool_schemas)
            
            # Handle tool calls in a loop until we get a final response
            while response_message.tool_calls:
                # Add the assistant's response (with tool call) to messages
                messages.append(response_message)
                
                # Execute each tool call
                for tool_call in response_message.tool_calls:
                    console.print(f"[dim][Tool Call: {tool_call.function.name}][/dim]")
                    
                    # Execute the tool using the tool_functions dictionary
                    tool_result = execute_tool_call(tool_call, tool_functions)
                    
                    # Add tool result to messages
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(tool_result)
                    })
                
                # Get the next response from the model
                with console.status("[bold green]Processing...", spinner="dots"):
                    response_message = call_llm(messages, client, tool_schemas)
            
            # We've exited the loop, so response_message contains the final text response
            console.print("[dim]Assistant ➜[/dim] ", end='')
            render_response(response_message.content, console)
            
            # Add final response to context
            messages.append(response_message)

            if show_messages: 
                print_messages(messages, console)
            
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")
            # Remove the last user message on error
            if messages and messages[-1].get("role") == "user":
                messages.pop()
        
        console.print()

if __name__ == '__main__': 
    main(show_messages=True)