import tomllib
import sys
import os

# file = "alert_example.toml"
# with open(file, "rb") as toml:
#             alert = tomllib.load(toml)

failure = 0 

for root, dirs, files in os.walk("detections/"):
    for file in files:
        if file.endswith(".toml"):
            full_path = os.path.join(root, file)
            with open(full_path, "rb") as toml:
                alert = tomllib.load(toml)

                # required_fields = ["description", "name", "risk_score", "severity", "type", "query"]
                present_fields = []
                missing_fields =[]

                try:
                    if alert['metadata']['creation_date']:
                        pass 
                except:
                    print("The metadata table does not contain a creation_date on: " + full_path)
                    failure = 1

                if alert['rule']['type'] == "query":
                    required_fields = ["description", "name", "risk_score", "severity", "type", "query"]  
                elif alert['rule']['type'] == "eql": #event correlation alert
                    required_fields = ["description", "name", "risk_score", "severity", "type", "query", "language"] 
                elif alert['rule']['type'] == "threshold": #threshold based alert
                    required_fields = ["description", "name", "risk_score", "severity", "type", "query", "threshold"] 
                else:
                    print("Unsupported rule type found in: " + full_path) #error if type not found
                    break

                for table in alert:
                    for field in alert[table]:
                        present_fields.append(field)

                for field in required_fields:
                    if field not in present_fields:
                        missing_fields.append(field)

                if missing_fields:
                    print("The following fields do not exist in " + file + ": " + str(missing_fields))
                    failure  = 1
                else:
                    print("validation passed for: " + file)

#If we end up with 1 there is an error so exit and let me know there was an issue
if failure != 0:
    sys.exit(1)
