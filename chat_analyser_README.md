# WhatsApp Chat Analyser

Analytics for exported WhatsApp conversations — message statistics, activity timelines, word frequency, and **sentiment analysis built to work on Hinglish**.

**[Live app](https://chatanalyser-6262justk7hchujewy4n9p.streamlit.app/)** · Python · pandas · VADER · Streamlit

---

## Why this exists

Most chat analysers produce the same handful of charts. Two things make them close to useless on real Indian group chats, and this project addresses both.

### 1. English sentiment models score Hinglish as neutral

Indian group chats are heavily **code-mixed** — Hindi written in Roman script, interleaved with English. VADER is tuned on English vocabulary, so transliterated Hindi is simply absent from its lexicon.

A message like *"bakwaas tha yaar, mood kharab ho gaya"* is obviously negative to any Hindi speaker, but VADER recognises none of those tokens and returns a compound score of **0.0 — perfectly neutral**. In a chat that is majority Hinglish, most of the emotional signal is silently discarded.

**The approach here** is a scoring layer on top of VADER:

```
final_score = vader_compound + 0.10 × emoji_score + 0.10 × hinglish_score
```

- **`HINGLISH_SCORE`** — 42 hand-assigned polarity weights for common code-mixed vocabulary, ranging from `jhakaas` (+4) and `zabardast` (+4) through to `bakwaas` (−4) and `ghatiya` (−4). Spelling variants are included where they matter (`accha` / `acha`, `badiya` / `badhiya`), since transliteration is not standardised.
- **`EMOJI_SCORE`** — 25 emoji with explicit polarity, because in casual chat an emoji often carries more sentiment than the surrounding words.
- Remaining emoji are passed through `emoji.demojize()` so VADER can read them as text rather than dropping them.

Classification thresholds follow VADER's convention: ≥ +0.05 positive, ≤ −0.05 negative, neutral in between.

### 2. English stopword lists leave Hinglish chats unreadable

Word-frequency analysis on a Hinglish chat using an English stopword list returns *hai*, *nahi*, *kya*, *mera*, *tha* — grammatical filler, no signal.

This project ships a **377-word Hinglish stopword list** covering pronouns, postpositions, auxiliaries, conjunctions and their common spelling variants, so the frequency charts surface words that actually mean something.

### 3. WhatsApp exports the same person under different names

A participant can appear under a saved contact name, a nickname, or a raw phone number depending on who saved whom. Naive analysis treats one person as several and splits their statistics.

The app includes a **participant renaming step** before analysis, so identities can be normalised — and merged, by assigning two entries the same name.

---

## Features

**Parsing** (`preprocessor.py`)
- Regex extraction of timestamp, sender and message body from the exported `.txt`
- Separates group notifications from user messages
- Derives year, month, day, day-name, hour and minute for time-series analysis

**Statistics** (`helper.py`)
- Total messages, words, media messages and shared links
- Most active participants, with percentage contribution
- Monthly message timeline
- Weekly activity by day of week
- Most common words, filtered through the Hinglish stopword list
- WordCloud

**Sentiment**
- Per-message positive / negative / neutral classification
- Bar and pie distribution charts
- Works for the whole group or a single selected participant

**Text normalisation**
- URL stripping
- Repeated-character collapsing, so `sooooo` and `soo` are treated alike
- Whitespace normalisation

---

## Privacy

The uploaded file is read into memory, decoded, and processed for the duration of the session. Nothing is written to disk or to a database by this application.

That said, a WhatsApp export contains other people's messages and phone numbers. Consider the privacy of everyone in the chat before uploading it anywhere — including here.

---

## Usage

1. In WhatsApp: open a chat → **⋮ → More → Export chat → Without media**
2. Open the [live app](https://chatanalyser-6262justk7hchujewy4n9p.streamlit.app/)
3. Upload the `.txt` file
4. Optionally tick **Rename Participants** to normalise names
5. Choose a participant (or *Overall*) and click **Show Analysis**

---

## Run locally

```bash
git clone https://github.com/nandanigoyal543-jpg/chat_analyser.git
cd chat_analyser

python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

pip install -r requirements.txt
streamlit run app.py
```

---

## Project structure

```
├── app.py             # Streamlit interface and charts
├── helper.py          # statistics, stopwords, lexicons, sentiment scoring
├── preprocessor.py    # regex parsing of the exported chat into a DataFrame
└── requirements.txt
```

**Stack:** Python · pandas · `vaderSentiment` · `emoji` · `urlextract` · `wordcloud` · Matplotlib · Streamlit

---

## Limitations

- **Export format is not universal.** The parser targets the `DD/MM/YYYY, HH:MM am/pm -` format. Exports using US month-first ordering, 24-hour time, or a non-English device locale will not parse without adjusting the regex.
- **The lexicons are hand-built and small** — 42 Hinglish terms and 25 emoji. They cover frequent vocabulary, not regional slang, newer usage, or the long tail of transliteration variants.
- **The `0.10` weights are chosen by judgement, not fitted.** They have not been tuned against labelled data, and no accuracy figure is claimed for the extended scorer versus stock VADER.
- **Lexicon sentiment has no context awareness.** Negation scope, sarcasm and irony are not handled — an inherent limit of the bag-of-words approach rather than a bug.
- Sentiment output is indicative and exploratory, not a psychological measure.

---

## Planned improvements

- Hand-label a test set of messages and report accuracy of the extended scorer against stock VADER, to replace judgement-set weights with measured ones
- Tune the emoji and Hinglish weights on that labelled data
- Day-by-hour activity heatmap
- Emoji frequency analysis
- CSV export of processed results
- Response-time and conversation-initiator analysis

---

*Built by Nandani Goyal.*
