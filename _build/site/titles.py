"""Title Case for tour and product names: every word capitalised, except short joining words in the middle.
Hyphenated words are capitalised on both sides (Kids-Friendly, Full-Day); existing capitals (BBQ, DXB) are kept."""
SMALL = {"a", "an", "and", "as", "at", "but", "by", "for", "from", "in", "nor", "of", "on", "or", "per", "the", "to", "with"}


def title_case(s):
    words = s.split(' ')
    out = []
    for i, w in enumerate(words):
        core = w.strip(',:;')
        if 0 < i < len(words) - 1 and core.lower() in SMALL and not words[i - 1].endswith(':'):
            out.append(w.lower()); continue
        out.append('-'.join(p[:1].upper() + p[1:] for p in w.split('-')))
    return ' '.join(out)


if __name__ == '__main__':
    for s in ["Private evening desert safari", "Kids-friendly evening safari, Abu Dhabi", "Candlelight dinner for two", "Morning safari with quad bike",
              "Full-day Abu Dhabi city tour", "Dune buggy and quad bike", "Dubai city tour and dinner cruise", "Layover safari from Dubai Airport", "Dhow dinner cruise"]:
        print(title_case(s))
