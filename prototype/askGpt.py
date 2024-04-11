import os
from openai import OpenAI
import json

client = OpenAI(
  api_key=os.environ['OPENAI_API_KEY'],
)

student_1_description = "David Nguyen is a sophomore majoring in computer science at Stanford University. He is Asian American and has a 3.8 GPA. David is known for his programming skills and is an active member of the university's Robotics Club. He hopes to pursue a career in artificial intelligence after graduating."
student_2_description="Ravi Patel is a sophomore majoring in computer science at the University of Michigan. He is South Asian Indian American and has a 3.7 GPA. Ravi is an active member of the university's Chess Club and the South Asian Student Association. He hopes to pursue a career in software engineering after graduating."

student_custom_functions = [
    {
        'name': 'extract_student_info',
        'description': 'Get the student information from the body of the input text',
        'parameters': {
            'type': 'object',
            'properties': {
                'name': {
                    'type': 'string',
                    'description': 'Name of the person'
                },
                'major': {
                    'type': 'string',
                    'description': 'Major subject.'
                },
                'school': {
                    'type': 'string',
                    'description': 'The university name.'
                },
                'grades': {
                    'type': 'integer',
                    'description': 'GPA of the student.'
                },
                'club': {
                    'type': 'string',
                    'description': 'School club for extracurricular activities. '
                }
                
            }
        }
    }
]



student_description = [student_1_description,student_2_description]
for i in student_description:
    response = client.chat.completions.create(
        model = 'gpt-3.5-turbo',
        messages = [{'role': 'user', 'content': i}],
        functions = student_custom_functions,
        function_call = 'auto'
    )

    print(response)

    # Loading the response as a JSON object
    json_response = json.loads(response.choices[0].message.function_call.arguments)
    print(json_response)


order_custom_functions = [
    {
        'name': 'extract_order_info',
        'description': 'ask user their order id when they query about their order',
        'parameters': {
            'type': 'object',
            'properties': {
                'order_id': {
                    'type': 'string',
                    'description': 'Order id'
                }
            }
        }
    }
]

def askGpt(content):
    response = client.chat.completions.create(
        model = 'gpt-3.5-turbo',
        messages = [{'role': 'user', 'content': content}],
        functions = order_custom_functions,
        function_call = 'auto'
    )

    print(response)

    descriptions = [
    student_1_description, 
    "Who was a Abraham Lincoln?",
    school_1_description
                ]

for i, sample in enumerate(descriptions):
    response = client.chat.completions.create(
        model = 'gpt-3.5-turbo',
        messages = [{'role': 'user', 'content': sample}],
        functions = custom_functions,
        function_call = 'auto'
    )
    
    response_message = response.choices[0].message
    
    if dict(response_message).get('function_call'):
        
        # Which function call was invoked
        function_called = response_message.function_call.name
        
        # Extracting the arguments
        function_args  = json.loads(response_message.function_call.arguments)
        
        # Function names
        available_functions = {
            "extract_school_info": extract_school_info,
            "extract_student_info": extract_student_info
        }
        
        fuction_to_call = available_functions[function_called]
        response_message = fuction_to_call(*list(function_args .values()))
        
    else:
        response_message = response_message.content
    
    print(f"\nSample#{i+1}\n")
    print(response_message)