import replicate

class BankingBot:
    def __init__(self):
        self.SYSTEM_PROMPT = "Act as you are a customer executive from Rich Dad Poor Dad Bank. You answer professionally and only answer related to the banking services. Your name is Sneha. Do not mention everytime that you are a customer executive"
        self.message_history = []  # Initialize an empty list to keep track of message history

    def ask_bot(self, prompt: str):
        # Add user message to message history
        self.message_history.append({
            "text": prompt,
            "isUser": True
        })

        generated_prompt = self.generate_prompt()

        print("Generated prompt for this call: " + generated_prompt)
        output = replicate.run(
            "meta/llama-2-13b-chat",
            input={
                "system_prompt": self.SYSTEM_PROMPT,
                "prompt": generated_prompt,
                "temperature": 0.75,
                "max_new_tokens": 100,
                "min_new_tokens": -1
            }
        )

        output_string = ''.join(map(str, output))

        # Add bot response to message history
        self.message_history.append({
            "text": output_string,
            "isUser": False
        })

        print("Output for \n" + prompt + "\n" + output_string)

        return output_string

    def generate_prompt(self):
        # Generate prompt from message history
        return "\n".join(
            f'[INST] {message["text"]} [/INST]' if message["isUser"] else message["text"]
            for message in self.message_history
        )
