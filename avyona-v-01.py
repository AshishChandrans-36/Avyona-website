import random
import json
import os

class LearningAI:
    def __init__(self, memory_file="ai_memory.json"):
        self.memory_file = memory_file
        self.memory = self.load_memory()
        self.default_responses = {
            "happy": ["I'm glad to hear that!", "That's wonderful!", "Yay!"],
            "sad": ["I'm sorry to hear that.", "That must be tough.", "I'm here for you."],
            "angry": ["I understand your frustration.", "Let's try to calm down.", "Take a deep breath."],
            "neutral": ["I see.", "Okay.", "Tell me more."]
        }

    def load_memory(self):
        if os.path.exists(self.memory_file):
            with open(self.memory_file, "r") as f:
                return json.load(f)
        else:
            return []

    def save_memory(self):
        with open(self.memory_file, "w") as f:
            json.dump(self.memory, f)

    def detect_emotion(self, user_input):
        user_input = user_input.lower()
        if any(word in user_input for word in ["happy", "great", "good", "awesome", "fantastic"]):
            return "happy"
        elif any(word in user_input for word in ["sad", "unhappy", "depressed", "down", "bad"]):
            return "sad"
        elif any(word in user_input for word in ["angry", "mad", "furious", "annoyed"]):
            return "angry"
        else:
            return "neutral"

    def learn_response(self, user_input):
        # Try to find a similar user input in memory and reuse the AI response
        for chat in reversed(self.memory):
            if chat["user"].lower() == user_input.lower():
                return chat["ai"]
        return None

    def respond(self, user_input):
        learned = self.learn_response(user_input)
        if learned:
            return f"(Learned) {learned}"
        emotion = self.detect_emotion(user_input)
        return random.choice(self.default_responses[emotion])

    def remember(self, user_input, response):
        self.memory.append({"user": user_input, "ai": response})
        if len(self.memory) > 100:
            self.memory.pop(0)
        self.save_memory()

    def show_memory(self):
        print("\n--- Learned Conversations (last 10) ---")
        for i, chat in enumerate(self.memory[-10:], 1):
            print(f"{i}. You: {chat['user']}")
            print(f"   AI: {chat['ai']}")
        print("--------------------------------------\n")

if __name__ == "__main__":
    ai = LearningAI()
    print("Learning AI: Hello! How are you feeling today?")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Learning AI: Goodbye! Take care.")
            break
        if user_input.lower() == "memory":
            ai.show_memory()
            continue
        response = ai.respond(user_input)
        ai.remember(user_input, response)
        print(f"Learning AI: {response}")