# Esimerkki, jotta muistais myöhemmin:
# luodaan luvulle 236 tarkistusbitti
# Ensimmäisessä vaiheessa käännetää luku ja lisätää nolla -> 0632
# pysyäkseen mukana täytyy katsoa alhaalla olevaa calchecksum funktiota
# verhoeff_table_d[c][verhoeff_table_p[(i+1)%8][int(item)]]
# aluksi c ja i on kumpikin nolla eli tiedetään, että d taulun x koordinaatti on 0
# y koordinaatti saadaan p taulusta
# p taulun x koordinaatti tulee indeksi modulo 8, joka siis on 1.
# p taulun y koordinaatti on meidän käännetyn luvun ensimmäinen alkio eli 2, joten
# p(1,2) Nähdään että sen on 7 eli 7 on d taulun y koordinaatti
# Tämän avulla saadaan c muuttujan uusi arvo d(0, 7) = 7
# Seuraavassa iteraatiossa tiedetään jälleen c:n arvo 7 ja etsitään samaan tyyliin d taululle
# y:n arvo, kunnes arvo nolla tulee. Nolla laskun jälkeen katsotaan j taulusta c arvoa vastaava luku
# joka on haluttu checksum digit.


class VerhoeffAlgorithm:
    def __init__(self) -> None:
        self.verhoeff_table_d = (
            (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
            (1, 2, 3, 4, 0, 6, 7, 8, 9, 5),
            (2, 3, 4, 0, 1, 7, 8, 9, 5, 6),
            (3, 4, 0, 1, 2, 8, 9, 5, 6, 7),
            (4, 0, 1, 2, 3, 9, 5, 6, 7, 8),
            (5, 9, 8, 7, 6, 0, 4, 3, 2, 1),
            (6, 5, 9, 8, 7, 1, 0, 4, 3, 2),
            (7, 6, 5, 9, 8, 2, 1, 0, 4, 3),
            (8, 7, 6, 5, 9, 3, 2, 1, 0, 4),
            (9, 8, 7, 6, 5, 4, 3, 2, 1, 0)
        )

        self.verhoeff_table_p = (
            (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
            (1, 5, 7, 6, 2, 8, 3, 0, 9, 4),
            (5, 8, 0, 3, 7, 9, 6, 1, 4, 2),
            (8, 9, 1, 6, 0, 4, 3, 5, 2, 7),
            (9, 4, 5, 3, 1, 2, 6, 8, 7, 0),
            (4, 2, 8, 6, 5, 7, 3, 9, 0, 1),
            (2, 7, 9, 3, 8, 0, 6, 4, 1, 5),
            (7, 0, 4, 6, 9, 1, 3, 2, 5, 8)
        )

        self.verhoeff_table_inv = (0, 4, 3, 2, 1, 5, 6, 7, 8, 9)

    def calchecksum(self, number: str) -> int:
        c = 0
        for i, item in enumerate(reversed(number)):
            c = self.verhoeff_table_d[c][self.verhoeff_table_p[(
                i+1) % 8][int(item)]]
        return self.verhoeff_table_inv[c]

    def generateVerhoeff(self, number: int, partition_id: str) -> str:
        national_id = '1000288'
        value = f'{str(number)}{national_id}{partition_id}'
        return f'{value}{self.calchecksum(value)}'

    def validate(self, number) -> bool:
        c = 0
        for i, item in enumerate(reversed(str(number))):
            c = self.verhoeff_table_d[c][self.verhoeff_table_p[i % 8][int(
                item)]]
        return c == 0
