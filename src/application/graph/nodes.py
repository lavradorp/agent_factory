from langchain_core.messages import SystemMessage, ToolMessage

from src.application.graph.state import AgentState


def call_llm(state: AgentState, llm, system_prompt = None) -> AgentState:
    messages = state['messages']

    if system_prompt and not any(isinstance(m, SystemMessage) for m in messages):
        messages = [SystemMessage(content=system_prompt)] + messages
    
    message = llm.invoke(messages)

    return {'messages': [message]}

def exists_action(state: AgentState) -> bool:
    last_message = state['messages'][-1]
    tool_calls = getattr(last_message, 'tool_calls', [])
    
    return len(tool_calls) > 0


def take_action(state: AgentState, registred_tools: dict) -> dict:
    tool_calls = state['messages'][-1].tool_calls
    results = []

    for t in tool_calls:
        tool_name = t['name']
        raw_args = t['args']
        
        search_string = ""
        
        if isinstance(raw_args, dict):
            search_string = raw_args.get('query') or raw_args.get('question') or ""

            if isinstance(search_string, dict):
                search_string = search_string.get('description', str(search_string))
        else:
            search_string = str(raw_args)
            
        clean_args = {"query": search_string}

        if tool_name not in registred_tools:
            error_msg = f"Tool '{tool_name}' does not exist. Available tools: {list(registred_tools.keys())}"
            results.append(ToolMessage(tool_call_id=t['id'], name=tool_name, content=error_msg))
            continue

        try:
            result = registred_tools[tool_name].invoke(clean_args)

            str_result = str(result)
            
            results.append(ToolMessage(tool_call_id=t['id'], name=tool_name, content=str_result))
            
        except Exception as e:
            error_msg = f"Error executing tool: {str(e)}"
            results.append(ToolMessage(tool_call_id=t['id'], name=tool_name, content=error_msg))

    return {'messages': results}

    