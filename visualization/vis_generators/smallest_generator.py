# Filtern der Primzahlen, für die ein kleinster Erzeuger gefunden wurde
valid_smallest_generators = [g for g in smallest_generators if g is not None]

# Zählen der Häufigkeit jedes gültigen Erzeugers
valid_generator_counts = Counter(valid_smallest_generators)

# Sortieren der Erzeuger nach ihrer Größe für die Visualisierung
sorted_valid_generators = sorted(valid_generator_counts.items())

# Vorbereitung der Daten für die Visualisierung
valid_generators, valid_counts = zip(*sorted_valid_generators)

# Visualisierung
plt.figure(figsize=(12, 6))
plt.bar(valid_generators, valid_counts, color='teal')
plt.xlabel('Kleinster Erzeuger')
plt.ylabel('Häufigkeit')
plt.title('Häufigkeit des kleinsten Erzeugers für Primzahlen von 2 bis 1000')
plt.xticks(np.arange(min(valid_generators), max(valid_generators)+1, 1))
plt.grid(axis='y')
plt.show()
