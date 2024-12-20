import pandas as pd

# Function to calculate yearly changes for activities, members, and grants
def calculate_yearly_changes(data):
    data = data.sort_values(by=["id", "year"])
    data["Activity Change (%)"] = data.groupby("id")["activities"].pct_change() * 100
    data["Member Change (%)"] = data.groupby("id")["total_members"].pct_change() * 100
    data["Grant Change (%)"] = data.groupby("id")["approved_grants"].pct_change() * 100
    return data