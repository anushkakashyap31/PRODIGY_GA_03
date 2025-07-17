import random
import re
from collections import defaultdict

class MarkovChainTextGenerator:
    def __init__(self, order=4):
        self.markov_chain = defaultdict(list)
        self.order = order

    def clean_text(self, text):
        # Remove emojis and special characters
        text = re.sub(r'[^\w\s.,?!\'-]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def build_chain(self, text):
        text = self.clean_text(text)
        words = text.split()

        for i in range(len(words) - self.order):
            key = tuple(words[i:i + self.order])
            next_word = words[i + self.order]
            self.markov_chain[key].append(next_word)

    def generate_text(self, start=None, length=100):
        if not self.markov_chain:
            return "Error: Markov chain is empty."

        # Choose a random starting point if not provided or invalid
        if start:
            start_words = start.split()
            if len(start_words) < self.order:
                print(f"⚠️ Start word should contain at least {self.order} words. Picking random.")
                start_key = random.choice(list(self.markov_chain.keys()))
            else:
                start_key = tuple(start_words[:self.order])
                if start_key not in self.markov_chain:
                    print(f"⚠️ '{start}' not found in training data. Picking random.")
                    start_key = random.choice(list(self.markov_chain.keys()))
        else:
            start_key = random.choice(list(self.markov_chain.keys()))

        result = list(start_key)

        for _ in range(length - self.order):
            next_words = self.markov_chain.get(start_key)
            if not next_words:
                break
            next_word = random.choice(next_words)
            result.append(next_word)
            start_key = tuple(result[-self.order:])

        return ' '.join(result)


if __name__ == "__main__":
    # Load input text
    with open("input.txt", "r", encoding="utf-8") as file:
        text = file.read()

    generator = MarkovChainTextGenerator(order=4)
    generator.build_chain(text)

    print("🔤 Enter a start phrase (at least 4 words recommended):")
    start = input("→ ")

    print("\n📌 Generating text...\n")
    generated_text = generator.generate_text(start, length=100)

    print("📝 Generated Text:\n")
    print(generated_text)
