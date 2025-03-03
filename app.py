import os
import json
import yaml
from crewai import Agent, Task, Crew, LLM, Process
from dotenv import load_dotenv,find_dotenv
from os import environ as env
from typing import List
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
import requests
import pandas as pd

import markdown
from langchain_google_genai import ChatGoogleGenerativeAI

import litellm
#litellm.set_verbose = True
os.environ['LITELLM_LOG'] = 'DEBUG'

load_dotenv('config/.env')

print('GOOGLE_API_KEY:  {}'.format(env['GOOGLE_API_KEY']))

GEMINI_API_KEY = env['GOOGLE_API_KEY']

env["GEMINI_API_KEY"] = env['GOOGLE_API_KEY']
MODEL_NAME = "models/text-embedding-004"
env["SERPER_API_KEY"] = env['SERPER_KEY']

MODEL_NAME_LLM = "gemini/gemini-1.5-pro-latest"
MODEL_NAME_LLM = "gemini/gemini-2.0-flash-exp"

llm = LLM(
    model = MODEL_NAME_LLM,
    temperature = 0.7
)


#Loading Tasks and Agents YAML files

# Define file paths for YAML configurations
files = {
    'agents': 'config/agents.yaml',
    'tasks': 'config/tasks.yaml'
}

# Load configurations from YAML files
configs = {}
for config_type, file_path in files.items():
    with open(file_path, 'r') as file:
        configs[config_type] = yaml.safe_load(file)

# Assign loaded configurations to specific variables
agents_config = configs['agents']
tasks_config = configs['tasks']


#Important Use a tool for read file system
# Using FileReadTool

from crewai_tools import FileReadTool
csv_tool = FileReadTool(file_path='./support_tickets_data.csv')

#Creating Agents, Tasks and Crew

# Creating Agents
suggestion_generation_agent = Agent(
  config=agents_config['suggestion_generation_agent'],
  tools = [csv_tool],
  llm = llm

)

reporting_agent = Agent(
  config=agents_config['reporting_agent'],
  tools = [csv_tool],
  llm = llm
)

chart_generation_agent = Agent(
  config=agents_config['chart_generation_agent'],
  allow_code_execution = False,
  llm = llm
)

# Creating Tasks
suggestion_generation = Task(
  config = tasks_config['suggestion_generation'],
  agent = suggestion_generation_agent
)

table_generation = Task(
  config = tasks_config['table_generation'],
  agent = reporting_agent
)

chart_generation = Task(
  config = tasks_config['chart_generation'],
  agent = chart_generation_agent
)

final_report_assembly = Task(
  config = tasks_config['final_report_assembly'],
  agent = reporting_agent,
  context = [suggestion_generation, table_generation, chart_generation]
)


# Creating Crew
support_report_crew = Crew(
  agents=[
    suggestion_generation_agent,
    reporting_agent,
    chart_generation_agent
  ],
  tasks=[
    suggestion_generation,
    table_generation,
    chart_generation,
    final_report_assembly
  ],
  verbose = True
)


#Testing our Crew
#support_report_crew.test(n_iterations=1, openai_model_name='gpt-4o')

#support_report_crew.test(n_iterations=1)

#Training your crew and agents
#support_report_crew.train(n_iterations=1, filename='training.pkl')

#Comparing new test results
#support_report_crew.test(n_iterations=1, openai_model_name='gpt-4o')

#support_report_crew.test(n_iterations=1 )

from IPython.display import Image, display

# Load and display the image
# test_image = Image(filename='test_before_training.png', width=368)
# display(test_image)

#Kicking off Crew
result = support_report_crew.kickoff()

#Result
from IPython.display import display, Markdown
display(Markdown(result.raw))


