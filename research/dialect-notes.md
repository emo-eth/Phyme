# Dialect-Aware Rhyme Matching: Technical Notes

## 1. CMU ARPABET Vowel Inventory (Reference)

Phyme uses CMU Pronouncing Dictionary's ARPABET notation. The 15 base vowel phonemes (each with stress variants 0/1/2):

| ARPABET | IPA   | Lexical Set | Example Words |
|---------|-------|-------------|---------------|
| AA      | ɑ     | LOT/PALM    | dot, hop, father |
| AE      | æ     | TRAP/BATH   | dash, cat, man |
| AH      | ʌ     | STRUT       | love, one, dust |
| AO      | ɔ     | THOUGHT     | tall, caught, cork |
| AW      | aʊ    | MOUTH       | crown, bound, scout |
| AY      | aɪ    | PRICE       | crime, hide, guys |
| EH      | ɛ     | DRESS       | gem, hem, bed |
| ER      | ɝ     | NURSE       | earth, bird, purr |
| EY      | eɪ    | FACE        | baked, fame, lei |
| IH      | ɪ     | KIT         | hill, tick, swing |
| IY      | iː    | FLEECE      | fleet, gene, east |
| OW      | oʊ    | GOAT        | show, folk, dough |
| OY      | ɔɪ    | CHOICE      | boy, coin, noise |
| UH      | ʊ     | FOOT        | hook, book, pull |
| UW      | uː    | GOOSE       | drool, queue, chew |

## 2. Major American English Mergers Affecting Rhyme

### 2.1 Cot-Caught Merger (AA ↔ AO)

**The single most impactful merger for rhyme matching.**

- **What**: LOT (AA /ɑ/) and THOUGHT (AO /ɔ/) become identical
- **Where**: Western US (including California), Canada, Pittsburgh, Upper Midwest, spreading nationwide
- **Prevalence**: ~40% of Americans as of the 1990s ANAE survey; growing rapidly, especially among younger speakers
- **CMU mapping**: `AA` ↔ `AO` become interchangeable
- **Rhyme impact**: HIGH — cot/caught, stock/stalk, don/dawn, nod/gnawed, rot/wrought all become perfect rhymes
- **Example word pairs now rhyming**: 
  - cot/caught, bot/bought, tot/taught
  - stock/stalk, hock/hawk, cock/caulk
  - don/dawn, pond/pawned, collar/caller
  - knotty/naughty, hottie/haughty

**Implementation note**: This is a simple unconditional merger. In a merged dialect, replace all AO with AA (or vice versa) before rhyme comparison.

### 2.2 Pin-Pen Merger (IH ↔ EH before nasals)

- **What**: KIT (IH /ɪ/) and DRESS (EH /ɛ/) merge before nasal consonants (M, N, NG)
- **Where**: Southern US (very widespread), parts of Midwest, Bakersfield CA
- **Prevalence**: Near-universal in the South; the most widespread Southern feature
- **CMU mapping**: `IH` ↔ `EH` when followed by `M`, `N`, or `NG`
- **Rhyme impact**: MEDIUM — pin/pen, him/hem, tin/ten, kin/Ken, Jim/gem, since/sense
- **CRITICAL**: This is **conditional** — only applies before nasals, NOT in all positions

**Implementation note**: This requires checking the following consonant. A merger rule needs: `{phones: [IH, EH], condition: "before_nasal"}` where nasals = {M, N, NG}.

### 2.3 Mary-Marry-Merry Merger (EH ↔ AE ↔ EY before /r/)

- **What**: Three pre-/r/ vowels merge: SQUARE (EH + R), TRAP+R (AE + R), FACE+R (EY + R)
- **Where**: Most of the US and Canada (except NYC, Philadelphia, some New England, conservative Southern)
- **Prevalence**: ~55-65% of Americans have the full three-way merger
- **CMU mapping**: `EH` ↔ `AE` ↔ `EY` when followed by `R` (same syllable or cross-syllable)
- **Rhyme impact**: MEDIUM — Mary/marry/merry, fairy/ferry/carry (already), hairy/Harry/very
- **Partial mergers common**: marry-merry (AE-EH before R) merges first; Mary (EY+R) last to merge

