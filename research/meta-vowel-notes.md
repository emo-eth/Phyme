# Meta Vowel Research Notes

## 1. Complete ARPABET Diphthong Decomposition Table

### The Five Pure Vowels (Monophthong Anchors)

These are the "cardinal" vowels that map cleanly to traditional English vowel letters:

| Pure Vowel | ARPABET | IPA | Example | Traditional Letter |
|------------|---------|-----|---------|-------------------|
| Pure.A | AA | ɑ | "spa", "hot" | A (broad) |
| Pure.E | EY | eɪ | "day", "bait" | E (long) |
| Pure.I | IY | i | "free", "beat" | I (long) |
| Pure.O | OW | oʊ | "go", "boat" | O (long) |
| Pure.U | UW | u | "blue", "boot" | U (long) |

Note: EY and OW are themselves technically narrow diphthongs (eɪ and oʊ), but in General American English they're perceived as "single" vowels. This is important — the line between monophthong and diphthong is blurry in English.

### Full Diphthong Decomposition

| ARPABET | IPA | Example | Onset | Offglide | Pure Components | Notes |
|---------|-----|---------|-------|----------|-----------------|-------|
| **AY** | aɪ | "time", "sky" | AA (ɑ) | IY (i) | [Pure.A, Pure.I] | Wide diphthong. The most common "squishy rhyme" candidate. |
| **OY** | ɔɪ | "boy", "coin" | AO/OW (ɔ) | IY (i) | [Pure.O, Pure.I] | Onset is technically AO but perceptually close to OW. |
| **AW** | aʊ | "how", "crown" | AA (ɑ) | UW (u) | [Pure.A, Pure.U] | Mirror of AY — same onset, different offglide. |
| **EY** | eɪ | "day", "bait" | EH (ɛ) | IY (i) | [Pure.E, Pure.I] | Narrow diphthong, often perceived as monophthong. |
| **OW** | oʊ | "go", "boat" | AO/AA (o) | UW (u) | [Pure.O, Pure.U] | Narrow diphthong, often perceived as monophthong. |

### Monophthong Equivalence Classes

Each ARPABET monophthong can be mapped to the pure vowel(s) it's closest to:

| ARPABET | IPA | Example | Nearest Pure | Alt Pure | Notes |
|---------|-----|---------|-------------|----------|-------|
| **AA** | ɑ | "spa", "dot" | Pure.A | — | The canonical A |
| **AE** | æ | "bat", "dash" | Pure.A | Pure.E | Between A and E; "bat" sounds A-ish |
| **AH** | ʌ | "but", "love" | Pure.A | — | Reduced/central; unstressed AH0 → schwa |
| **AO** | ɔ | "caught", "tall" | Pure.A | Pure.O | Cot-caught merger makes this ≈ AA for many speakers |
| **EH** | ɛ | "bet", "gem" | Pure.E | — | Open-mid front; the onset of EY |
| **IH** | ɪ | "bit", "hill" | Pure.I | — | Near-close; the offglide target of AY |
| **UH** | ʊ | "book", "hook" | Pure.U | Pure.O | Near-close back; the offglide target of AW |
| **ER** | ɝ | "bird", "earth" | Pure.A? | — | R-colored; closest to central schwa. Wildcard. |

### Diphthong-Monophthong Match Matrix

This is the key table for meta vowel matching. A ✓ means the diphthong should match the monophthong at some squishiness level.

| | AA | AE | AH | AO | EH | IH | IY | UH | UW | OW | EY | ER |
|------|----|----|----|----|----|----|----|----|----|----|----|----|
| **AY** | ✓✓ | ✓ | ✓ | . | . | ✓ | ✓✓ | . | . | . | . | . |
| **OY** | . | . | . | ✓ | . | ✓ | ✓✓ | . | . | ✓✓ | . | . |
| **AW** | ✓✓ | ✓ | ✓ | . | . | . | . | ✓ | ✓✓ | . | . | . |
| **EY** | . | . | . | . | ✓✓ | ✓ | ✓✓ | . | . | . | — | . |
| **OW** | . | . | . | ✓ | . | . | . | ✓ | ✓✓ | — | . | . |

