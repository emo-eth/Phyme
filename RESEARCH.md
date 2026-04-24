# Phyme Research & Brainstorm

## Repo State (2026-03-28)

### Branches
| Branch | Status | Key Changes |
|--------|--------|-------------|
| `master` | Published PyPI version | CMU dict, ARPABET phones, trie-based rhyme search |
| `dev` | Minor cleanup | Removes unused search, list cast |
| `phone-classes` | **Most advanced** | `Phone`, `MetaPhone`, `MetaVowel`, `MetaShortVowel` classes; type hints; vowel mapping analysis |
| `type-hints` | Subset of phone-classes | Early type hints + Permutation enum |
| `feature/11-family-rhyme` | Complete-ish | Recursive family/partner rhyme methods |
| `feature/wildcard-trie-search` | Stub | Constants only |
| `feature/phyme-tests` / `feature/rhymeUtilTests` / `feature/rhymetrie-tests` | Test branches | Various test additions |

### Current Architecture
- **Data**: CMU Pronouncing Dictionary (ARPABET notation), preprocessed into JSON
- **Core**: Reversed-phone trie for suffix matching (rhymes = shared endings)
- **Rhyme types**: Perfect, Family, Partner, Additive, Subtractive, Substitution, Assonance, Consonant
- **phone-classes branch additions**:
  - `Phone` class with vowel/consonant/voiced properties
  - `MetaPhone`: phone that matches ANY of its replacement phones (fuzzy matching)
  - `MetaVowel`: MetaPhone that counts as a vowel (for diphthong components)
  - `MetaShortVowel`: for semivowels (W→UW, Y→IY) that shouldn't count as syllables
  - `ShortVowel`: vowel that doesn't count toward syllable count
  - `OptionalPhone`, `ConsolidatedPhone`: stubbed out
  - Extensive vowel mapping notes in `mappings.json`

### Existing "Meta Vowel" Work (mappings.json)
The mappings file contains a hand-crafted analysis of vowel relationships:
- **Pure vowels**: A=AA, E=EY, I=IY, O=OW, U=UW
- **Diphthongs decomposed**: AY=[AA,IY], OY=[OW,IY], AW=[AA,UW], EY=[EY,IY]
- **Dialect-specific notes**: "not in california english: AO, EH"
- **Replacement sets**: Each CMU vowel mapped to which pure vowels it can substitute for

## Research Areas

### 1. IPA vs ARPABET / CMU Dict Replacement
**Status**: Not started
**Question**: Can we move from CMU's ARPABET to IPA, and what do we gain?

#### Findings

> Researched 2026-03-28. Detailed notes in `research/ipa-notes.md`.

##### The ARPABET↔IPA Mapping: Close but Lossy

The 39 CMU/ARPABET phonemes map almost 1:1 to IPA symbols (see full table in `research/ipa-notes.md`). The mapping is clean for consonants. For vowels, there are two critical losses:

1. **AH is overloaded** — CMU uses AH for both the stressed vowel in "strut" (IPA: ʌ) AND the unstressed schwa in "about" (IPA: ə). These are different sounds that shouldn't rhyme with each other. Stress digit (AH0 vs AH1) is the only distinguisher, and Phyme's current trie strips stress for matching.

2. **ER is overloaded** — Similarly, stressed "bird" [ɝ] and unstressed "letter" [ɚ] are both ER. Different stress, different rhyme behavior.

Going the other direction (IPA → ARPABET), we lose more: allophonic detail like flapping (the [ɾ] in "butter" that makes it sound like "budder"), aspiration, vowel length, nasalization, and dark-L vs light-L. These matter for natural-sounding rhyme perception.

**Bottom line**: ARPABET→IPA is nearly lossless with the AH0/ER0 special case. IPA→ARPABET is lossy but acceptable for broad phonemic work. The conversion is straightforward to implement.

##### Available IPA Dictionaries