**Implementation note**: Conditional on following R. The merger means `AE_R`, `EH_R`, and `EY_R` sequences are all equivalent. Some speakers have partial mergers (just marry=merry but not =Mary).

### 2.4 Northern Cities Vowel Shift (NCVS)

A **chain shift** affecting 6 vowels, found in Great Lakes cities (Chicago, Detroit, Cleveland, Buffalo, Rochester, Syracuse, Milwaukee). Does NOT produce mergers but shifts vowel qualities:

| Stage | Movement | ARPABET | Direction |
|-------|----------|---------|-----------|
| 1 | TRAP raises | AE → toward EH/EY | ↑ (fronted + raised) |
| 2 | LOT fronts | AA → toward AE | → (fronted) |
| 3 | THOUGHT lowers | AO → toward AA | ↓ (lowered) |
| 4 | DRESS backs | EH → toward AH | ← (backed) |
| 5 | KIT centralizes | IH → toward schwa | (centralized) |
| 6 | STRUT backs | AH → toward AO | ← (backed) |

- **Rhyme impact**: MODERATE — The chain nature means vowels shift but don't merge. However, perceptual near-mergers occur:
  - TRAP (AE) sounds close to DRESS (EH) or FACE (EY)
  - LOT (AA) sounds close to TRAP (AE)  
  - DRESS (EH) sounds close to STRUT (AH)
  - STRUT (AH) sounds close to THOUGHT (AO)
  
- **For rhyming purposes**: These are NOT mergers — NCVS speakers maintain all contrasts. But for "squishy" rhyming, adjacent pairs could be treated as near-rhymes with reduced distance.

**Implementation note**: Model as "softened distances" between adjacent pairs rather than full mergers. The NCVS notably **resists** the cot-caught merger.

### 2.5 Southern Vowel Shift (SVS)

A complex chain shift with 3 stages, found throughout the South:

| Stage | Movement | ARPABET | Effect |
|-------|----------|---------|--------|
| 1 | PRICE monophthongizes | AY → AA-like [aː] | Diphthong → monophthong |
| 2a | FACE lowers | EY → toward EH | ↓ |
| 2b | DRESS raises | EH → toward EY | ↑ |
| 3a | FLEECE lowers start | IY → [ɪi] | Diphthongizes differently |
| 3b | KIT raises | IH → toward IY | ↑ |

Plus:
- MOUTH (AW) fronts → toward [æʊ]
- THOUGHT (AO) lowers → toward [ɑɒ]

**Key rhyme impacts:**
1. **AY monophthongization**: ride/rod, time/Tom can become near-rhymes (AY ≈ AA). This is the BIG one.
   - Especially before voiced consonants and word-finally
   - Before voiceless consonants, glide often retained (ride [aːd] but right [aɪt])
2. **EY/EH near-merger**: name/nem, day/dead approach each other
3. **IH/IY near-merger**: hit/heat approach each other (Stage 3 only, most advanced speakers)

**Implementation note**: AY → AA (conditional: primarily before voiced consonants and word-finally) is the most impactful. Model EY↔EH and IH↔IY as soft near-mergers.

### 2.6 California Vowel Shift

Part of the broader Western/Low-Back-Merger Shift:

