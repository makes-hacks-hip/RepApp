from django.db import models


class Cafe(models.Model):
    ort = models.CharField(max_length=200)
    datum = models.DateField()


class Reparateur(models.Model):
    name = models.CharField(max_length=200)
    mail = models.CharField(max_length=200)


class Organisator(models.Model):
    name = models.CharField(max_length=200)
    mail = models.CharField(max_length=200)


class Gerät(models.Model):
    identifier = models.CharField(max_length=200)
    besitzer = models.CharField(max_length=200)
    mail = models.CharField(max_length=200)
    gerät = models.CharField(max_length=200)
    fehler = models.TextField()
    folgetermin = models.BooleanField()


class Termin(models.Model):
    uhrzeit = models.TimeField()
    bestätigt = models.BooleanField()
    cafeid = models.ForeignKey(Cafe, on_delete=models.CASCADE)
    reparateurid = models.ForeignKey(Reparateur, on_delete=models.CASCADE)
    gerätid = models.ForeignKey(Gerät, on_delete=models.CASCADE)


class Frage(models.Model):
    frage = models.TextField()
    antwort = models.TextField()
    datum = models.DateField()
    organisatorid = models.ForeignKey(Organisator, on_delete=models.CASCADE)
    reparateurid = models.ForeignKey(Reparateur, on_delete=models.CASCADE)
    gerätid = models.ForeignKey(Gerät, on_delete=models.CASCADE)
