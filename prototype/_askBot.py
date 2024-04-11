import replicate

SYSTEM_PROMPT="Pretend that you are a customer executive from ICICI Bank. You answer professionally and only answer related to the banking services. Your name is Sneha. If customer ask for anything other than banking, refuse politely."
def askBot(prompt: str, prompt_history: str):
    print("prompt history: "+prompt)
    output = replicate.run(
    "meta/llama-2-13b-chat",
    input={
        "system_prompt": SYSTEM_PROMPT,
        "prompt": prompt_history+"\n"+"[INST]"+prompt+"[/INST]",
        "temperature": 0.75
    }
    )

    print("raw output: ", output)
    output_string = ''.join(map(str, output))

    print("output for \n"+prompt+"\n"+output_string)
    prompt_history = updatePromptHistory(prompt, output_string, prompt_history)

    return (output_string, prompt_history)
    
def updatePromptHistory(prompt: str, output: str, prompt_history: str):
    if len(prompt_history) > 0:
        prompt_history += "\n"
    prompt_history += "[INST]"+prompt+"[/INST]"+"\n"+output

    return prompt_history
