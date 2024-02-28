# AI map engine

## Opis

Ten projekt ma na celu przekształcenie istniejącej - napisanej wiele lat temu przeze mnie - prostej gry, stworzonej pierwotnie w JavaScript, na język Python. 
Pierwszym celem jest przeniesienie mechaniki i funkcjonalności gry, ale głównym celem jest rozwinięcie jej o nowe możliwości 
dzięki wykorzystaniu technik uczenia maszynowego. Przy tym przede wszystkim zgłebienie tematu, poznanie możliwości i ograniczeń wykorzystania AI w tworzeniu gier.

Projekt składa się z trzech głównych części:

- Przepisanie gry na Python: Przeniesienie logiki i mechaniki gry do Pythona, z wykorzystaniem odpowiednich bibliotek do obsługi grafiki i interakcji użytkownika.

- Wytrenowanie sieci neuronowej do przechodzenia gry: Rozwój modelu uczenia ze wzmocnieniem (Deep Reinforcement Learning, DRL), który będzie zdolny do nauczenia się strategii maksymalizacji zdobywanych punktów w grze.

- Wytrenowanie sieci neuronowej do tworzenia mapy: Opracowanie drugiego modelu DRL, który będzie odpowiedzialny za generowanie map gry. Mapy te będą musiały być wystarczająco zróżnicowane, aby zapewnić wyzwanie dla pierwszej sieci, jednocześnie oferując bogactwo elementów do interakcji.

## Szczegóły

### Przepisanie Gry na Python
- Mapy: Gra ma taką zaletę (dla tego projektu), że tworzy 'świat gry' z mini mapki na której każdy piksel ma inne znaczenie i jest inaczej reprezentowany w 'świecie gry' w zależności od jego koloru,
- Wybór biblioteki graficznej: Do realizacji gry w Pythonie, postanowiłem wykorzystać bibliotekę Pygame, która oferuje szerokie możliwości w zakresie tworzenia interfejsu graficznego i obsługi zdarzeń.
- Modularyzacja kodu: Przy przenoszeniu logiki gry, wprowadzę zmiany aby podzielić kod na moduły odpowiadające różnym aspektom gry (np. logika gry, renderowanie grafiki, obsługa wejścia), 
co ułatwi późniejsze wprowadzanie zmian i integrację z sieciami neuronowymi.

### Wytrenowanie Sieci Neuronowej do Przechodzenia Gry
- Wybór algorytmu: Dla deep reinforcement learning (DRL), zamierzam wykorzystgać Policy Gradients (np. A3C lub PPO).
- Symulacja środowiska: Gra musi być używana jako środowisko dla agenta DRL, oferując API do wykonania akcji i otrzymania obserwacji oraz nagród.

### Wytrenowanie Sieci Neuronowej do Tworzenia Mapy
- Generative Adversarial Networks (GANs): Pierwszy pomysł (żeby nauczyć wielu rzeczy przy jednym projekcie) to generowanie map z wykorzystaniem sieci GAN, gdzie sieć generatywna tworzy mapy, a dyskryminator (w tym przypadku, sieć do przechodzenia gry) ocenia je pod kątem trudności i interesujących cech.
- Customizacja funkcji straty: Aby zachęcić do tworzenia map, które są wyzwaniem, ale też oferują możliwość zdobycia punktów, potrzeba odpowiedniej funkcji straty, aby uwzględniała oba te aspekty.

### Współpraca między Sieciami
- Funkcja kosztu jako łącznik: Kluczowym elementem projektu będzie funkcja kosztu, która pozwoli na komunikację między sieciami. Musi ona efektywnie bilansować trudność map z możliwością zdobywania punktów, dążąc do równowagi.
- Iteracyjna optymalizacja: Proces ten będzie wymagał wielu iteracji treningowych, gdzie na podstawie wyników jednej sieci, druga będzie dostosowywać swoje działania. Może być konieczne ręczne dostosowanie wagi poszczególnych składowych funkcji kosztu, aby znaleźć optymalną równowagę.


## Technologie

- Python 3.11
- Pygame - do implementacji gry
- TensorFlow - do implementacji sieci neuronowych

## Instalacja

Instrukcje dotyczące instalacji potrzebnych narzędzi i bibliotek.

```bash
# Klonowanie repozytorium
git clone https://github.com/daniel-w-p/ai_map_engine.git

# Przechodzenie do katalogu projektu
cd ai_map_engine

# Instalacja zależności (przykład używa pip, ale możesz dostosować do swoich potrzeb)
pip install -r requirements.txt
```

## Uruchomienie

### Uruchomienie gry
```python main_game.py```

### Uruchomienie treningu sieci do przechodzenia gry
```python train_agent.py```

### Uruchomienie procesu generowania map
```python generate_maps.py```