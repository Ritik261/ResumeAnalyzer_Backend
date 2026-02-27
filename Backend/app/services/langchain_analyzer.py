from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import RunnablePassthrough
from pydantic import BaseModel, Field
class ResumeAnalysisResult(BaseModel):
    key_skills: list[str] = Field(description="List of key technical skills")
    ats_score: int = Field(description="ATS score between 0 and 100")
    recommendations: list[str] = Field(description="List of improvement suggestions")
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.2
)
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an expert ATS resume analyzer. "
        "Analyze resumes strictly and objectively."
    ),
    (
        "human",
        """
Resume Text:
{resume}

Extract:
- Key skills
- ATS score (0-100)
- Improvement recommendations

Return in JSON
"""
    )
])
parser = JsonOutputParser(pydantic_object=ResumeAnalysisResult)

resume_chain = (
    {"resume": RunnablePassthrough()}
    | prompt
    | llm
    | parser
)
def analyze_resume(resume_text: str) -> ResumeAnalysisResult:
    return resume_chain.invoke(resume_text)
