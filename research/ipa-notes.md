# IPA Research Notes for Phyme

> Detailed technical notes on IPA pronunciation data, libraries, and integration strategies.
> Written 2026-03-28.

---

## 1. ARPABET ↔ IPA Mapping (Complete Table)

The CMU dict uses 39 ARPABET phonemes. Each maps to IPA as follows:

### Vowels (15 phonemes)

| ARPABET | IPA | Example | Type | Notes |
|---------|-----|---------|------|-------|
| AA | ɑ | b**o**t, f**a**ther | monophthong | Open back unrounded. With father-bother merger (GenAm) |
| AE | æ | b**a**t | monophthong | Near-open front unrounded |
| AH | ʌ | b**u**ck | monophthong | Near-open central. AH0 often realized as schwa [ə] |
| AO | ɔ | c**au**ght, st**o**ry | monophthong | Open-mid back rounded. Merged with AA in many US dialects (cot-caught merger) |
| AW | aʊ | b**ou**t | diphthong | |
| AY | aɪ | b**i**te | diphthong | |
| EH | ɛ | b**e**t | monophthong | Open-mid front unrounded |
| ER | ɝ | b**ir**d | r-colored | R-colored mid central (stressed) |
| EY | eɪ | b**ai**t | diphthong | |
| IH | ɪ | b**i**t | monophthong | Near-close near-front unrounded |
| IY | i | b**ea**t | monophthong | Close front unrounded |
| OW | oʊ | b**oa**t | diphthong | |
| OY | ɔɪ | b**oy** | diphthong | |
| UH | ʊ | b**oo**k | monophthong | Near-close near-back rounded |
| UW | u | b**oo**t | monophthong | Close back rounded |

### Consonants (24 phonemes)

| ARPABET | IPA | Example | Type |
|---------|-----|---------|------|
| B | b | **b**uy | stop |
| CH | tʃ | **Ch**ina | affricate |
| D | d | **d**ie | stop |
| DH | ð | **th**y | fricative |
| F | f | **f**ight | fricative |
| G | ɡ | **g**uy | stop |
| HH | h | **h**igh | fricative |
| JH | dʒ | **j**ive | affricate |
| K | k | **k**ite | stop |
| L | l | **l**ie | approximant |
| M | m | **m**y | nasal |
| N | n | **n**igh | nasal |
| NG | ŋ | si**ng** | nasal |
| P | p | **p**ie | stop |
| R | ɹ | **r**ye | approximant |
| S | s | **s**igh | fricative |
| SH | ʃ | **sh**y | fricative |
| T | t | **t**ie | stop |
| TH | θ | **th**igh | fricative |
| UH | ʊ | b**oo**k | (listed above as vowel) |
| V | v | **v**ie | fricative |
| W | w | **w**ise | approximant |
| Y | j | **y**acht | approximant |
| Z | z | **z**oo | fricative |
| ZH | ʒ | plea**s**ure | fricative |

### Is the mapping 1:1 or lossy?

**It's lossy in both directions, but more lossy going IPA → ARPABET.**

Key losses going ARPABET → IPA:
- **AH is overloaded**: AH0 (unstressed) is usually [ə] (schwa), AH1 (stressed) is [ʌ]. CMU doesn't distinguish these; IPA does. This matters hugely for rhyme — schwa doesn't really rhyme with the stressed ʌ in "but".
- **No allophonic detail**: ARPABET T is just /t/. IPA can represent [tʰ] (aspirated), [ɾ] (flapped, as in "butter"), [t̚] (unreleased), [ʔ] (glottal stop, as in "button").

Key losses going IPA → ARPABET:
- **Schwa vs strut**: IPA ə and ʌ both map to AH. A rhyming engine treating unstressed ə as equivalent to stressed ʌ misses important nuance.
- **Allophonic variants**: IPA [ɾ] (flap in "butter") has no ARPABET equivalent — it maps to either T or D, losing the information that "butter" and "budder" sound identical.
- **Vowel length**: IPA can mark /iː/ vs /i/. ARPABET has no length marking.
- **R-coloring nuance**: ARPABET ER covers both stressed [ɝ] and unstressed [ɚ]. IPA distinguishes these.
- **Lateral dark L**: [ɫ] (dark L in "bell") vs [l] (light L in "lip") — both just L in ARPABET.
- **Nasalization**: IPA can mark [ã] (nasalized). ARPABET cannot.

