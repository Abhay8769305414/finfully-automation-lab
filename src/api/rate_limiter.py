import time
from collections import defaultdict
from fastapi import HTTPException, status, Request

class InMemoryRateLimiter:
    def __init__(self, requests_per_minute: int = 60):
        self.rpm = requests_per_minute
        self.requests = defaultdict(list)
        
    def check_rate_limit(self, client_id: str):
        now = time.time()
        minute_ago = now - 60.0
        
        self.requests[client_id] = [t for t in self.requests[client_id] if t > minute_ago]
        
        if len(self.requests[client_id]) >= self.rpm:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded. Please try again later.",
            )
            
        self.requests[client_id].append(now)

rate_limiter = InMemoryRateLimiter(requests_per_minute=120)
