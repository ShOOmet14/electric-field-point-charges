import numpy as np
import matplotlib.pyplot as plt

# zmienne globalne (według projektu ustawione na 1), można odkomentować aby uzyskać rzeczywistą wartość
#epsilon = 8.854e-12 
#pi = np.pi
#k = 1/(4*pi*epsilon)

k = 1

# obiekt ładunek, zawiera współrzędne oraz wartość ładunku, metodę wypisującą te parametry, metodę losującą ładunek oraz metodę losującą współrzędne ładunku na podstawie wszystkich dostępnych miejsc (każdy ładunek może występować tylko raz na daną parę współrzędnych)
class Ladunek:
    def __init__(self, x, y, q):
        self.x = x
        self.y = y
        self.q = q

    def __repr__(self):
        nazwa = self.__class__.__name__
        return f'{nazwa} (x = {self.x}, y = {self.y}, q = {self.q})'

    @staticmethod
    def losujWartoscLadunku(ziarno, ladunekMin, ladunekMax):
        q = 0
        while q == 0:
            q = int(ziarno.integers(ladunekMin, ladunekMax + 1))

        return q
    
    @classmethod
    def losuj(cls, ilosc, ziarno, wspolrzednaMin, wspolrzednaMax, ladunekMin, ladunekMax, punkt):
        mozliweWspolrzedne = [
            (x, y)
            for x in range (wspolrzednaMin, wspolrzednaMax + 1)
            for y in range (wspolrzednaMin, wspolrzednaMax + 1)
            if (x, y) != (punkt.x, punkt.y)
        ]

        if ilosc > len(mozliweWspolrzedne):
            raise ValueError(f"Za dużo ładunków! Liczba zależna jest od współrzędnych min i max, w Twoim maksymalnie możesz wylosować {len(mozliweWspolrzedne)} unikalnych ładunków")
        
        indeksy = ziarno.choice(len(mozliweWspolrzedne), size = ilosc, replace = False)

        ladunki = []
        for i in indeksy:
            x, y = mozliweWspolrzedne[i]
            q = cls.losujWartoscLadunku(ziarno, ladunekMin, ladunekMax)
            ladunki.append(cls(x, y, q))
        
        return ladunki

# obiekt punkt, zawiera współrzędne x i y, metodę wypisywana oraz metodę sprawdzającą poprawność współrzędnych
class Punkt:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        nazwa = self.__class__.__name__
        return f'{nazwa} (x = {self.x}, y = {self.y})'
    
    def sprawdzenie(self, wspolrzednaMin, wspolrzednaMax):
        return wspolrzednaMin <= self.x <= wspolrzednaMax and wspolrzednaMin <= self.y <= wspolrzednaMax

# funkcja losująca ładunki, ich współrzędne i wartości, oraz umożliwa wybór współrzędnych punktu
def losowanieLadunkow():
    # wczytywanie limintów współrzędnych, oraz x i y dla punktu
    wspolrzedneMax = int(input("Podaj maksymalne współrzędne dla punktów (w każdą stronę od środka układu): "))
    wspolrzedneMin = -wspolrzedneMax

    xPunktu = int(input("Podaj współrzędną x punktu: "))
    yPunktu = int(input("Podaj współrzędną y punktu: "))

    punkt = Punkt(xPunktu, yPunktu)
    
    if not punkt.sprawdzenie(wspolrzedneMin, wspolrzedneMax):
        print("Współrzędne punktu nie mogą wychodzić poza zakres.")
        return None
    
    print(repr(punkt))

    # wczytywanie liczby ładunków, ich wartości (minimum i maksimum) i weryfikacja
    maxIlosc = (2*wspolrzedneMax + 1)**2 - 1
    ilosc = int(input(f"Podaj ilość ładunków (max: {maxIlosc}): "))

    if ilosc <= 0:
        print("Ilość musi być dodatnią liczbą naturalną.")
        return None
    
    if ilosc > maxIlosc:    
        print(f"Za dużo ładunków! Maksymalnie: {maxIlosc}.")
        return None
    
    ladunekMin = int(input("Podaj minimalną wartość ładunku: "))
    ladunekMax = int(input("Podaj maksymalna wartość łądunku: "))

    if ladunekMin > ladunekMax:
        print("Wartość mininimalna nie może być większa od wartości maksymalnej.")
        return None
    
    if ladunekMin == 0 and ladunekMax == 0:
        print("Nie można losować tylko zera, podaj inny zakres.")
        return None

    ziarno = np.random.default_rng()

    ladunki = Ladunek.losuj(ilosc, ziarno, wspolrzedneMin, wspolrzedneMax, ladunekMin, ladunekMax, punkt)
    
    for i in ladunki:
        print(repr(i))

    return punkt, ladunki, wspolrzedneMin, wspolrzedneMax
    
