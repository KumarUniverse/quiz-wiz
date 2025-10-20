import random
import requests
from bs4 import BeautifulSoup

def scrape_quizlet(topic: str, max_questions: int = 10):
    """
    Fetch flashcards from a Quizlet subject page.
    Returns a list of MCQs: [{question, options, answer}].
    """
    headers = {"User-Agent": "Mozilla/5.0"}
    #search_url = f"https://quizlet.com/subject/{topic.replace(' ', '-')}/"
    search_url = f"https://quizlet.com/search?query={topic}"

    try:
        search_page = requests.get(search_url, headers=headers, timeout=15)
    except requests.RequestException as e:
        return [{"error": f"Network error fetching Quizlet: {e}"}]

    soup = BeautifulSoup(search_page.text, "html.parser")
    set_links = []

    # Collect up to 3 flashcard set links
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "flash-cards/" in href:
            full = href.split("?")[0]
            if full not in set_links:
                set_links.append(full)
        if len(set_links) >= 3:
            break

    if not set_links:
        return [{"error": f"No flashcard sets found for '{topic}'."}]

    chosen_url = random.choice(set_links)
    try:
        page = requests.get(chosen_url, headers=headers, timeout=15)
    except requests.RequestException as e:
        return [{"error": f"Error fetching Quizlet set: {e}"}]

    set_soup = BeautifulSoup(page.text, "html.parser")

    # Try multiple fallback selectors
    cards = set_soup.find_all("span", class_="TermText") or \
            set_soup.select(".SetPageTerm-content span") or \
            set_soup.select("div[data-testid='SetPageTerm-content'] span")

    terms = [c.get_text(strip=True) for c in cards if c.get_text(strip=True)]
    qa_pairs = [(terms[i], terms[i+1]) for i in range(0, len(terms) - 1, 2)]

    if not qa_pairs:
        return [{"error": f"Could not extract flashcards for '{topic}'."}]

    all_answers = [b for _, b in qa_pairs]
    questions = []

    for q, correct in qa_pairs[:max_questions]:
        pool = [a for a in all_answers if a != correct]
        wrongs = random.sample(pool, min(3, len(pool)))
        options = wrongs + [correct]
        random.shuffle(options)
        questions.append({"question": q, "options": options, "answer": correct})

    return questions
