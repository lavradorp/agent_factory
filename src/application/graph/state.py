import operator
from typing import Annotated, TypedDict, Sequence

from langchain_core.messages import AnyMessage


class AgentState(TypedDict): 
    messages: Annotated[Sequence[AnyMessage], operator.add]

