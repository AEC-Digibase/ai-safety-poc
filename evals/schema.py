from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Annotated, List, Literal, Optional
from pydantic import StringConstraints

PromptText = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
AnswerText = PromptText
NameText = AnswerText

class Prompt(BaseModel):
    # required natural language input
    text: PromptText = Field(..., description="User prompt text")
    # optional orchestration context
    system: Optional[str] = None
    policy: Optional[str] = None

class TruthItem(BaseModel):
    type: Literal['truth'] = 'truth'
    id: Optional[str] = None
    prompt: Prompt
    answer: AnswerText
    checker: Literal['check_truth'] = 'check_truth'
    severity: Literal['info','low','medium','high'] = 'medium'
    tags: List[str] = []
    ref: Optional[str] = None # citation or url

class JailbreakItem(BaseModel):
    type: Literal['jailbreak'] = 'jailbreak'
    id: Optional[str] = None
    prompt: Prompt
    checker: Literal['check_jailbreak'] = 'check_jailbreak'
    severity: Literal['low','medium','high','critical'] = 'high'
    tags: List[str] = []

class PIIItem(BaseModel):
    type: Literal['pii'] = 'pii'
    id: Optional[str] = None
    prompt: Prompt
    checker: Literal['check_pii'] = 'check_pii'
    severity: Literal['medium','high'] = 'high'
    tags: List[str] = []

SuiteMetric = Literal['accuracy','success_rate_low_is_good','leaks_low_is_good']


class Suite(BaseModel):
    name: NameText
    metric: SuiteMetric
    # checker at suite level is optional when items specify their own
    checker: Optional[Literal['check_truth','check_jailbreak','check_pii']] = None
    items: List[TruthItem | JailbreakItem | PIIItem]


class Config:
    extra = 'forbid'