✓✓ = direct component match (onset or offglide)  
✓ = close neighbor within same pure vowel class  
— = self  
. = no match

### Songwriter's Intuition Translation

The table above is phonologically "correct" but what matters is what **sounds good** in a song. Real examples:

- **"time" (AY) ↔ "spa" (AA)**: The "ahh" onset of AY. Works well when the rhyme-bearing syllable is stressed and followed by similar consonant frames. Eminem does this constantly.
- **"time" (AY) ↔ "free" (IY)**: The "ee" offglide. Works especially well in melismatic singing where the vowel glides into the offglide.
- **"boy" (OY) ↔ "go" (OW)**: The "oh" onset. Common in pop/rock.
- **"how" (AW) ↔ "time" (AY)**: Both share the AA onset — "ahh-oo" vs "ahh-ee". This is why they feel related even though they're different diphthongs.
- **"day" (EY) ↔ "free" (IY)**: The "ee" offglide. Very common in singing.

The key insight: **onset matching feels stronger than offglide matching** in stressed, final position, because that's where the vowel spends most of its duration. Offglide matching is stronger in unstressed or medial positions, and in singing where vowels are held long enough for the glide to be prominent.

---

## 2. Analysis of Existing phone-classes Code

### What's Working

1. **Phone class hierarchy**: Clean inheritance chain `Phone → MetaPhone → MetaVowel/MetaShortVowel`. The `is_vowel`, `is_consonant`, `is_voiced` properties are correctly overridden at each level.

2. **MetaPhone equality**: The `__eq__` override is clever — a MetaPhone matches ANY of its replacement phones. This means `MetaPhone("TH", "DH") == Phone("DH")` returns True. This is the mechanism that enables fuzzy matching.

3. **MetaShortVowel for semivowels**: Y→MetaShortVowel(Y, IY0) and W→MetaShortVowel(W, UW0) in `phone_mapper`. These correctly handle the semivowel-as-vowel ambiguity without inflating syllable count (`is_vowel=False`, `is_consonant=False`).

4. **Trie _replace_phones**: The `RhymeTrieNode._replace_phones` method already handles MetaPhones correctly — when it encounters a MetaPhone during search, it expands to search each replacement phone. This is the core fuzzy-search mechanism.

5. **Permutation system**: The existing `Permutation` enum + `PermutedPhone` system handles consonant fuzzing (family, partner, additive, subtractive). Well-designed and extensible.

### What's Incomplete

1. **No diphthong MetaVowels**: `phone_mapper` only handles Y and W. Diphthong vowels (AY, OY, AW, etc.) are still mapped to plain `Phone` objects. This means the entire meta vowel concept for diphthongs is unactivated.

2. **No decomposition data structure**: The analysis in `mappings.json` is hand-written notes, not code. There's no `DIPHTHONG_COMPONENTS` dict or similar that maps AY → [AA, IY].

3. **1-to-many expansion problem**: The commented-out `CompoundMetaPhone` shows the developer hit the fundamental issue: AY is ONE phone in ARPABET but decomposes into TWO vowel targets. The current trie structure assumes 1:1 phone-to-node mapping. A MetaVowel can match _different_ phones but can't _expand_ into multiple phones.

4. **No squishiness parameter**: All matching is binary (exact or not). There's no way to request "only onset matches" vs "any component matches" vs "same pure vowel class".

5. **No stress-aware vowel flexibility**: Unstressed vowels should be more permissive (AH0 ≈ schwa ≈ anything), but the current system treats all stress levels identically for vowel identity.

6. **Hashing inconsistency**: `MetaPhone.__hash__` uses `super().__hash__()` which hashes based on `self.phone` (the primary phone). This means `MetaPhone("AY", Phone("AA"), Phone("IY"))` hashes to the same bucket as `Phone("AY")`, NOT `Phone("AA")`. For trie insertion this is fine (the MetaVowel inserts under the AY slot). But for trie search, the lookup `self.children.get(phones[0])` uses hash+eq. If we're searching for Phone("AA") and a child is keyed as MetaVowel("AY", ...), the dict lookup will fail because Phone("AA").__hash__ ≠ MetaVowel("AY").__hash__ even though Phone("AA") == MetaVowel("AY") returns True (via MetaPhone.__eq__). **This is a bug.** Dict lookup requires that `a == b` implies `hash(a) == hash(b)`. The current MetaPhone breaks this contract.

