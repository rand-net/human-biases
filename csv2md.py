import csv
import pandas as pd

biases_df = pd.read_csv(
    "data/biases.csv",
    header=None,
    names=["Affected_Domain", "Name", "Type", "Description"],
)

unique_domains = []
file_output = ""
for unique_domain in biases_df["Affected_Domain"].unique():
    unique_domains.append(unique_domain)
    selected_domain = biases_df[biases_df["Affected_Domain"] == unique_domain]
    unique_types = []
    file_output += "# " + str(unique_domain)
    for unique_type in selected_domain["Type"].unique():
        unique_types.append(unique_type)
        items = selected_domain[selected_domain["Type"] == unique_type]

        file_output += "\n## " + str(unique_type)
        for item_name, item_description in zip(items["Name"], items["Description"]):
            file_string = "\n### " + str(item_name) + "\n" + str(item_description)
            file_output += file_string

with open("data/biases.md", "w") as f:
    f.write(file_output)