# funkcja licząca składowe wektora pola elektrycznego, na wejściu: ładunek punktu, jego współrzędne x,y i współrzędne punktu badanego
def poleElektryczne(ladunek, xLadunku, yLadunku, xPunktu, yPunktu):
    # składowe i wartość wektora położenia
    r_x = xPunktu - xLadunku
    r_y = yPunktu - yLadunku
    wartoscR = np.sqrt(r_x*r_x + r_y*r_y)
    wartoscR = max(wartoscR, 1e-12)

    # składowe wektora pola elektrycznego
    E_x = ladunek*k*r_x / (wartoscR*wartoscR*wartoscR) # używam mnożenia bo jest bardziej wydajne niż potęgowanie
    E_y = ladunek*k*r_y / (wartoscR*wartoscR*wartoscR)
    return E_x, E_y

# funkcja obliczająca superpozycję wszystkich pól elektrycznych oraz wypisująca wartości pola elektrycznego dla danego ładunku
def superpozycjaPolElektrycznych(ladunkiDane, punktDane):
    E_calk_x = 0
    E_calk_y = 0

    for ladunek in ladunkiDane:
        tempX, tempY = poleElektryczne(ladunek.q, ladunek.x, ladunek.y, punktDane.x, punktDane.y)
        E_calk_x += tempX
        E_calk_y += tempY
        wartoscE = np.sqrt(tempX*tempX + tempY*tempY)
        print(f'Dla ładunku {ladunek} E_x = {tempX:.6f}, E_y = {tempY:.6f}, |E| = {wartoscE:.6f}.')

    return E_calk_x, E_calk_y

def wykres(punkt, ladunki, wspolrzedneMin, wspolrzedneMax):
    E_x, E_y = superpozycjaPolElektrycznych(ladunki, punkt)
    wartoscE = np.sqrt(E_x*E_x + E_y*E_y)

    print(f"\nWYNIK: E_x = {E_x:.6f}, E_y = {E_y:.6f}, |E| = {wartoscE:.6f}\n", "Ważne, strzałka jest skalowana na rysunku.")

    dlugosc_strzalki = 2.0
    if wartoscE > 0:
        E_x = (E_x / wartoscE) * dlugosc_strzalki
        E_y = (E_y / wartoscE) * dlugosc_strzalki
    else:
        E_x, E_y = 0, 0

    plt.quiver(punkt.x, punkt.y, E_x, E_y, angles='xy', scale_units='xy', scale=1, color='g')
    plt.plot(punkt.x, punkt.y, 'og')
    plt.text(punkt.x + 0.1, punkt.y + 0.1, "P")

    dodatni_podpis = False
    ujemny_podpis = False

    for ladunek in ladunki:
        if ladunek.q > 0:
            if not dodatni_podpis:
                plt.plot(ladunek.x, ladunek.y, "ob", label="q > 0")
                dodatni_podpis = True
            else:
                plt.plot(ladunek.x, ladunek.y, "ob")
        else:
            if not ujemny_podpis:
                plt.plot(ladunek.x, ladunek.y, "or", label="q < 0")
                ujemny_podpis = True
            else:
                plt.plot(ladunek.x, ladunek.y, "or")
        plt.text(ladunek.x + 0.15, ladunek.y + 0.15, f"{ladunek.q:+d}") # + pokazuje znak, d - liczba całkowita

    margines = 1
    plt.grid(True)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.gca().set_aspect('equal', adjustable='box') # równe osie X i Y
    plt.xlim(wspolrzedneMin - margines, wspolrzedneMax + margines)
    plt.ylim(wspolrzedneMin - margines, wspolrzedneMax + margines)
    plt.title("Wektor pola elektrycznego w punkcie P")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    wynik = losowanieLadunkow()
    
    if wynik is not None:
        punkt, ladunki, wspolrzedneMin, wspolrzedneMax = wynik
        wykres(punkt, ladunki, wspolrzedneMin, wspolrzedneMax)

# dodać na github jako projekt po przetłumaczeniu na angielski