from pathlib import Path

for path in Path("data/local/").glob("*"):
    lang = path.name
    if len(str(lang)) <= 3:
        continue
    if lang == "tajik":
        continue

    with (path / "text" / "vocab").open() as f:
        vocab = []
        for line in f:
            vocab.append(line.split()[0])

    with (path / "text" / "words").open("w") as f:
        for word in vocab:
            print(word, file=f)
