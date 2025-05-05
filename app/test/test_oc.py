import os
import dotenv

dotenv.load_dotenv()

print("oc: ", os.getenv("OC"))