import operator
from collections.abc import Sequence
from typing import Annotated, TypedDict

from langchain_core.messages import AnyMessage


class AgentState(TypedDict): 
    messages: Annotated[Sequence[AnyMessage], operator.add]