7. **No bidirectional matching**: Currently, if "time" (AY) is inserted as a MetaVowel, searching for "time" will expand to match AA and IY children. But searching for "spa" (AA) won't find AY children unless AA is ALSO wrapped as a MetaVowel containing AY. The matching needs to work both directions.

### Existing Infrastructure Gaps

- No way to score or rank fuzzy matches by quality
- No dialect parameter to control which vowel mergers are active
- No way to handle the cot-caught merger (AA ≈ AO for many speakers)
- The `get_by_vowel` method is a start but doesn't integrate meta vowels

---

## 3. Proposed Trie Modifications

### Option A: Search-Time Expansion (Recommended)

Keep the trie structure as-is. Modify search to consult a vowel equivalence table:

```python
# Vowel equivalence table
VOWEL_META_CLASSES = {
    # For each vowel, what other vowels it can match at each squishiness level
    "AY1": {
        1: {"AY1"},                           # exact only
        2: {"AY1", "AA1"},                    # onset match
        3: {"AY1", "AA1", "IY1"},             # onset + offglide
        4: {"AY1", "AA1", "IY1", "AH1", "AE1", "IH1"},  # full pure class
    },
    "AA1": {
        1: {"AA1"},
        2: {"AA1", "AY1", "AW1"},            # any diphthong with AA onset
        3: {"AA1", "AY1", "AW1", "AH1", "AE1", "AO1"},  # Pure.A class
    },
    # ... etc
}
```

At search time, instead of `self.children.get(phones[0])`, iterate over the equivalence set and merge results:

```python
def search_meta(self, phones, squishiness=1):
    if not phones:
        yield self
        return
    target_phone = phones[0]
    equivalents = get_equivalents(target_phone, squishiness)
    for equiv in equivalents:
        child = self.children.get(equiv)
        if child:
            yield from child.search_meta(phones[1:], squishiness)
```

**Pros**: 
- No change to trie structure or insert logic
- Squishiness is a search-time parameter
- No storage overhead
- Backward compatible

