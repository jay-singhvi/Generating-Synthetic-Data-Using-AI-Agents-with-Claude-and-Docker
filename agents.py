# importing libraries
import csv
import os
from dotenv import load_dotenv
import anthropic
from prompts import *

load_dotenv(".env")

if not os.getenv("ANTHROPIC_API_KEY"):
    os.environ["ANTHROPIC_API_KEY"] = input("Enter your Anthropic API key: ")

claude_client = anthropic.Anthropic()
claude_model = "claude-3-5-sonnet-20240620"


# Function to read the CSV file from the User
def read_from_csv(file_path):
    data = []
    with open(file_path, "r", newline="") as csvfile:  # Open the CSV file in read mode
        csvreader = csv.reader(csvfile)

        for row in csvreader:
            data.append(row)  # Add each row to the data list
        return data


def save_to_csv(data, file_path, headers=None):
    mode = (
        "w" if headers else "a"
    )  # Set the mode based on whether the headers are provided
    with open(
        file_path, mode, newline=""
    ) as csvfile:  # Open the CSV file in write mode
        csvwriter = csv.writer(csvfile)

        if headers:
            csvwriter.writerow(headers)  # Write the headers if provided
        for row in csv.reader(data.splitlines()):
            csvwriter.writerow(row)  # Write each row to the CSV file


# Create Analyzer Agent
def analyzer_agent(sample_data, client=claude_client, claude_model=claude_model):

    message = client.messages.create(
        model=claude_model,
        max_tokens=400,  # Max number of tokens to generate - 400 is a good balance between accuracy and speed
        temperature=0,  # Setting the temperature to 0 for deterministic results
        system=ANALYZER_SYSTEM_PROMPT,  # Set the system prompt to the provided system prompt
        messages=[
            {
                "role": "user",
                "content": ANALYZER_USER_PROMPT.format(
                    sample_data=sample_data
                ),  # Format the prompt with the sample data
            }
        ],
    )
    return message.content[0].text  # Return the content of the message


# Create Generator Agent
def generator_agent(
    analysis_result,
    sample_data,
    client=claude_client,
    claude_model=claude_model,
    num_rows=15,
):

    message = client.messages.create(
        model=claude_model,
        max_tokens=1000,  # Max number of tokens to generate - 400 is a good balance between accuracy and speed
        temperature=1,  # Setting the temperature to High 1 for more creative results
        system=GENERATOR_SYSTEM_PROMPT,  # Set the system prompt to the provided system prompt
        messages=[
            {
                "role": "user",
                "content": GENERATOR_USER_PROMPT.format(
                    num_rows=num_rows,
                    analysis_result=analysis_result,
                    sample_data=sample_data,
                ),  # Format the prompt with the analysis and sample data
            }
        ],
    )
    return message.content[0].text


# Main Execution
file_path = input("Enter the CSV file name:")
file_path = os.path.join("/app/data", file_path)
desired_rows = int(input("Enter the number of rows to generate: "))

# Read CSV file from User
sample_data = read_from_csv(file_path)
sample_data_str = "\n".join(
    [",".join(row) for row in sample_data]
)  # Converts 2D list to 1D string

print("Analyzing...Calling Analyzer Agent")
analysis_result = analyzer_agent(sample_data_str)

print("Analysis Result: \n", analysis_result)

print("\nGenerating...Calling Generator Agent")

# Output files
output_file = "/app/data/output.csv"
headers = sample_data[0]
save_to_csv("", output_file, headers)

batch_size = 25
generated_rows = 0

while generated_rows < desired_rows:

    rows_to_generate = min(batch_size, desired_rows - generated_rows)
    print(f"Generating {rows_to_generate} rows")
    generated_data = generator_agent(
        analysis_result, sample_data_str, num_rows=rows_to_generate
    )
    save_to_csv(generated_data, output_file)
    generated_rows += rows_to_generate
    print(f"Generated {generated_rows} rows out of {desired_rows} desired rows")

print("Generated CSV file saved to /app/data/output.csv")
print({output_file})
