def count_sentence_stats(sentence: str):
	vowels = set("aeiouAEIOU")
	num_chars = len(sentence)
	words = sentence.split()
	num_words = len(words)
	num_vowels = sum(1 for ch in sentence if ch in vowels)
	return num_chars, num_words, num_vowels

def main():
	sentence = input("Enter a sentence: ")
	chars, words, vowels = count_sentence_stats(sentence)
	print("Number of characters:", chars)
	print("Number of words:", words)
	print("Number of vowels:", vowels)

if __name__ == "__main__":
	main()
