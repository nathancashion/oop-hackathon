import models_ollama as models
import data
import json

stats_prompt = """Identify if the report presented diagnoses one of the following diagnosis : {diagnosis}.

Return NO DIAGNOSIS if there is no diagnosis that matches this list {diagnosis}

Here is the report
{report}
"""

stats_for_age_prompt = """
If there is a matching diagnosis, return the percentage corresponding to the persons age group.
This information might be relevant for your answer.
{data}

This is the persons report:
{report}

Instructions:
- Don't return more than one percentage.
- If there is no matching diagnosis return nothing.
"""

def identify_disease_in_report(report):
    return models.call_openai(stats_prompt.format(report=report, diagnosis=",".join(data.stats_data.keys()), stats=json.dumps(data.stats_data))).choices[0].message.content

def stat_finder(report):
    # Identify the diagnosis in the Report.
    return identify_disease_in_report(report)

def stat_finder_age(report):
    # Identify the diagnosis in the Report.
    return models.call_openai(stats_for_age_prompt.format(data=json.dumps(data.stats_data), report=report)).choices[0].message.content