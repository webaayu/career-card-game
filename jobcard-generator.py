import gradio as gr
import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Define the base careers directory
base_careers_dir = "careers"

# Ensure the base careers directory exists
os.makedirs(base_careers_dir, exist_ok=True)

def generate_career_profile(job_profile_name, job_category):
    # Define the prompt
    prompt = f"""
    Generate a JSON object for a career profile with the following structure:
    {{
        "CareerCard": {{
            "Title": "{job_profile_name}",
            "Overview": "Provide a brief description explaining the role, responsibilities, and significance of a {job_profile_name}.",
            "Pros & Cons": {{
                "Pros": ["List 3–4 key pros."],
                "Cons": ["List 3–4 key cons."]
            }},
            "Dual Impact Highlights": {{
                "Personal Growth": "Summarize how this career affects personal growth.",
                "Community Impact": "Summarize how this career impacts the community."
            }}
        }},
        "Level1ScenarioCards": [
            {{
                "Title": "Initial Challenge 1",
                "Description": "Describe a basic challenge or opportunity typical for an entry-level {job_profile_name}.",
                "DecisionCards": [
                    {{
                        "Option A": "Describe an action choice.",
                        "Outcomes": {{
                            "PersonalImpact": "+X",
                            "CommunityImpact": "+Y"
                        }}
                    }},
                    {{
                        "Option B": "Describe an alternative action choice.",
                        "Outcomes": {{
                            "PersonalImpact": "+A",
                            "CommunityImpact": "+B"
                        }}
                    }}
                ]
            }}
        ],
        "Level2ScenarioCards": [
            {{
                "Title": "Advanced Challenge 1",
                "Description": "Describe a more complex challenge that a {job_profile_name} might face as responsibilities increase.",
                "DecisionCards": [
                    {{
                        "Option A": "Describe an action choice.",
                        "Outcomes": {{
                            "PersonalImpact": "+X",
                            "CommunityImpact": "+Y"
                        }}
                    }},
                    {{
                        "Option B": "Describe an alternative action choice.",
                        "Outcomes": {{
                            "PersonalImpact": "+A",
                            "CommunityImpact": "+B"
                        }}
                    }}
                ]
            }}
        ]
    }}
    """

    # Generate the JSON response
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an AI that generates structured career profiles in JSON format."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=1000,
    )

    # Debugging: Print the response
    print("Response from OpenAI:", response)

    # Extract and clean response content
    if response.choices:
        content = response.choices[0].message.content.strip()

        # Remove possible markdown formatting
        if content.startswith("```json"):
            content = content[7:-3].strip()

        try:
            career_profile = json.loads(content)  # Convert string to JSON

            # Define the category-specific directory path
            category_dir = os.path.join(base_careers_dir, job_category)
            os.makedirs(category_dir, exist_ok=True)  # Ensure the category directory exists

            # Define the file path
            file_path = os.path.join(category_dir, f"{job_profile_name.replace(' ', '_').lower()}.json")

            # Save the JSON to a file
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(career_profile, f, indent=4)

            return f"Career profile for '{job_profile_name}' has been saved as '{file_path}'."

        except json.JSONDecodeError:
            return "Error: Failed to parse OpenAI response into JSON."

    return "Error: OpenAI API response did not contain the expected content."

# Define the Gradio interface
iface = gr.Interface(
    fn=generate_career_profile,
    inputs=[
        gr.Textbox(label="Job Profile Name"),
        gr.Dropdown(
            label="Job Category",
            choices=["Education", "Technology", "Healthcare", "Hospitality", "Finance", "Marketing", "Engineering", "Arts and Design", "Legal", "Science and Research"],
            type="value",
        ),
    ],
    outputs=gr.Textbox(label="Status"),
    live=False
)

# Launch the interface
iface.launch()
