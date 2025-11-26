  from db import cur, con
  from utils import getUserInput
  
  def getScheduledActivities():
    start_date = getUserInput("Start date (YYYY-MM-DD): ")
    end_date = getUserInput("End date (YYYY-MM-DD): ")
    area_name = getUserInput("Campus area: ")
    
    filterConditions = []
    filterParameters = []
    
    baseQuery = ""
    SELECT
        activity.activity_id,
        activity.activity_desc,