- **Cot-caught merger**: Complete (AA = AO) — see §2.1
- **GOOSE (UW) and GOAT (OW) fronting**: UW/OW move toward central position. Doesn't affect rhyme matching (still same phoneme)
- **TRAP (AE) retraction**: AE moves back and lower. Approaches AA territory. Does NOT merge.
- **DRESS (EH) lowering**: EH moves lower. Does NOT merge with AE.
- **KIT (IH) lowering/backing**: IH moves toward schwa-territory.
- **Front vowels raised before /ŋ/**: AE → EY and IH → IY before NG (ring sounds like "reeng", rang sounds like "raing")

**Key rhyme impacts:**
1. Cot-caught merger (dominant feature)
2. Pre-velar nasal raising: `AE` → `EY` before `NG`, `IH` → `IY` before `NG`
   - ring/reen, bang/bane approach each other

**Implementation note**: The cot-caught merger is the only true merger. The vowel shift movements are quality changes within phonemes, not mergers. The pre-NG raising is an interesting conditional shift.

### 2.7 Other Notable Mergers

#### Hurry-Furry Merger
- **What**: AH before intervocalic R merges with ER
- **Where**: Most of North America
- **CMU**: `AH` + intervocalic `R` ↔ `ER`
- **Impact**: LOW for end-rhyme (affects mid-word syllables more)

#### GOOSE-fronting / FOOT-GOOSE relationships
- **What**: UW and UH move forward
- **Where**: Most American dialects
- **Impact**: LOW — the phonemes don't merge, just shift position

#### Fill-Feel Merger
- **What**: IH and IY merge before L
- **Where**: Southern US, parts of Western US
- **CMU**: `IH` ↔ `IY` before `L`
- **Impact**: LOW-MEDIUM — fill/feel, mill/meal, pill/peel, will/we'll

#### Full-Fool Merger
- **What**: UH and UW merge before L  
- **Where**: Similar distribution to fill-feel
- **CMU**: `UH` ↔ `UW` before `L`
- **Impact**: LOW-MEDIUM — full/fool, pull/pool, bull/bool

#### Curt-Caught Merger (before /r/)
- Various pre-/r/ mergers reduce vowel contrasts
- Most Americans merge many vowel distinctions before /r/

## 3. Proposed Dialect Profiles

Based on the research, I propose **5 dialect profiles** that meaningfully cover the space of American English rhyme variation:

### Profile 1: "General American / Western" (baseline expanding)
The most common modern American English, spreading nationwide via media.
```json
{
  "id": "general_western",
  "name": "General American / Western",
  "description": "Western US, spreading. Cot-caught merged, Mary-marry-merry merged.",
  "region": "Western US, Upper Midwest (younger speakers), spreading nationwide",
  "mergers": [
    {
      "id": "cot_caught",
      "phones": ["AA", "AO"],
      "condition": null,
      "type": "unconditional",
      "description": "LOT-THOUGHT merger: cot=caught, stock=stalk"
    },
    {
      "id": "mary_marry_merry",
      "phones": ["AE", "EH", "EY"],
      "condition": {"following": ["R"]},
      "type": "conditional",
      "description": "Pre-R merger: Mary=marry=merry"
    }
  ]
}
```

### Profile 2: "Southern"
Traditional Southern American English with key vowel shifts.
```json
{
  "id": "southern",
  "name": "Southern American",
  "description": "Southern US. Pin-pen merged, AY monophthongized, no cot-caught.",
  "region": "Southern US (excluding FL, urban TX, Atlanta)",
  "mergers": [
    {
      "id": "pin_pen",
      "phones": ["IH", "EH"],
      "condition": {"following": ["M", "N", "NG"]},
      "type": "conditional",
      "description": "Pin-pen merger before nasals"
    },
    {
      "id": "ay_monophthong",
      "phones": ["AY"],
      "maps_to": "AA",
      "condition": {"following": ["voiced", "word_boundary"]},
      "type": "reduction",
      "description": "PRICE monophthongization: ride≈rod"
    },
    {
      "id": "mary_marry_merry",
      "phones": ["AE", "EH", "EY"],
      "condition": {"following": ["R"]},
      "type": "conditional",
      "description": "Pre-R merger (partial in conservative speakers)"
    },
    {
      "id": "fill_feel",
      "phones": ["IH", "IY"],
      "condition": {"following": ["L"]},
      "type": "conditional",
      "description": "Fill-feel merger before /l/"
    },
    {
      "id": "full_fool",
      "phones": ["UH", "UW"],
      "condition": {"following": ["L"]},
      "type": "conditional",
      "description": "Full-fool merger before /l/"
    }
  ],
  "near_mergers": [
    {
      "id": "svs_face_dress",
      "phones": ["EY", "EH"],
      "type": "chain_shift_adjacent",
      "distance_modifier": 0.5,
      "description": "SVS Stage 2: FACE and DRESS approach each other"
    }
  ]
}
```

### Profile 3: "Inland North / Great Lakes"
Northern Cities Vowel Shift territory.
```json
{
  "id": "inland_north",
  "name": "Inland North / Great Lakes",
  "description": "Great Lakes cities. NCVS active, resists cot-caught merger.",
  "region": "Chicago, Detroit, Cleveland, Buffalo, Rochester, Syracuse, Milwaukee",
  "mergers": [
    {
      "id": "mary_marry_merry",
      "phones": ["AE", "EH", "EY"],
      "condition": {"following": ["R"]},
      "type": "conditional",
      "description": "Pre-R merger"
    }
  ],
  "near_mergers": [
    {
      "id": "ncvs_trap_dress",
      "phones": ["AE", "EH"],
      "type": "chain_shift_adjacent",
      "distance_modifier": 0.5,
      "description": "NCVS: raised TRAP approaches DRESS"
    },
    {
      "id": "ncvs_lot_trap",
      "phones": ["AA", "AE"],
      "type": "chain_shift_adjacent",
      "distance_modifier": 0.5,
      "description": "NCVS: fronted LOT approaches TRAP"
    },
    {
      "id": "ncvs_dress_strut",
      "phones": ["EH", "AH"],
      "type": "chain_shift_adjacent",
      "distance_modifier": 0.5,
      "description": "NCVS: backed DRESS approaches STRUT"
    },
    {
      "id": "ncvs_strut_thought",
      "phones": ["AH", "AO"],
      "type": "chain_shift_adjacent",
      "distance_modifier": 0.5,
      "description": "NCVS: backed STRUT approaches THOUGHT"
    }
  ],
  "notes": "The NCVS does NOT produce true mergers — speakers maintain all contrasts. Near-mergers affect perception of rhyme quality."
}
```

### Profile 4: "Northeast Corridor" (NYC/Philly/Baltimore)
Distinctive for its resistance to many widespread mergers.
```json
{
  "id": "northeast",
  "name": "Northeast Corridor",
  "description": "NYC, Philadelphia, Baltimore. Most merger-resistant. Complex AE tensing.",
  "region": "NYC, Philadelphia, Baltimore, parts of NJ",
  "mergers": [],
  "anti_mergers": [
    "cot_caught",
    "mary_marry_merry"
  ],
  "notes": "This dialect maintains the MOST vowel contrasts of any major American dialect. Cot≠caught, Mary≠marry≠merry (or partial). For rhyme matching, this is the MOST conservative profile — fewest extra rhymes."
}
```

### Profile 5: "Midland / Transitional"
The middle ground, often considered the "default" broadcast American.
```json
{
  "id": "midland",
  "name": "Midland American",
  "description": "Transition zone. Partial cot-caught, Mary-marry-merry merged.",
  "region": "Central Ohio, Indiana, Kansas, Missouri, Oklahoma, much of PA",
  "mergers": [
    {
      "id": "mary_marry_merry",
      "phones": ["AE", "EH", "EY"],
      "condition": {"following": ["R"]},
      "type": "conditional",
      "description": "Pre-R merger"
    },
    {
      "id": "cot_caught_partial",
      "phones": ["AA", "AO"],
      "condition": null,
      "type": "unconditional",
      "confidence": 0.5,
      "description": "Cot-caught merger in transition — some speakers merged, some not"
    }
  ]
}
```

## 4. Proposed Schema for Dialect Profiles

```python
from dataclasses import dataclass, field
from typing import Optional, List, Set, Dict, Literal
from enum import Enum

class MergerType(Enum):
    UNCONDITIONAL = "unconditional"     # Always applies (e.g., cot-caught)
    CONDITIONAL = "conditional"          # Only in specific phonetic environments
    REDUCTION = "reduction"              # Diphthong → monophthong  
    CHAIN_SHIFT = "chain_shift_adjacent" # Near-merger from vowel shift

@dataclass
class PhoneticCondition:
    """Defines when a merger applies"""
    following: Optional[Set[str]] = None     # Following phone(s): {"M", "N", "NG"} or {"R"}
    preceding: Optional[Set[str]] = None     # Preceding phone(s)
    position: Optional[str] = None           # "word_final", "pre_voiceless", etc.
    following_voiced: Optional[bool] = None  # True = only before voiced consonants

@dataclass  
class Merger:
    """A phoneme merger or near-merger rule"""
    id: str
    phones: List[str]                        # ARPABET phones involved
    merger_type: MergerType
    condition: Optional[PhoneticCondition] = None
    maps_to: Optional[str] = None            # For reductions: what the phone becomes
    distance_modifier: float = 0.0           # 0.0 = full merger, 0.5 = half-distance
    description: str = ""

@dataclass
class DialectProfile:
    """A regional dialect's rhyme-affecting features"""
    id: str
    name: str
    description: str
    region: str
    mergers: List[Merger] = field(default_factory=list)
    near_mergers: List[Merger] = field(default_factory=list)

    def get_equivalent_phones(self, phone: str, context: Optional[dict] = None) -> Set[str]:
        """Given a phone and its context, return the set of phones it's equivalent to."""
        equivalents = {phone}
        for merger in self.mergers:
            if phone in merger.phones:
                if merger.condition is None or self._matches_condition(merger.condition, context):
                    if merger.maps_to:
                        equivalents.add(merger.maps_to)
                    else:
                        equivalents.update(merger.phones)
        return equivalents

    def _matches_condition(self, condition: PhoneticCondition, context: Optional[dict]) -> bool:
        """Check if phonetic context matches a merger condition."""
        if context is None:
            return False
        if condition.following and context.get("following"):
            if context["following"] not in condition.following:
                return False
        if condition.following_voiced is not None:
            if context.get("following_voiced") != condition.following_voiced:
                return False
        return True
```

## 5. Merger Impact Summary (sorted by rhyme impact)

| Rank | Merger | ARPABET | Impact | Prevalence | Conditional? |
|------|--------|---------|--------|------------|--------------|
| 1 | Cot-caught | AA ↔ AO | HIGH | ~50%+ & growing | No |
| 2 | AY monophthong (Southern) | AY → AA | HIGH | ~30% (South) | Yes (before voiced/final) |
| 3 | Pin-pen | IH ↔ EH | MEDIUM | ~30% (South) | Yes (before nasals) |
| 4 | Mary-marry-merry | AE ↔ EH ↔ EY | MEDIUM | ~60% | Yes (before R) |
| 5 | Fill-feel | IH ↔ IY | LOW-MED | ~25% (South/West) | Yes (before L) |
| 6 | Full-fool | UH ↔ UW | LOW-MED | ~25% | Yes (before L) |
| 7 | NCVS chain shifts | multiple | LOW | ~15% (declining) | Complex |
| 8 | SVS chain shifts | multiple | LOW | ~30% | Complex |

## 6. Existing Tools & Resources

### Databases
- **CMU Pronouncing Dictionary**: Current data source. Single "General American" pronunciation per word (sometimes 2-3 variants). Does NOT encode dialectal variation.
- **Atlas of North American English (ANAE)** (Labov, Ash, Boberg 2006): The authoritative survey. Maps isoglosses for all major sound changes. Not freely available as data (book + website).
- **DARE (Dictionary of American Regional English)**: Lexical focus, less phonological.
- **FAVE (Forced Alignment and Vowel Extraction)**: Tool from U. Penn for analyzing vowel formants. Could be used to *verify* dialect differences from speech data.

### Python Libraries
- **`panphon`** (David Mortensen): Maps IPA segments to articulatory feature vectors. Useful for computing phonological *distance* between segments. Could be used to quantify "how different" two vowels are across dialects.
- **`epitran`**: Grapheme-to-phoneme for many languages. Uses Flite for English. Produces single-dialect output only.
- **`g2p_en`**: English grapheme-to-phoneme. CMU-based. No dialect awareness.
- **`phonemizer`**: Wrapper around espeak-ng. Can produce IPA for different English "dialects" (en-us, en-gb, en-sc) but these are very coarse.
- **`eng_to_ipa`**: Simple CMU dictionary lookup. No dialect awareness.

### No existing tool models American dialect variation computationally at the phoneme level.
This is a gap in the tooling landscape. The closest approaches are:
1. Using multiple pronunciation dictionaries (e.g., CMU for GenAm, something else for Southern) — but alternative dicts don't exist in ARPABET
2. Rule-based transforms on CMU output — **this is what Phyme should do**
3. Using formant data from ANAE — requires acoustic analysis, not practical for a rhyming dictionary

## 7. Implementation Recommendations for Phyme

### Approach: Rule-Based Dialect Transforms

The most practical approach is:
1. **Keep CMU as the base** — it represents a "General American" baseline
2. **Define dialect profiles as transform rules** — each profile is a set of mergers/shifts applied on top of CMU
3. **At rhyme-comparison time**, apply the active dialect profile to both words being compared
4. **Allow "any dialect" mode** that uses the UNION of all mergers for maximum "squishiness"

### Integration with MetaPhone

The existing `MetaPhone` class is a natural fit:
- A `MetaPhone` already represents "this phone OR any of these replacement phones"
- A dialect profile can be used to *construct* MetaPhones at load time:
  - In "western" dialect: `MetaVowel(Phone("AA"), Phone("AO"))` — AA matches AO and vice versa
  - In "southern" dialect: `MetaVowel(Phone("IH"), Phone("EH"))` but only when followed by nasal

### Handling Conditional Mergers

The tricky part is conditional mergers (pin-pen, mary-marry-merry). Options:
1. **Context-aware MetaPhone**: Extend MetaPhone with a condition predicate
2. **Pre-process pronunciations**: Transform the pronunciation BEFORE building the trie, based on context
3. **Post-filter**: Find rhymes with unconditional matching, then filter based on phonetic context

Option 2 is probably cleanest: when loading words under "southern" profile, rewrite `P IH1 N` → `P IH1/EH1 N` (marking the IH as MetaVowel(IH, EH) because it's followed by N).

### Suggested API

```python
from phyme import Phyme

# Default: General American (CMU as-is)
ph = Phyme()

# Dialect-aware
ph = Phyme(dialect="western")          # cot-caught merged
ph = Phyme(dialect="southern")         # pin-pen merged, AY mono
ph = Phyme(dialect="any")              # maximum squish — union of all mergers
ph = Phyme(dialect=["cot_caught", "pin_pen"])  # cherry-pick individual mergers
```

### Priority Order for Implementation

1. **Cot-caught merger** (AA↔AO) — unconditional, highest impact, simplest to implement
2. **Mary-marry-merry** (AE↔EH↔EY before R) — conditional but common
3. **Pin-pen merger** (IH↔EH before nasals) — conditional, good test of the condition system
4. **AY monophthongization** (AY→AA before voiced) — reduction type, different from merger
5. **Fill-feel, full-fool** — more conditional mergers
6. **Chain shift near-mergers** — lowest priority, most complex