**For Phyme specifically**: The AH/schwa ambiguity is the most impactful loss. A word ending in unstressed "-tion" ([ʃən]) doesn't rhyme with "sun" ([sʌn]) the way current ARPABET matching would suggest.

---

## 2. Available IPA Pronunciation Dictionaries

### A. open-dict-data/ipa-dict (GitHub)
- **Coverage**: en_US and en_UK variants
- **Size**: ~135k entries for en_US (comparable to CMU's 133.9k)
- **Format**: TSV — `word\t/IPA/`
- **Source**: Semi-automatic, manually verified for lemmas
- **Multiple pronunciations**: Yes, separated by `, ` (e.g., `a\t/ˈeɪ/, /ə/`)
- **License**: Open/MIT
- **Dialect support**: Separate files for en_US (General American) and en_UK (RP)
- **Quality**: Good. Uses standard IPA conventions. Already includes stress marks.
- **URL**: https://github.com/open-dict-data/ipa-dict

### B. WikiPron (CUNY-CL/wikipron)
- **Coverage**: Mines Wiktionary for 100+ languages
- **Size**: English has one of the largest sets — the scraped database claims 3M+ entries across all languages. For English specifically, probably 60-100k+ entries (can re-scrape for more).
- **Format**: TSV — `word\tIPA_phones` (space-separated)
- **Source**: Scraped from Wiktionary (crowd-sourced, but curated)
- **Dialect filtering**: `--dialect` flag — can target "General American", "Received Pronunciation", etc.
- **Broad vs narrow**: Can request either phonemic (/.../) or phonetic ([...]) transcriptions
- **Quality**: Variable — Wiktionary contributors have different standards. But the tool handles segmentation well.
- **License**: Apache 2.0 for tool; data inherits Wiktionary's CC-BY-SA
- **Best for**: Getting dialect-specific pronunciations, expanding beyond CMU

### C. eSpeak-ng
- **Coverage**: 100+ languages, built-in G2P rules
- **Size**: Not a dictionary per se — it's a rule-based synthesizer that converts any text to IPA
- **Format**: Command-line output or via phonemizer Python wrapper
- **Quality**: Mechanical/rule-based, occasionally weird for English. But universal coverage.
- **Key advantage**: Can phonemize ANY word, not just dictionary entries
- **Key disadvantage**: Rule-based, not based on actual recorded speech. Some English pronunciations are off.

### D. Wiktionary Dumps (direct)
- **Coverage**: ~500k English entries have some pronunciation info
- **Format**: MediaWiki XML dump, needs parsing
- **Quality**: Best crowd-sourced IPA data for English, but requires XML extraction
- **Dialect annotations**: Often tagged with (US), (UK), (Australia), etc.
- **Hassle**: Significant parsing work. WikiPron does this for you.

### E. PHOIBLE (phoible.org)
- **Not a pronunciation dictionary** — it's a database of phoneme inventories for 3000+ languages
- **Useful for**: Understanding what phonemes exist in a language, cross-language comparison
- **Not useful for**: Word-level pronunciation lookup

### Coverage comparison:

| Source | English Words | Multi-pron | Dialect Tags | Format | License |
|--------|-------------|------------|--------------|--------|---------|
| CMU Dict | ~133.9k | Yes (numbered) | GenAm only | ARPABET text | BSD |
| ipa-dict (en_US) | ~135k | Yes | GenAm, RP | IPA TSV | MIT |
| WikiPron (English) | ~60-100k+ | Some | Many dialects | IPA TSV | Apache/CC-BY-SA |
| eSpeak-ng | Unlimited (G2P) | No | ~GenAm | IPA (rule-based) | GPL-3.0 |
| Wiktionary dump | ~500k entries | Yes | Many | XML (needs parsing) | CC-BY-SA |

---

## 3. Python Libraries for IPA

### A. `phonemizer` (bootphon/phonemizer)
**What it does**: Converts text to IPA phonemes. Wraps multiple backends.

```python
from phonemizer import phonemize
# eSpeak backend (IPA output, 100+ languages)
result = phonemize("hello world", backend='espeak', language='en-us')
# result: "həloʊ wɜːld "

# Festival backend (US English only, custom phone set)
result = phonemize("hello world", backend='festival', language='en-us')
```

**Backends**:
- `espeak`: IPA output, 100+ languages, fast. Requires espeak-ng installed.
- `espeak-mbrola`: SAMPA output, 35 languages, slow.
- `festival`: US English only, custom phoneset, supports syllable tokenization.
- `segments`: User-defined G2P mapping.

**Pros**: Multi-backend, well-maintained, good Python API, CLI tool.
**Cons**: Requires system-level espeak-ng install. Festival only for English.
**Install**: `pip install phonemizer` + `brew install espeak` (macOS)
**Best for Phyme**: Universal G2P fallback — any word not in dict → phonemizer → IPA

### B. `epitran` (dmort27/epitran)
**What it does**: Orthography → IPA transliteration. 100+ language-script pairs.

```python
import epitran
epi = epitran.Epitran('eng-Latn')  # English in Latin script
ipa = epi.transliterate('hello')
# 'hɛloʊ'

# Also provides phonetic feature vectors!
tuples = epi.word_to_tuples('cat')
# Each phone gets a 21-dimensional binary feature vector
```

**Key feature**: Phonetic feature vectors. Each IPA phone → binary vector of articulatory features (voicing, place, manner, etc.). This could be incredibly useful for fuzzy rhyme matching — compute distance between phones as Hamming distance between feature vectors.

**Pros**: Feature vectors, multi-language, maintained by academic lab (CUNY).
**Cons**: English requires Flite (lex_lookup) to be installed. Uses CMU dict internally for English.
**Install**: `pip install epitran` + install Flite
**Best for Phyme**: Phonetic feature vectors for computing sound similarity.

### C. `eng-to-ipa` (eng_to_ipa)
**What it does**: Specifically converts English text → IPA. Uses CMU dict internally.

```python
import eng_to_ipa as ipa
result = ipa.convert("The quick brown fox")
# 'ðə kwɪk braʊn fɑks'

# Multiple pronunciations
result = ipa.ipa_list("record")
# [['rəˈkɔrd', 'rɪˈkɔrd', 'ˈrɛkərd']]

# Check CMU coverage
ipa.isin_cmu("emoji")  # False

# Built-in rhyming (basic)
ipa.get_rhymes("cat")
# [['bat', 'brat', 'chat', 'fat', ...]]
```

**Pros**: Dead simple API. Multiple pronunciations. Built-in rhyme function.
**Cons**: Just wraps CMU dict → IPA conversion. No real G2P for OOV words (marks them with *). Small project, minimal maintenance.
**Install**: `pip install eng-to-ipa`
**Best for Phyme**: Quick CMU → IPA conversion layer. Could use its mapping table.

### D. `ipapy`
**What it does**: IPA string manipulation — parsing, validation, feature queries.

```python
from ipapy import UNICODE_TO_IPA, is_valid_ipa
from ipapy.ipastring import IPAString

# Parse IPA string
s = IPAString(unicode_string="həˈloʊ")
# Filter by type
vowels = s.vowels  # [ə, oʊ...]
consonants = s.consonants

# Get phone properties
phone = UNICODE_TO_IPA["ɑ"]
# Properties: height=open, backness=back, roundness=unrounded, type=vowel

# Validate IPA
is_valid_ipa("həˈloʊ")  # True
is_valid_ipa("hello")   # False (not IPA)
```

**Pros**: Rich IPA character database with descriptors (height, backness, roundness, voicing, place, manner). Good for building vowel-distance metrics.
**Cons**: Last updated 2019. No G2P capability. Pure manipulation library.
**Install**: `pip install ipapy`
**Best for Phyme**: IPA string parsing and phone property queries. Build vowel space distance from descriptors.

### E. `gruut` + `gruut-ipa`
**What it does**: Full NLP pipeline — tokenization, text normalization, IPA phonemization.

```python
from gruut import sentences

for sent in sentences("I read the book", lang="en-us"):
    for word in sent:
        if word.phonemes:
            print(word.text, *word.phonemes)
# I ˈaɪ
# read ɹ ˈɛ d   (past tense — handles homograph disambiguation!)
# the ð ə
# book b ˈʊ k
```

**gruut-ipa** separately:
```python
# Convert between IPA, espeak, and SAMPA notation
# python3 -m gruut_ipa convert ipa espeak "mʊmˈbaɪ"
# [[mUm'baI]]

# Split IPA into phones
# python3 -m gruut_ipa phones "ˈjɛs|ˈt͡ʃuːz"
# ˈj ɛ s | ˈt͡ʃ uː z

# Group phones into language-specific phonemes
# python3 -m gruut_ipa phonemes en-us "/dʒʌst ə kaʊ/"
# d͡ʒ ʌ s t ə k aʊ
```

**Pros**: Homograph disambiguation! Text normalization (numbers, currency). Multi-language. IPA phoneme grouping that knows about diphthongs. Converts between IPA/espeak/SAMPA.
**Cons**: Linux-focused (may need tweaks on macOS). Built for TTS pipelines. Development seems stalled (rhasspy project).
**Install**: `pip install gruut` (add `[lang]` extras for non-English)
**Best for Phyme**: Homograph disambiguation and IPA phoneme grouping.

### F. `g2p-en`
**What it does**: English G2P with neural net fallback for OOV words.

```python
from g2p_en import G2p
g2p = G2p()
result = g2p("I'm an activationist.")
# ['AY1', ' ', 'AH0', 'M', ' ', 'AE1', 'N', ' ', 'AE2', 'K', 'T', ...]
```

**Key feature**: Neural seq2seq model predicts pronunciation for ANY word, even made-up ones.
**Output**: ARPABET (not IPA) — but could be piped through a converter.
**Homograph handling**: Uses POS tags to disambiguate (e.g., "refuse" verb vs noun).
**Pros**: Handles OOV words via learned model. POS-based homograph disambiguation.
**Cons**: Outputs ARPABET, not IPA. Depends on NLTK.
**Install**: `pip install g2p_en`
**Best for Phyme**: OOV word handling in ARPABET. Could pair with ARPABET→IPA converter.

---

## 4. G2P (Grapheme-to-Phoneme) Options for OOV Words

For words not in any dictionary, we need G2P:

| Tool | Output Format | Method | OOV Quality | Speed |
|------|--------------|--------|-------------|-------|
| g2p-en | ARPABET | Neural seq2seq + CMU dict | Good for English | Fast |
| eSpeak-ng | IPA | Rule-based | Decent, sometimes robotic | Fast |
| phonemizer (espeak) | IPA | Rule-based (wraps espeak) | Same as eSpeak | Fast |
| epitran | IPA | Rule-based + Flite | OK for common patterns | Fast |
| gruut | IPA | CRF model + lexicon | Good | Medium |
| DeepPhonemizer | IPA | Transformer model | Very good | Slow (GPU) |

**Recommended strategy for Phyme**:
1. Look up in primary dictionary (CMU or IPA dict)
2. If not found, try g2p-en (neural, ARPABET) → convert to IPA
3. If still weird, fall back to eSpeak via phonemizer (rule-based, IPA)

---

## 5. Practical Tradeoffs: CMU vs IPA Sources

### What CMU gives you that's hard to replace:
- **134k words, clean, consistent** — one annotation standard, one dialect (GenAm)
- **Stress markers** — built into vowel codes (0/1/2)
- **Multiple pronunciations** — numbered variants (WORD(1), WORD(2))
- **Battle-tested** — used in NLTK, g2p-en, eng-to-ipa, hundreds of projects
- **Simple format** — ASCII, easy to parse, no Unicode headaches

### What IPA gives you that CMU doesn't:
- **Finer vowel distinctions** — schwa (ə) vs strut (ʌ), which CMU conflates in AH
- **Dialect variation** — ipa-dict has en_US + en_UK; WikiPron can target any dialect
- **Allophonic detail** — flapping (ɾ), aspiration (tʰ), glottal stops (ʔ)
- **Cross-language potential** — same notation for Spanish, French, etc.
- **Vowel space geometry** — IPA phones have defined articulatory features (height, backness, roundness) that enable continuous distance metrics instead of discrete matching
- **Diphthong transparency** — aɪ is visibly "a sliding to ɪ"; AY is opaque

### What IPA makes harder:
- **Unicode complexity** — combining diacritics, multiple ways to encode same phone (t͡ʃ vs tʃ vs ʧ)
- **Segmentation** — splitting an IPA string into phones requires knowing about combining chars, ties, and diacritics. Libraries like ipapy and gruut-ipa handle this.
- **Consistency** — different sources use slightly different IPA conventions. eSpeak uses ɹ for English R; some sources use r. Both are "correct" at different levels of detail.
- **Stress marking** — IPA uses ˈ (primary) and ˌ (secondary) before the stressed syllable. This is positionally different from ARPABET's digit-on-vowel system.

---

## 6. Architecture: IPA as Internal Representation

### Proposed approach: Dual-layer phoneme system

```
                    ┌─────────────┐
  CMU Dict ──────── │  ARPABET    │ ── converter ──┐
                    └─────────────┘                │
                                                   ▼
  ipa-dict ──────── ┌─────────────┐         ┌─────────────┐
                    │  IPA (raw)  │ ──────► │  Internal    │ ◄── rhyme engine
  WikiPron ──────── └─────────────┘         │  IPA repr   │
                                            └─────────────┘
  eSpeak G2P ────── (IPA output) ────────────────┘
```

**Internal representation**: A normalized subset of IPA.
- Use ~45 IPA symbols for English (the 39 ARPABET equivalents + schwa + a few allophones)
- Define a `Phoneme` class with articulatory features (from ipapy descriptors)
- Stress stored as a property on vowel phonemes (like ARPABET, but richer)

### Conversion strategy:

```python
# ARPABET → Internal IPA
ARPABET_TO_IPA = {
    'AA': 'ɑ',   'AE': 'æ',   'AH': 'ʌ',  # AH0 → ə (special case!)
    'AO': 'ɔ',   'AW': 'aʊ',  'AY': 'aɪ',
    'B':  'b',    'CH': 'tʃ',  'D':  'd',
    'DH': 'ð',   'EH': 'ɛ',   'ER': 'ɝ',  # ER0 → ɚ (special case!)
    'EY': 'eɪ',  'F':  'f',   'G':  'ɡ',
    'HH': 'h',   'IH': 'ɪ',   'IY': 'i',
    'JH': 'dʒ',  'K':  'k',   'L':  'l',
    'M':  'm',    'N':  'n',   'NG': 'ŋ',
    'OW': 'oʊ',  'OY': 'ɔɪ',  'P':  'p',
    'R':  'ɹ',   'S':  's',   'SH': 'ʃ',
    'T':  't',    'TH': 'θ',   'UH': 'ʊ',
    'UW': 'u',    'V':  'v',   'W':  'w',
    'Y':  'j',    'Z':  'z',   'ZH': 'ʒ',
}

def arpabet_to_ipa(phones: list[str]) -> list[str]:
    """Convert ARPABET phone sequence to IPA."""
    result = []
    for phone in phones:
        # Strip stress digit
        base = phone.rstrip('012')
        stress = phone[len(base):] if len(phone) > len(base) else None
        
        # Special case: AH0 is schwa, not strut
        if base == 'AH' and stress == '0':
            result.append('ə')
        elif base == 'ER' and stress == '0':
            result.append('ɚ')
        else:
            ipa = ARPABET_TO_IPA.get(base, base)
            # Prepend stress mark if needed
            if stress == '1':
                result.append('ˈ' + ipa)
            elif stress == '2':
                result.append('ˌ' + ipa)
            else:
                result.append(ipa)
    return result
```

### Accepting both CMU and IPA input:

```python
class PhonemeSequence:
    """Unified phoneme representation."""
    
    def __init__(self, ipa_phones: list[str]):
        self.phones = ipa_phones
    
    @classmethod
    def from_arpabet(cls, arpabet: list[str]) -> 'PhonemeSequence':
        return cls(arpabet_to_ipa(arpabet))
    
    @classmethod
    def from_ipa(cls, ipa_string: str) -> 'PhonemeSequence':
        # Use gruut-ipa or ipapy to segment
        return cls(segment_ipa(ipa_string))
    
    @classmethod
    def from_word(cls, word: str) -> 'PhonemeSequence':
        # 1. Check IPA dict
        # 2. Check CMU dict → convert
        # 3. G2P fallback
        ...
```

---

## 7. Vowel Space Distance (Key Insight for Rhyming)

IPA vowels have defined articulatory features that form a geometric space:

```
        Front    Central    Back
Close    i  y    ɨ  ʉ      ɯ  u
         ɪ  ʏ              ʊ
Close-mid e  ø   ɘ  ɵ      ɤ  o
Mid            ə
Open-mid ɛ  œ   ɜ  ɞ      ʌ  ɔ
         æ
Open     a  ɶ             ɑ  ɒ
```

For rhyming, we can compute vowel distance as the geometric distance in this space:

```python
# Vowel features: (height_numeric, backness_numeric, rounded)
VOWEL_FEATURES = {
    'i':  (7, 0, False),  # close front unrounded
    'ɪ':  (6, 1, False),  # near-close near-front unrounded
    'e':  (5, 0, False),  # close-mid front unrounded
    'ɛ':  (3, 0, False),  # open-mid front unrounded
    'æ':  (2, 0, False),  # near-open front unrounded
    'a':  (1, 0, False),  # open front unrounded
    'ə':  (4, 2, False),  # mid central
    'ʌ':  (3, 2, False),  # open-mid central (back in some analyses)
    'ɑ':  (1, 4, False),  # open back unrounded
    'ɔ':  (3, 4, True),   # open-mid back rounded
    'o':  (5, 4, True),   # close-mid back rounded
    'ʊ':  (6, 3, True),   # near-close near-back rounded
    'u':  (7, 4, True),   # close back rounded
    'ɝ':  (4, 2, False),  # r-colored mid central (treat like ə + ɹ)
}

def vowel_distance(v1: str, v2: str) -> float:
    """Euclidean distance in vowel space."""
    f1 = VOWEL_FEATURES[v1]
    f2 = VOWEL_FEATURES[v2]
    return ((f1[0]-f2[0])**2 + (f1[1]-f2[1])**2 + (f1[2]!=f2[2])*4)**0.5
```

This enables **gradient rhyme scoring** instead of binary match/no-match:
- "cat" (æ) ↔ "bet" (ɛ): distance ≈ 1.0 (close — slant rhyme)
- "cat" (æ) ↔ "boot" (u): distance ≈ 6.4 (far — no rhyme)

---

## 8. Recommendations for Phyme

### Short-term (can do now):
1. **Add ARPABET→IPA converter** using the mapping table above (pay special attention to AH0→ə and ER0→ɚ)
2. **Integrate eng-to-ipa** for quick CMU→IPA display (it's basically a thin wrapper)
3. **Add vowel distance metric** using IPA vowel features — even without changing the underlying data

### Medium-term (next iteration):
4. **Adopt IPA as internal representation** with the `PhonemeSequence` class pattern
5. **Load ipa-dict alongside CMU** — merge for broader coverage
6. **Add G2P fallback** using phonemizer/eSpeak for OOV words
7. **Use ipapy or gruut-ipa** for IPA string parsing and phone property lookup

### Long-term (future vision):
8. **WikiPron integration** for dialect-specific pronunciation variants
9. **Phonetic feature vectors** (from epitran) for ML-based rhyme similarity
10. **Cross-language rhyming** — Spanish words that rhyme with English words, etc.

### What NOT to do:
- Don't drop CMU dict — it's clean, well-tested, and the IPA sources are essentially derived from it anyway
- Don't try to support all of IPA — narrow transcription with diacritics is overkill for rhyming
- Don't use a single G2P source — combine dictionary lookup + neural + rule-based fallback
