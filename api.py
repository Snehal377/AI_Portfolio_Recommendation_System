from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import agent
app = FastAPI()  

# Request body schema
class InvestmentRequest(BaseModel):
    goal: str
    amount: float = None
    duration: int

# Add ye function yaha

@app.post("/recommend_portfolio")
def recommend_portfolio(request: InvestmentRequest):
    if request.amount is None or request.amount <= 0:
        return {"error": "Investment amount is missing or zero. Please provide a valid amount."}

    try:
        # LangGraph invoke
        result = agent.app.invoke({
            "input": request.goal,
            "amount": request.amount,
            "duration": request.duration
        })

    except Exception as e:
        return {"error": f"Agent failed to generate portfolio: {str(e)}"}

    return {"portfolio_recommendation": result["final_recommendation"]}

@app.get("/health")
def health_check():
    return {"status": "OK"}