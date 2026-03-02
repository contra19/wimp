from fastapi import FastAPI

app = FastAPI(title="WIMP - Watchdog Intelligent Monitoring Platform")

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "wimp-api"}
