from openai import OpenAI
from rich.console import Console
from rich.panel import Panel
import json

from util import call_llm, render_response, print_messages
from tools.translate_dna import translate_dna, translate_dna_schema

def execute_tool_call(tool_call):
    """Execute the tool call that the LLM requested"""
    function_name = tool_call.function.name
    assert function_name == "translate_dna"

    arguments = json.loads(tool_call.function.arguments)    

    return translate_dna(**arguments)

def main(show_messages): 
    # Initialize Rich console
    console = Console()

    # Initialize client
    client = OpenAI()
    
    # Initialize context (message history)
    messages = []
    
    # Define the tool schema 
    tool_schemas = [translate_dna_schema]
    
    # Welcome message
    console.print(Panel.fit(
        "[cyan bold]Chat REPL with DNA Translation[/cyan bold]\n[dim]Type 'quit' or 'exit' to end[/dim]\n[yellow]Try: 'Translate this DNA: ATGGCCATTGTAATGGGCCGC'[/yellow]",
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
            # Show spinner while waiting for response
            with console.status("[bold green]Thinking...", spinner="dots"):
                response_message = call_llm(messages, client, tool_schemas)
            
            # Check if the model wants to call a tool
            if response_message.tool_calls:                
                # Add the assistant's response (with tool call) to messages
                messages.append(response_message)
                
                # There should be only one tool because we supplied only one tool to the LLM 
                assert len(response_message.tool_calls) == 1 
                tool_call, = response_message.tool_calls

                # Execute tool call 
                console.print(f"[dim][Tool Call: {tool_call.function.name}][/dim]")
                    
                # Execute the tool
                tool_result = execute_tool_call(tool_call)
                    
                # Add tool result to messages
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(tool_result)
                })
                
                # Get the final response from the model
                with console.status("[bold green]Generating response...", spinner="dots"):
                    final_response = call_llm(messages, client, tool_schemas)
                
                # Display the final response
                console.print("[dim]Assistant ➜[/dim] ", end='')
                render_response(final_response.content, console)
                
                # Add final response to context
                messages.append(final_response)
            else:
                # No tool call, just display the response
                console.print("[dim]Assistant ➜[/dim] ", end='')
                render_response(response_message.content, console)
                
                # Add assistant response to context
                messages.append(response_message)

            if show_messages: 
                print_messages(messages, console)
            
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")
            messages.pop()
        
        console.print()

if __name__ == '__main__': 
    main(show_messages=True)