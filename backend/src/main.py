from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.v1 import AuthRouter, UserRouter, CandidateExamRouter,SubmissionRouter, SearchRouter, QuestionRouter, StorageRouter, ExamRouter
from fastapi.exceptions import ResponseValidationError
from fastapi import Request
from fastapi.responses import JSONResponse

app = FastAPI()

origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

auth_routes = AuthRouter()
user_routes = UserRouter()
submission_routes = SubmissionRouter()
search_routes = SearchRouter()
question_routes = QuestionRouter()
storage_routes = StorageRouter()
exam_routes = ExamRouter()
candidate_exam_routes = CandidateExamRouter()

app.include_router(user_routes.router)
app.include_router(auth_routes.router)
app.include_router(submission_routes.router)
app.include_router(search_routes.router)
app.include_router(question_routes.router)
app.include_router(storage_routes.router)
app.include_router(exam_routes.router)
app.include_router(candidate_exam_routes.router)

@app.exception_handler(ResponseValidationError)
async def validation_exception_handler(request: Request, exc: ResponseValidationError):
    # This prints the EXACT field that is failing to your console
    print(f"Response Validation Error for {request.url}: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )
    
@app.get("/api/v1/")
def home():
    return {
        "message": "Backend server running on port 8000"
    }
