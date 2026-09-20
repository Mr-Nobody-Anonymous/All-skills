---
name: phonetics
description: "The physical properties of speech sounds: articulatory, acoustic, and auditory phonetics, IPA transcription"
category: linguistics
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/linguistics/phonetics/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Phonetics

## Scope
Phonetics studies the physical properties of speech sounds — how they are produced (articulatory), transmitted (acoustic), and perceived (auditory). This skill covers transcription, classification, and analysis of speech sounds.

## Articulatory Phonetics

### Consonant Classification
Every consonant is described by three parameters:

| Parameter | Options |
|-----------|---------|
| **Voicing** | Voiced (vocal folds vibrate) / Voiceless |
| **Place of articulation** | Bilabial, labiodental, dental, alveolar, postalveolar, retroflex, palatal, velar, uvular, pharyngeal, glottal |
| **Manner of articulation** | Plosive (stop), nasal, trill, tap/flap, fricative, lateral fricative, approximant, lateral approximant |

**Examples (IPA)**:
- [p] voiceless bilabial plosive (English "pin")
- [z] voiced alveolar fricative (English "zoo")
- [ʃ] voiceless postalveolar fricative (English "ship")
- [ŋ] voiced velar nasal (English "sing")

### Vowel Classification
- **Height**: Close (high) → close-mid → open-mid → open (low)
- **Backness**: Front → central → back
- **Rounding**: Rounded / unrounded
- **Vowel quadrilateral**: Standard IPA chart plotting height × backness

**Cardinal vowels**: [i] (close front unrounded), [u] (close back rounded), [a] (open front unrounded), [ɑ] (open back unrounded)

### Suprasegmentals
- **Stress**: Primary [ˈ], secondary [ˌ]
- **Tone**: Level (˥˦˧˨˩) or contour (rising, falling)
- **Length**: Long [ː], half-long [ˑ]
- **Intonation**: Pitch patterns over phrases/sentences

## Acoustic Phonetics
- **Fundamental frequency (F0)**: Perceived as pitch; ~120 Hz (male), ~220 Hz (female)
- **Formants**: Resonant frequencies of the vocal tract
  - F1 inversely correlates with vowel height
  - F2 correlates with vowel frontness
- **Voice Onset Time (VOT)**: Time between stop release and voicing onset
  - Negative VOT: pre-voiced (French /b/)
  - Short positive: unaspirated (English /b/)
  - Long positive: aspirated (English /p/)
- **Spectrogram**: Time × frequency × amplitude visualization of speech

## Auditory Phonetics
- **Frequency perception**: Logarithmic (mel scale, Bark scale)
- **Categorical perception**: Sharp boundaries between phoneme categories
- **Coarticulation**: Sounds influence neighboring sounds in connected speech

## Transcription Systems
- **Broad transcription /.../ **: Phonemic, language-specific contrasts only
- **Narrow transcription [...]**: Phonetic detail, allophonic variation included
- **IPA (International Phonetic Alphabet)**: Universal system; current version: 2020 revision

## Computational Tools
- **Praat**: Acoustic analysis, spectrograms, formant tracking, pitch extraction
- **ELAN**: Time-aligned transcription of multimedia
- **Montreal Forced Aligner**: Automatic phone-level alignment
- **Python**: `parselmouth` (Praat interface), `librosa` (audio analysis)

## Standards & References
- International Phonetic Association — *Handbook of the IPA*
- Ladefoged & Johnson — *A Course in Phonetics*
- Ladefoged & Maddieson — *The Sounds of the World's Languages*
