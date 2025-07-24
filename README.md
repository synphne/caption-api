# SynPhNe GPT Assistant

A **one‑click web tool** that writes LinkedIn captions, carousel copy, event announcements and post‑event summaries in SynPhNe’s exact brand voice. No prompt‑crafting, no jargon, no drift.

---

## 1 · How managers & copywriters use it (no coding)

1. **Open the app link** your intern will share (hosted on Streamlit Cloud).
2. Pick a **caption type** from the dropdown (e.g. *LinkedIn Informative Post*).
3. Fill in the **topic or event name**.
4. Click **Generate**.
5. Copy‑paste the result into LinkedIn, tweak if you wish, and post.

> *Tip — each output already includes the optimal hashtag pair and fits under LinkedIn’s 500‑character fold.*

---

## 2 · If you want to run it locally (optional)

> Only needed for power‑users who prefer to test on their own laptop.

```bash
# 1 Clone the repo
$ git clone https://github.com/synphne/synphne‑gpt‑assistant.git
$ cd synphne‑gpt‑assistant

# 2 Create a virtual environment (recommended)
$ python -m venv venv
$ source venv/bin/activate   # Windows: venv\Scripts\activate

# 3 Install dependencies
$ pip install -r requirements.txt

# 4 Add your OpenAI key (never commit this!)
$ echo "OPENAI_API_KEY=sk‑XXXX" > .env

# 5 Run the app
$ streamlit run main.py
```
Streamlit will open in your browser at **http://localhost:8501**.

---

## 3 · File guide (what lives where)

| File / folder | What it does |
|--------------|-------------|
| **main.py** | The Streamlit front‑end and GPT call logic |
| **prompts.py** | All reusable brand‑safe prompt templates |
| **requirements.txt** | Python packages (Streamlit, OpenAI, python‑dotenv) |
| **.env** | Holds the `OPENAI_API_KEY` – *keep this private!* |
| **brand_guide.md** | SynPhNe tone rules & signature phrases |
| **README.md** | This guide |

---

## 4 · Deployment notes (Streamlit Cloud)

1. Push the repo (minus `.env`) to GitHub.
2. Go to **streamlit.io/cloud → New app → Connect GitHub**.
3. Select `main.py` as the entry point.
4. Under **Secrets**, add your OpenAI key as:
   ```
   OPENAI_API_KEY = sk‑XXXX
   ```
5. Click **Deploy** – you’ll get a public URL you can share with the team.

The app auto‑updates each time you push to `main`.

---

## 5 · How it works (non‑technical summary)

* The tool sends a short instruction ("prompt") plus SynPhNe tone rules to OpenAI’s GPT‑3.5 model.
* GPT returns brand‑perfect copy in under two seconds.
* Each template enforces length, tone, and hashtag rules that mirror SynPhNe’s top‑performing LinkedIn posts.

Total cost: about **$0.002 per caption** – pennies compared to manual copywriting time.

---

## 6 · Road‑map

| Phase | Upgrade |
|------|---------|
| Q2 | Add Slack command `/synphne caption …` |
| Q3 | Fine‑tune GPT model on 100+ historical posts for zero‑prompt tone memory |
| Q4 | Auto‑schedule posts directly to LinkedIn via API |

---

### Questions?
Ping **Lina Elatik** or open an issue in this repo. Happy captioning! :sparkles:
