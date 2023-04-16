from django.db import models


class Cafe(models.Model):
    ort = models.CharField(max_length=200)
    datum = models.DateField()

    def __str__(self):
        return f'Repair-Café am {self.datum} (Ort: {self.ort})'


class Reparateur(models.Model):
    name = models.CharField(max_length=200)
    mail = models.CharField(max_length=200)

    def __str__(self):
        return f'Reparatuer {self.name} (eMail: {self.mail})'


class Organisator(models.Model):
    name = models.CharField(max_length=200)
    mail = models.CharField(max_length=200)

    def __str__(self):
        return f'Organisator {self.name} (eMail: {self.mail})'


class Gerät(models.Model):
    identifier = models.CharField(max_length=200)
    besitzer = models.CharField(max_length=200)
    mail = models.CharField(max_length=200)
    gerät = models.CharField(max_length=200)
    fehler = models.TextField()
    folgetermin = models.BooleanField()

    def __str__(self):
        return f'Gerät {self.gerät} von {self.besitzer} (eMail: {self.mail})'


class Termin(models.Model):
    uhrzeit = models.TimeField()
    bestätigt = models.BooleanField()
    cafeid = models.ForeignKey(Cafe, on_delete=models.CASCADE)
    reparateurid = models.ForeignKey(Reparateur, on_delete=models.CASCADE)
    gerätid = models.ForeignKey(Gerät, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'Termin {self.cafeid.datum} {self.uhrzeit} für Gerät {self.gerätid.gerät} von {self.gerätid.besitzer}'


class Frage(models.Model):
    frage = models.TextField()
    antwort = models.TextField()
    datum = models.DateField()
    organisatorid = models.ForeignKey(
        Organisator, on_delete=models.CASCADE, null=True)
    reparateurid = models.ForeignKey(
        Reparateur, on_delete=models.CASCADE, null=True)
    gerätid = models.ForeignKey(Gerät, on_delete=models.CASCADE)

    def __str__(self):
        return f'Frage vom {self.datum} zum Gerät {self.gerätid.gerät}'
