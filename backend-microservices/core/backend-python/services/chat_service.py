from semantic.llm.hybrid_router import HybridLLMRouter

llm = HybridLLMRouter()

def chat(request):
    messages = [m.dict() for m in request.messages]
    response = llm.chat(messages=messages, force_local=request.force_local)
    return {"response": response}
