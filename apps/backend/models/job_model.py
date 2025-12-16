from pydantic import BaseModel

class Job(BaseModel):
   job_id:str
   pid:int
   command:list
   status: str
   
