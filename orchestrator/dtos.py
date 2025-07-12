from pydantic import BaseModel


class Problem(BaseModel):
    problem: str
    category: str

class Solution(BaseModel):
    title: str
    url: str