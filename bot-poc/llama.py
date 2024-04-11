import replicate

PROMPT_HISTORY=""
SYSTEM_PROMPT="Pretend that you are a customer executive from ICICI Bank from now on and give answers only in that context. Your name is Sneha and if any other question is asked other than bank related, just say sorry i cannot help with that."
def askBot(prompt: str):
    global PROMPT_HISTORY
    output = replicate.run(
    "meta/llama-2-13b-chat",
    input={
        "system_prompt": SYSTEM_PROMPT,
        "prompt": PROMPT_HISTORY+"\n"+prompt,
        "temperature": 0.75
    }
    )

    output_string = ' '.join(map(str, output))

    print("output for \n"+prompt+"\n"+output_string)
    updatePromptHistory(prompt, output_string)
    
def updatePromptHistory(prompt: str, output: str):
    if len(PROMPT_HISTORY) > 0:
        PROMPT_HISTORY += "\n"
    PROMPT_HISTORY += "[INST]"+prompt+"[/INST]"+"\n"+output