**Cons**:
- Search is slower (branching factor increases with squishiness)
- Stress matching must be handled (AY1 child won't match if we search for AA1 — need stress-agnostic lookup)

### Option B: Equivalence-Class Keyed Trie

Replace the `children` dict key type from `Phone` to a normalized equivalence class. All phones in the same class share a trie branch.

**Pros**: Fast lookup
**Cons**: Loses the ability to distinguish exact vs fuzzy matches. All matches at insert-time squishiness level become equivalent.

### Option C: Multi-Trie

Maintain separate tries at different squishiness levels. Level 0 = exact. Level 1 = insert with MetaVowels. Level 2 = insert with decomposed diphthongs.

**Pros**: Clean separation, fast lookup at each level
**Cons**: Memory multiplication (2-4x), insert time increases

### Recommendation: Option A with Stress Normalization

Option A is the best fit for Phyme's architecture because:
1. The `_replace_phones` mechanism already does search-time expansion for MetaPhones
2. Adding a squishiness parameter is natural — it controls how many equivalents to expand
3. No breaking changes to the existing trie or insert path
4. Performance is manageable because the branching factor is small (at most ~6 equivalent vowels)

The key modifications needed:
1. Build a `VowelEquivalence` class that maps `(phone, squishiness_level) → set of equivalent phones`
2. Modify `search_permutations` to accept a `squishiness` parameter
3. Handle stress normalization: when looking up equivalents, strip stress digits, then re-apply to check children with matching stress (or any stress at high squishiness)
4. Add new public methods: `get_meta_rhymes(word, squishiness=2)`

---

## 4. Squishiness Parameter Design

### Proposed Levels

```
Level 0: EXACT
  Only exact phone matches. "time" (AY1) matches only AY1.
  This is current behavior.

Level 1: VOWEL NEIGHBORS  
  Monophthongs match close neighbors within the same quality region.
  IH ↔ IY (bit ↔ beat)
  UH ↔ UW (book ↔ boot)  
  AH ↔ AA (but ↔ bot)
  EH ↔ EY-onset (bet ↔ bait-onset)
  AO ↔ AA (caught ↔ cot — cot-caught merger)

Level 2: DIPHTHONG ONSET
  Diphthongs match their onset monophthong.
  AY matches AA (time ↔ spa) — the "ahh" connection
  OY matches OW/AO (boy ↔ go) — the "oh" connection
  AW matches AA (how ↔ spa) — the "ahh" connection
  AND: monophthongs match diphthongs containing them as onset
  AA matches AY, AW (spa ↔ time, spa ↔ how)

Level 3: DIPHTHONG FULL
  Diphthongs match onset OR offglide.
  AY matches AA or IY (time ↔ spa, time ↔ free)
  OY matches OW or IY (boy ↔ go, boy ↔ free)  
  AW matches AA or UW (how ↔ spa, how ↔ blue)
  AND cross-diphthong via shared components:
  AY ↔ AW (shared AA onset)
  AY ↔ EY (shared IY offglide)
  AY ↔ OY (shared IY offglide)

Level 4: PURE VOWEL CLASS
  Any vowels sharing a Pure Vowel class match.
  Pure.A class: AA, AH, AE, AO, AY-onset, AW-onset, OY-onset(?)
  Pure.I class: IY, IH, AY-offglide, OY-offglide, EY-offglide
  Pure.U class: UW, UH, AW-offglide, OW-offglide
  Pure.E class: EY-onset, EH
  Pure.O class: OW-onset, AO, OY-onset
```

### API Surface

```python
from phyme import Phyme

ph = Phyme()

# Exact (current behavior, backward compatible)
ph.get_perfect_rhymes("time")  
# → {1: ["dime", "rhyme", "crime", ...]}

# Meta vowel rhymes (new)
ph.get_meta_rhymes("time", squishiness=2)
# → {1: ["dime", "crime", ..., "spa", "bra", ...]}  (onset matches)

ph.get_meta_rhymes("time", squishiness=3)
# → {1: ["dime", "crime", ..., "spa", "bra", ..., "free", "see", ...]}  (full component)

# Also works in reverse
ph.get_meta_rhymes("spa", squishiness=2)
# → {1: ["bra", "ha", ..., "time", "rhyme", ...]}  (finds diphthongs with AA onset)
```

### Scoring / Ranking

Within meta rhyme results, matches should be ranked by quality:
1. Exact match (squishiness=0 would have found it)
2. Vowel neighbor match
3. Onset component match  
4. Offglide component match
5. Pure class match

This ranking should influence the `sort_words` output so that better matches appear first, regardless of word frequency.

### Stress Interaction

Squishiness should also influence stress matching:
- At level 0-2: only match phones with the same stress digit
- At level 3+: match any stressed (1 or 2) with any stressed, and unstressed (0) is more permissive
- Unstressed positions at level 2+: AH0 matches any vowel (schwa reduction)

---

## 5. Vowel Reduction & Unstressed Permissiveness

### The Schwa Problem

In casual American English, virtually all unstressed vowels reduce toward schwa [ə], which ARPABET represents as AH0 (or sometimes IH0). Examples:

- "comfortable" → the second vowel is nominally AH0 but could be IH0 or EH0
- "chocolate" → first vowel is AA1 (stressed), second collapses to nearly nothing
- "banana" → the unstressed A's are schwa, not AA

### Proposed Handling

```python
SCHWA_EQUIVALENTS = {"AH0", "IH0", "AX0"}  # AX not in CMU but conceptually

def is_schwa_position(phone, stress):
    """Unstressed vowels are schwa-adjacent"""
    return stress == "0" and phone.phone[:-1] in {"AH", "IH", "EH", "AE"}
```

At squishiness ≥ 2, unstressed vowel positions should match any unstressed vowel. This dramatically improves multi-syllable rhyme finding without sacrificing stressed-vowel precision.

### Implementation

The cleanest way: in the vowel equivalence table, when building the equivalent set for an unstressed vowel, include ALL unstressed vowels at squishiness ≥ 2. This doesn't require trie changes — just a wider expansion during search.

---

## 6. Multi-Phone Substitution Analysis

### The Core Problem

ARPABET treats AY as **one phone**. IPA treats it as **two targets** (/aɪ/). If we decompose AY into [AA, IY] in the trie:

- "time" goes from 3 phones `[T, AY1, M]` to 4 phones `[T, AA1, IY0, M]`
- The trie depth changes
- Syllable count stays the same (1), but the phone count doesn't match
- Searching for words with AY won't find the decomposed form, and vice versa

### Why NOT to Decompose

1. **Structural mismatch**: Every existing word in the trie uses the ARPABET convention. Decomposing some words but not others creates inconsistency.
2. **CMU dict compatibility**: The CMU dictionary uses single-symbol diphthongs. Fighting the data format creates maintenance burden.
3. **Syllable count breaks**: The syllable extraction logic counts vowels to determine syllables. Decomposing AY into AA+IY would count as two syllables.
4. **Search complexity**: You'd need to search both the decomposed and non-decomposed forms.

### The MetaVowel Alternative (Recommended)

Don't decompose. Instead, use the existing MetaVowel mechanism to declare: "AY is one phone, but it's equivalent to AA and IY for matching purposes."

```python
# At search time:
# Searching for "time" [T, AY1, M] reversed → [M, AY1, T]
# At the AY1 position, with squishiness=3, also search [M, AA1, T] and [M, IY1, T]

# Searching for "spa" [S, P, AA1] reversed → [AA1, P, S]  
# At the AA1 position, with squishiness=2, also search [AY1, P, S]
```

This keeps AY as one phone in the trie but allows it to match other phones during search. The key is making the equivalence bidirectional:
- AY → can match AA, IY (when searching for a word with AY)
- AA → can match AY, AW (when searching for a word with AA)

### The Commented-Out CompoundMetaPhone

The `CompoundMetaPhone` in rhymeUtils.py was heading toward actual decomposition (replacing one phone with a list of phones). This is the wrong direction for the reasons above. The right approach is the MetaVowel expansion at search time — a phone matches a SET of alternative single phones, not a SEQUENCE of phones.

---

## 7. Real-World Rhyme Examples (Songwriter's Ear)

### Diphthong-Monophthong Rhymes That Sound Good

**AY ↔ AA (onset)**
- time / calm / palm / drama / spa
- mind / wand / fond / beyond
- "I've got time for the drama" — the /ɑ/ onset connects

**AY ↔ IY (offglide)**  
- sky / free / sea / degree / debris
- "the sky sets me free" — the /i/ offglide lingers in singing

**AW ↔ AA (onset)**
- how / spa / raw / draw
- down / dawn / gone / swan
- "how far is the dawn" — the /ɑ/ connection

**OY ↔ OW (onset)**
- boy / go / flow / show / grow
- coin / bone / tone / zone
- "the boy lets it flow" — the /o/ connection

**AY ↔ AW (shared onset)**
- time / down / how / now / crown
- This is diphthong-to-diphthong via shared AA onset
- "time's running down" — both start with /ɑ/ then diverge

**EY ↔ IY (offglide)**
- day / free / see / agree / key
- "one day you'll see" — the /i/ offglide of EY matches IY

### Diphthong-Monophthong Rhymes That DON'T Sound Good

- time (AY) / book (UH) — no component overlap
- boy (OY) / bat (AE) — onset and offglide are both far
- how (AW) / bet (EH) — no connection

### What Makes a Squishy Rhyme Work in Song

1. **Consonant frame similarity**: The surrounding consonants matter as much as the vowel. "time/crime" is perfect; "time/calm" works because the final consonant frame is similar enough (nasal M vs. open-M).
2. **Rhythmic position**: Squishy rhymes work better on strong beats where the vowel gets held.
3. **Melodic support**: If the melody emphasizes the shared component (onset or offglide), the listener's ear latches onto the similarity.
4. **Expectation**: Once a rhyme scheme is established, listeners are primed to hear connections. The first pair sets the "squishiness tolerance" for the verse.
5. **Speed**: In fast rap, the consonant skeleton matters more than exact vowels. At conversational speed, vowel precision matters more.