| Source | English Words | Multi-pron | Dialect Tags | License |
|--------|-------------|------------|--------------|---------|
| CMU Dict | ~133.9k | Yes | GenAm only | BSD |
| [ipa-dict](https://github.com/open-dict-data/ipa-dict) (en_US) | ~135k | Yes | GenAm, RP | MIT |
| [WikiPron](https://github.com/CUNY-CL/wikipron) | ~60-100k+ | Some | Many dialects | Apache/CC-BY-SA |
| eSpeak-ng (G2P) | Unlimited | No | GenAm-ish | GPL-3.0 |
| Wiktionary dump | ~500k entries | Yes | Many | CC-BY-SA |

**ipa-dict** is the most direct CMU replacement — comparable size (~135k entries), IPA format, includes both en_US and en_UK. It's TSV, trivial to parse.

**WikiPron** is the best for dialect work — it scrapes Wiktionary and can filter by dialect tag ("General American", "Received Pronunciation", "Australian", etc.). The `--dialect` flag and `--narrow` option give fine control. 3M+ entries across all languages.

**eSpeak-ng** (via `phonemizer`) is the universal G2P fallback — any word in, IPA out. Rule-based, not perfect, but covers words not in any dictionary.

##### Python Libraries (Ranked for Phyme Relevance)

1. **`phonemizer`** — Best G2P wrapper. Wraps eSpeak (IPA, 100+ langs), Festival (US English, syllables), MBROLA (SAMPA). `pip install phonemizer` + system espeak-ng. This is the fallback for words not in any dictionary.

2. **`gruut` + `gruut-ipa`** — Full NLP pipeline with homograph disambiguation ("I read" past vs present gets different IPA). gruut-ipa handles IPA↔eSpeak↔SAMPA conversion and proper IPA segmentation into phonemes. Knows that "aʊ" is one phoneme in English, not two.

3. **`ipapy`** — IPA string manipulation with articulatory feature queries (height, backness, roundness, voicing, place, manner). Perfect for building a vowel-distance metric. Last updated 2019 but stable.

4. **`epitran`** — Orthography→IPA with 21-dimensional phonetic feature vectors per phone. Feature vectors enable computing sound similarity as vector distance — powerful for fuzzy/slant rhyme scoring.

5. **`eng-to-ipa`** — Simplest CMU→IPA converter. Wraps CMU dict, adds stress marks, returns IPA strings. Has a basic `get_rhymes()` function. Good for validation/comparison.

6. **`g2p-en`** — Neural G2P for English, outputs ARPABET (not IPA). Handles OOV words via seq2seq model. POS-based homograph disambiguation. Would need ARPABET→IPA post-processing.

##### G2P Strategy for OOV Words

For words not in any dictionary, chain fallbacks:
1. Dictionary lookup (CMU or ipa-dict)
2. `g2p-en` neural model (ARPABET → convert to IPA)
3. `phonemizer`/eSpeak rule-based fallback (IPA directly)

##### Key Insight: Vowel Space Distance

IPA vowels have defined positions in articulatory space (height × backness × roundness). This enables **continuous rhyme scoring** instead of binary match/no-match:

```
        Front    Central    Back
Close    i                   u
         ɪ                   ʊ
Close-mid e        ə         o
Open-mid ɛ        ʌ         ɔ
Near-open æ
Open     a                   ɑ
```

Distance between vowels = geometric distance in this space. "cat" (æ) to "bet" (ɛ) is close (good slant rhyme). "cat" (æ) to "boot" (u) is far (no rhyme). This is what the existing `mappings.json` work was reaching for, but IPA gives us a principled, continuous metric instead of hand-crafted replacement sets.

##### Recommendation: Dual-Layer Architecture

Don't drop CMU — instead, use IPA as the internal representation while accepting both inputs:

```
CMU Dict ──► ARPABET→IPA converter ──┐
                                     ├──► Internal IPA repr ◄── rhyme engine
ipa-dict ──► IPA normalizer ─────────┘
eSpeak G2P ──► IPA output ───────────┘
```

- Convert CMU ARPABET to IPA at load time (special-case AH0→ə, ER0→ɚ)
- Accept IPA data from ipa-dict, WikiPron, or eSpeak directly
- Build phoneme distance metrics on IPA articulatory features
- Keep ARPABET as an input format for backward compatibility

See `research/ipa-notes.md` for code snippets, the full ARPABET→IPA mapping table, and the vowel distance function.

---

### 2. Regional Dialect Modeling
**Status**: Research complete (2026-03-28)
**Question**: How to adapt phoneme matching to regional American English dialects?

#### Findings

**Summary**: American English has 6 major vowel phenomena that meaningfully affect what rhymes. These can be modeled as 5 dialect profiles covering most variation. The key insight is that most variation comes from **mergers** (two phonemes becoming one) rather than shifts (phonemes moving but staying distinct). Mergers are what create/destroy rhyme pairs.

**Top Mergers by Rhyme Impact (ARPABET)**:

| # | Merger | Phones | Type | Prevalence |
|---|--------|--------|------|------------|
| 1 | **Cot-caught** | AA ↔ AO | Unconditional | ~50%+ growing |
| 2 | **AY monophthong** | AY → AA | Before voiced/final | ~30% (South) |
| 3 | **Pin-pen** | IH ↔ EH | Before nasals (M,N,NG) | ~30% (South) |
| 4 | **Mary-marry-merry** | AE ↔ EH ↔ EY | Before R | ~60% |
| 5 | **Fill-feel** | IH ↔ IY | Before L | ~25% |
| 6 | **Full-fool** | UH ↔ UW | Before L | ~25% |

**5 Proposed Dialect Profiles**:
1. **General American / Western** — Cot-caught merged, Mary-marry-merry merged. The "default" for young Americans.
2. **Southern** — Pin-pen merged, AY monophthongized, fill-feel/full-fool merged. No cot-caught.
3. **Inland North (Great Lakes)** — No mergers unique to it, but NCVS chain shift creates near-mergers between adjacent vowels (AE≈EH, AA≈AE, EH≈AH).
4. **Northeast Corridor (NYC/Philly)** — Most conservative. Maintains all contrasts. Fewest "squishy" rhymes.
5. **Midland / Transitional** — Cot-caught in transition, Mary-marry-merry merged.

**Key Implementation Insight**: Mergers are either **unconditional** (cot-caught: AA=AO everywhere) or **conditional** (pin-pen: IH=EH only before nasals). Conditional mergers need phonetic context. The existing `MetaPhone` class is a natural fit — dialect profiles construct MetaPhones at load time.

**Suggested "Any Dialect" Mode**: Union of ALL mergers for maximum squishiness. Treats AA/AO as interchangeable, IH/EH as interchangeable before nasals, etc. Best for creative rhyming (songwriting, poetry).

**No existing Python library models American dialect variation computationally.** This would be novel. Closest tools: `panphon` (phonological feature vectors), `epitran` (G2P), and CMU dict itself. The approach should be rule-based transforms on CMU output.

**Detailed technical notes**: See `research/dialect-notes.md` for full merger tables, proposed dialect profile JSON schema, implementation recommendations, and Python dataclass definitions.

---

### 3. Meta Vowels & Diphthong Squishiness
**Status**: Partially explored in phone-classes branch
**Question**: How should diphthongs interact with their component monophthongs in rhyme matching?

#### Findings

##### Phonological Theory: Why Diphthong-Monophthong Rhyming Works

Diphthongs are vowels with two targets — the tongue moves during pronunciation. In IPA, English diphthongs are transcribed as two-segment sequences (AY = /aɪ/, AW = /aʊ/, OY = /ɔɪ/), while ARPABET encodes each as a single symbol. This mismatch is the source of both the problem and the opportunity.

Phonologically, diphthongs sit on a spectrum between monophthongs and vowel sequences. A "closing" diphthong like AY starts at a lower, more open vowel (/a/) and glides toward a higher, closer vowel (/ɪ/). The onset is where most of the acoustic energy lives — it's longer and louder. The offglide is shorter and can be quite reduced, especially in casual speech.

This means **onset matching produces stronger-sounding slant rhymes than offglide matching** for stressed syllables. "time" (/taɪm/) and "spa" (/spɑ/) share the /ɑ/ quality at the point of maximum energy. "time" and "free" share /i/ quality, but only in the trailing portion.

**Songwriting context**: Slant rhyme (also: half rhyme, near rhyme, lazy rhyme) is defined as rhyme where either the vowel or consonant segments are similar but not identical. In rap, assonance-based rhyming (shared vowel sounds) is the default, not the exception. Eminem, Nas, MF DOOM, and others routinely treat diphthong-monophthong pairs as rhymes. The Wikipedia article on slant rhyme notes: "Half rhyme is often used, along with assonance, in rap music... to avoid rhyming clichés or obvious rhymes."

**Key insight for implementation**: The "squishiness" isn't subjective hand-waving — it maps directly to the phonological structure of diphthongs. A diphthong has an onset target and an offglide target. Matching either target against a monophthong produces a real acoustic similarity that listeners perceive.

##### How Existing Tools Handle This

**pronouncing** (Python, CMU dict wrapper): Purely exact rhyming-part match. `rhyming_part()` extracts everything from the last stressed vowel onward, then does exact string comparison. No fuzzy vowel matching at all. "time" only rhymes with words ending in "AY1 M".

**Datamuse/RhymeZone**: Offers `rel_rhy` (perfect rhyme) and `rel_nry` (approximate/near rhyme). The near rhyme algorithm is proprietary but appears to use phonetic distance metrics. Also offers `rel_cns` (consonant match: "sample" → "simple") which is similar to Phyme's consonant rhyme. No documented vowel decomposition or diphthong component matching.

**NLTK CMUdict**: Raw dictionary access, no rhyme-finding logic built in.

**The gap**: No existing open-source tool treats diphthong decomposition as a first-class feature. Phyme's MetaVowel concept would be novel.

##### Data Structure for Squishy Matching

The current trie stores reversed phone sequences for suffix matching. Rhymes share suffixes, so they share trie prefixes when reversed. The `children` dict maps `Phone → RhymeTrieNode`.

**Recommended approach: Search-time expansion** (not insert-time).

The trie stays as-is. When searching, each vowel phone is expanded to its equivalence set based on the squishiness level:

```
squishiness=0 → {AY1}  (exact)
squishiness=1 → {AY1, AY2}  (stress-flexible)
squishiness=2 → {AY1, AA1}  (onset component)
squishiness=3 → {AY1, AA1, IY1}  (onset + offglide)
squishiness=4 → {AY1, AA1, IY1, AH1, AE1, IH1, AW1, OY1}  (full class)
```

At each trie node, instead of `self.children.get(phone)`, iterate over the equivalence set and follow all matching branches. This is a generalization of what `_replace_phones` already does for MetaPhones.

**Why not insert-time expansion**: It would require inserting each word under multiple vowel keys, ballooning storage and making it impossible to distinguish exact from fuzzy matches at query time.

**Why not decompose diphthongs into multi-phone sequences**: It breaks the 1:1 phone-to-node invariant, changes syllable counts, and creates structural mismatches with the CMU data format. AY should remain one phone in the trie; it just matches MORE phones during search.

##### Existing MetaVowel Code: Status Assessment

**Working**:
- `MetaPhone.__eq__` correctly matches any replacement phone
- `MetaVowel` / `MetaShortVowel` type hierarchy is sound
- Y→IY0 and W→UW0 semivowel handling works
- `_replace_phones` in the trie does search-time expansion

**Bug found**: `MetaPhone.__hash__` uses `super().__hash__()` = `hash((self.phone, Phone))`, but `MetaPhone.__eq__` can return True for phones with different hashes. This violates the Python hash contract (`a == b → hash(a) == hash(b)`). Dict lookups (`self.children.get(phone)`) will silently fail when the search phone's hash doesn't match the stored MetaPhone's hash. This must be fixed before MetaVowels can work in the trie.

**Incomplete**:
- `phone_mapper` only handles Y and W, not diphthongs (AY, OY, AW, etc.)
- No vowel equivalence data structure (mappings.json is notes, not code)
- No squishiness parameter
- No stress-aware flexibility
- `CompoundMetaPhone` (commented out) was heading toward multi-phone decomposition — wrong direction
- No bidirectional matching (MetaVowels only expand the search phone, not the stored phone)

**Path to finish**: See detailed notes in `research/meta-vowel-notes.md` sections 3 and 4. TL;DR:
1. Fix the hash contract bug
2. Build a `VowelEquivalence` class with the decomposition table
3. Add `squishiness` parameter to search methods
4. Add `get_meta_rhymes()` public API
5. Add stress normalization at higher squishiness levels

##### Squishiness Parameterization

Five proposed levels, from strict to loose:

| Level | Name | What Matches | Example: "time" (AY) matches... |
|-------|------|-------------|--------------------------------|
| 0 | EXACT | Same phone only | AY1 |
| 1 | NEIGHBOR | Close monophthong neighbors | AY1 + stress variants |
| 2 | ONSET | Diphthong onset component | AY1 + AA1 ("spa", "calm") |
| 3 | FULL COMPONENT | Onset + offglide | AY1 + AA1 + IY1 ("spa", "free") |
| 4 | PURE CLASS | Any shared pure vowel class | AY1 + AA1 + IY1 + AH1 + AE1 + IH1 + AW1 + ... |

Higher levels include all matches from lower levels. Results should be ranked by match quality (exact > neighbor > onset > offglide > class).

##### Vowel Reduction in Unstressed Positions

Unstressed vowels in English collapse toward schwa (AH0, IH0). In casual speech, the vowel in the second syllable of "comfortable" is nearly indistinguishable from the second vowel in "chocolate" — both are reduced.

Recommendation: At squishiness ≥ 2, treat unstressed (stress=0) vowel positions as wildcards. Any unstressed vowel matches any other unstressed vowel. This massively improves multi-syllable rhyme finding (where unstressed syllables abound) without sacrificing the precision of stressed-vowel matching that makes a rhyme *sound* right.

##### Multi-Phone Substitution: Don't Decompose

The trie should NOT decompose AY into [AA, IY] as separate nodes. This would:
- Break the 1:1 phone-to-node invariant
- Change trie depth for diphthong words
- Break syllable counting (decomposed form looks like 2 syllables)
- Create insert/search asymmetry

Instead, use the MetaVowel mechanism: AY remains one phone but can *match* AA or IY at search time. This is equivalent in expressive power but preserves the trie structure.

##### Detailed notes: `research/meta-vowel-notes.md`

---

### 4. Architecture / Next Steps
**Status**: Synthesized (2026-03-28)
**Question**: What's the path from current state to a modern, dialect-aware rhyming engine?

#### Findings

##### The Big Picture

Phyme's existing trie architecture is sound. The `phone-classes` branch was heading in exactly the right direction. The path forward has three independent axes that converge:

1. **IPA as internal representation** — gives us continuous vowel distance metrics instead of binary matching
2. **Dialect profiles** — runtime-selectable merger rules that expand what counts as "the same phone"
3. **Meta vowels with squishiness** — diphthong component matching at configurable fuzziness levels

These three combine into a single search-time expansion mechanism: when searching the trie, each vowel phone is expanded to an equivalence set determined by `(squishiness_level, dialect_profile, vowel_distance_threshold)`.

##### Proposed Architecture

```
┌─────────────────────────────────────────────────┐
│                  Data Sources                    │
│  CMU Dict ──► ARPABET→IPA ──┐                   │
│  ipa-dict ──► normalize ────┤──► Unified IPA    │
│  WikiPron ──► normalize ────┘    Phone objects   │
│  eSpeak G2P (fallback for OOV)                   │
└──────────────────┬──────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────┐
│              Phone Object Layer                  │
│  Phone / MetaVowel / MetaShortVowel / ...       │
│  Each carries: IPA symbol, articulatory features │
│  (height, backness, roundness), stress level,    │
│  diphthong components (if applicable)            │
└──────────────────┬──────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────┐
│           Vowel Equivalence Engine               │
│  Input: (phone, squishiness, dialect_profile)    │
│  Output: set of equivalent phones to search      │
│                                                  │
│  Combines:                                       │
│  - Diphthong decomposition (meta vowels)         │
│  - Dialect mergers (cot-caught, pin-pen, etc.)   │
│  - Vowel distance threshold (IPA geometry)       │
│  - Stress relaxation (schwa wildcards)           │
└──────────────────┬──────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────┐
│              Rhyme Trie (unchanged)              │
│  Insert: words keyed by reversed phone sequence  │
│  Search: walk trie, at each vowel node expand    │
│          to equivalence set and follow all       │
│          matching branches                       │
│  Score: rank results by match quality            │
│         (exact > neighbor > onset > offglide)    │
└─────────────────────────────────────────────────┘
```

##### Critical Bug to Fix First

`MetaPhone.__hash__` violates Python's hash contract. `a == b` can be True while `hash(a) != hash(b)`. This means dict lookups in the trie's `children` dict silently fail for MetaPhone keys. Fix: either make MetaPhones non-hashable (use linear scan in children) or hash based on the replacement set (expensive but correct). Or: don't use MetaPhones as dict keys at all — use search-time expansion where the search phone is always a plain Phone, and the equivalence engine provides the set of children keys to check.

##### Implementation Roadmap

**Phase 0: Fix foundations (phone-classes branch)**
- Fix the hash contract bug
- Merge the type hints and Phone class hierarchy into a clean `v2` branch
- Add proper tests for MetaVowel equality/matching
- Wire up `phone_mapper` for all diphthongs (AY, OY, AW — not just Y/W)

**Phase 1: Squishiness MVP**
- Build `VowelEquivalence` class with the 5-level decomposition table
- Modify `search_permutations` to accept `squishiness` param
- Add `get_meta_rhymes(word, squishiness=2)` public API
- Handle stress normalization (strip stress for equivalence lookup, re-apply for trie walk)
- Result ranking by match quality

**Phase 2: Dialect profiles**
- Define 5 dialect profiles as JSON/dataclass
- Each profile = list of mergers (unconditional or conditional)
- `VowelEquivalence` accepts a `dialect` param that adds dialect mergers to the expansion set
- Add `dialect="any"` mode (union of all mergers) for maximum creativity
- `Phyme(dialect="western")` constructor param

**Phase 3: IPA internal representation**
- Add ARPABET→IPA converter (handle AH0→ə, ER0→ɚ)
- Add `ipa-dict` as alternate/supplementary data source
- Build vowel distance metric using articulatory features (height × backness × roundness)
- Use distance for continuous scoring instead of discrete levels
- Add `phonemizer`/eSpeak G2P fallback for OOV words
- Keep ARPABET as accepted input format for backward compatibility

**Phase 4: Polish**
- Multi-pronunciation support (CMU already has these, e.g., "READ(1)" vs "READ(2)")
- Optional phone handling (dropped R's, reduced syllables)
- Cross-diphthong matching (AY↔AW via shared onset)
- Performance profiling (search-time expansion could blow up at high squishiness)
- Modern packaging (pyproject.toml, proper CI)
- Updated README with the new API

##### What's Novel

No existing open-source rhyme tool does any of:
- Diphthong component matching with configurable squishiness
- Dialect-aware rhyme finding
- Continuous vowel distance scoring
- Meta vowel decomposition

Phyme would be the first to treat these as first-class features. The combination of songwriting focus + phonological rigor + dialect awareness is a genuinely new thing.

---

## Open Questions
- Should phyme support multiple pronunciations per word (CMU already has these, currently ignored)?
- How to handle words not in any dictionary? (G2P models?)
- Should dialect be a runtime parameter or a build-time data choice?
- How does songwriting rhyme differ from "strict" rhyme? (Already partially answered by existing rhyme types)
- Performance: current trie works well, but adding fuzzy vowel matching could blow up search space
