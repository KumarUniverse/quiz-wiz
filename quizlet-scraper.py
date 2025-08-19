# scrape_quizlet.py
import random
import requests
from bs4 import BeautifulSoup

def scrape_quizlet(topic: str, max_questions: int = 10):
    """
    Scrape Quizlet for `topic`, randomly pick one of top-3 sets,
    produce MCQs: [{question, options, answer}], with options shuffled.
    """
    headers = {"User-Agent": "Mozilla/5.0"}
    search_url = f"https://quizlet.com/subject/{topic.replace(' ', '-')}/"
    search_page = requests.get(search_url, headers=headers, timeout=15)
    soup = BeautifulSoup(search_page.text, "html.parser")

    # Collect top 3 flashcard set links
    set_links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith("/") and "/flashcards/" in href:
            full = "https://quizlet.com" + href
            if full not in set_links:
                set_links.append(full)
        if len(set_links) >= 3:
            break

    if not set_links:
        return [{"error": f"No flashcard sets found for '{topic}'"}]

    chosen_url = random.choice(set_links)
    page = requests.get(chosen_url, headers=headers, timeout=15)
    set_soup = BeautifulSoup(page.text, "html.parser")

    # Extract term/def pairs (front/back alternate)
    cards = set_soup.find_all("span", class_="TermText")
    terms = [c.get_text(strip=True) for c in cards]
    qa_pairs = [(terms[i], terms[i+1]) for i in range(0, len(terms) - 1, 2)]

    if not qa_pairs:
        return [{"error": "Could not extract flashcards."}]

    # Build MCQs: 1 correct + 3 incorrect (when available), shuffled
    all_answers = [b for _, b in qa_pairs]
    questions = []
    for q, correct in qa_pairs[:max_questions]:
        pool = [a for a in all_answers if a != correct]
        k = 3 if len(pool) >= 3 else max(0, len(pool))
        wrongs = random.sample(pool, k) if k > 0 else []
        options = wrongs + [correct]
        random.shuffle(options)
        questions.append({"question": q, "options": options, "answer": correct})

    return questions
