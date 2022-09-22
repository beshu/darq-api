# Framework: FastApi
# Database: MongoDB(driver: motor)
# Deploy: Docker Compose
#
# 1. Create a user model using Pydantic with fallowing attributes:
#
#         id
#         first_name
#         last_name
#         role (one of: admin, dev, simple mortal)
#         is_active
#         created_at
#         last_login
#         hashed_pass
#
# 2. Define and implement validation strategy for each one of given fields.
# 3. Implement REST API methods for users using already defined Pydantic model.
# 4. Implement a simple authentication middleware.
# 5. Crete an route restricted only for user's with admin role
#  which allow to change by oid(ObjectId) other user's attributes except hashed_pass.
# 6. Crete a docker-compose file to deploy the app.
# 7. Upload the solution to github and send the link.
import logging

import uvicorn as uvicorn
from fastapi import FastAPI
from app.user.router import r as user_router
from app.auth.router import r as auth_router

app = FastAPI(debug=True)
app.include_router(user_router)
app.include_router(auth_router)

if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=4557, reload=True, log_level=logging.DEBUG, use_colors=True)