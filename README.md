# Opetussovellus
<a name="ylos"></a>

Opetussovelluksen tarkoituksena on tarjota selainpohjainen alusta opetuksen tueksi sekä opettajille että oppilaille. Sovelluksen avulla opettajat voivat luoda oppilaille suoritettavaksi erilaisia kurssikohtaisia tehtäviä ja seurata näiden suorittamisen edistymistä. Lisäksi sovellukseen voi lisätä tehtävien lisäksi myös tekstipohjaista sisältöä. Sovellus tarjoaa yksilöllisen näkymän kullekin käyttäjälle ja omat käyttäjäroolit opettajille ja oppilaille. Käyttäjä tunnistetaan henkilökohtaisen käyttäjätunnuksen avulla. Näitä ylläpidetään ylläpitoroolin avulla.

Sovellus toteutetaan Helsingin yliopiston tietojenkäsittelytieteen aineopintojen tietokantasovellus-harjoitustyönä (tunnetaan myös _tsoha_). Lisätietoja löytyy kurssin [omilta sivulta](https://hy-tsoha.github.io/materiaali/index).

Sovelluksen aiheen pohjana toimii kurssimateriaalin ehdotus opetussovelluksen [sisällöstä](https://hy-tsoha.github.io/materiaali/pages/aiheen_valinta.html)

## Sisältö

- [Vaatimukset](#vaatimukset)

   - [Käyttöliittymä](#ui)
   - [Yhteenveto](#yhteenveto)
- [Arkkitehtuuri](#arkkitehtuuri)
- [Toteutus tällä hetkellä](#toteutus)
- [Kirjautuminen Herokuun](#kirjautuminen)


## <a name="vaatimukset"></a>Vaatimukset

Sovelluksessa on tuki kolmelle käyttäjäroolille:

1. Opiskelija
2. Opettaja
3. Ylläpitäjä

Kullekin käyttäjälle on oma henkilökohtaisella tunnuksella tunnistettava käyttäjätili johon kirjaudutaan sovelluksen aloitussivulta. Tunnus on siten aina yksilöllinen eikä useammalla käyttäjällä voi olla saman nimistä tunnusta. Tunnus on vähintään viiden merkin mittainen. Käyttäjät voivat luoda itse opiskelija-tason tunnunnuksen. Muita tunnuksia voi hallinnoida vain ylläpitäjä-roolin omaava käyttäjä, mutta kukin käyttäjä roolista riippumatta voi muuttaa omaa salasanaansa ja mahdollisia muita henkilökohtaisia tietojaan. Sovelluksessa on aina valmiina ylläpitotunnus, jota ei voi poistaa.

Sovellukseen voi luoda kursseja, joilla on yksilöllinen tunnus, kurssin nimi ja kuvaus. Kunkin kurssin alle voi:
 - luoda teksti- ja kuvapohjaista sisältöä
 - automaattisesti tarkastettavia tehtäviä

Opettajat ja ylläpitäjät voivat luoda ja tarkastella kursseja. Kurssien poistaminen tapahtuu joko kurssin luoneen opettajan tai kenen tahansa ylläpitäjän toimesta. Opettajat voivat tuottaa ja muokata kurssien sisältöä.

Opiskelijat voivat liittyä itse haluamilleen kursseille. Opettajat ja ylläpitäjät voivat nähdä, ketä kursseille on liittynyt.

Ilmoittauduttuaan kurssille opiskelijat voivat nähdä valitun kurssin sisällön ja suorittaa tämän alle luotuja tehtäviä. Opettajat voivat nähdä tehtävien suorituksiin liittyviä tietoja. Opiskelijat näkevät vain omat tietonsa.

### <a name="ui"></a>Käyttöliittymä

Sovelluksen käyttöliittymä on selainpohjainen ja sen tulee toimia yleisimmillä selaimilla (Chrome ja Firefox) sekä tekstipohjaisella selaimella.

Alla käyttöliittymäluonnos opiskelijakäyttäjän näkökulmasta.

![ui-luonnos](./dokumentaatio/opetussovellus_ui_opiskelija.png)

###  <a name="yhteenveto"></a>Yhteenveto

Yhteenvetona alla taulu toiminnoista ja oikeuksista.

| Toiminto					| Opiskelija	| Opettaja	| Ylläpitäjä 	|
| :--------					| :------:	| :-----:		| :----:		|
| **Käyttäjähallinta** |
| Uuden käyttäjätunnuksen luonti (Opiskelija) 	| X 		| X		| X		|
| Käyttäjän muuttaminen opettajaksi 		| 		| 		| X		|
| Käyttäjän muuttaminen ylläpitäjäksi		| 		|		| X		|
| Omien käyttäjätietojen muuttaminen 		| X		| X		| X		|
| Toisten käyttäjätietojen muuttaminen		| 		|		| X		|
| **Sisältö**	 				| 		|		| 		|
| Kurssien luominen 				| 		| X		| X		|
| Oman kurssin poistaminen			| 		| X		| X		|
| Toisen luoman kurssin poistaminen		| 		| 		| X		|
| Oman kurssin sisällön muokkaaminen		| 		| X		| X		|
| Toisen kurssin sisällön muokkaaminen		| 		| X<sup>[1](#a1)</sup>	| X		|
| Kurssien kuvauksen tarkasteleminen		| X		| X		| X		|
| Kursseille ilmoittautuminen			| X		| 	X	| X		|
| Kurssien materiaalien tarkastelminen / suorittaminen	| X <sup>[2](#a2)</sup> | X	| X		|
| Kurssien materiaalien muokkaaminen 		| 		| X		| X 		|
| Omien suoritusten tarkasteleminen 		| X		| X		| X		|
| Toisten suoritusten tarkasteleminen 		| X 		| X		| X		|

<a name="a1">1</a>: Toistaiseksi opettajat voivat muokata myös toistensa kursseja, mutta jatkokehitysideana opettajien oikeuksia voisi rajoittaa tai luoda edistyneemmät opettaja-tunnukset - tai mahdollisuuden jakaa oikeuksia muille opettajille kurssikohtaisesti.

<a name="a2">2</a>: Opiskelijan ilmoittauduttua kurssille.


## <a name="arkkitehtuuri"></a>Arkkitehtuuri

Sovelluksen toiminnallisuus toteutetaan Python 3-kielellä Flask-moduulia hyödyntäen, jonka avulla renderöidään käyttöliittymänä toimivat HTML-sivut. Sivuilla käytetään myös JavaScriptiä loppukäyttäjkäyttökokemusta parantavien toimintojen toteuttamiseksi. Tarkemmat tiedot sovelluksen riippuvuuksista löytyy tiedostosta [requirements.txt](requirements.txt)

Sovelluksessa käytettävien tietojen pysyväistallennuseen käytetään PostgreSQL-tietokantaa.

### <a name="dbrakenne"></a>Tietokannan rakenne

Tietokannassa on käytössä seuraavat taulut:
- Users (sovelluksen käyttäjätiedot)
- Courses (kurssit)
- Participants (kurssien osallistujat)
- Chapters (kurssien luvut)
- Exercises (lukujen tehtävät)
- Choises (tehtävien vastausvaihtoehdot)
- Answers (käyttäjien vastaukset)

Tietakannan SQL-skeema on tällä hetkellä seuraava:

```
CREATE TABLE users
(
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    first_name TEXT,
    last_name TEXT
);

CREATE TABLE courses
(
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    description TEXT,
    teacher_id INTEGER REFERENCES users (id),
    created_at TIMESTAMP
);

CREATE TABLE participants
(
    course_id INTEGER REFERENCES courses (id),
    user_id INTEGER REFERENCES users (id)
);

CREATE TABLE chapters
(
    id SERIAL PRIMARY KEY,
    ordinal INTEGER,
    name TEXT NOT NULL,
    content TEXT,
    course_id INTEGER REFERENCES courses (id),
    creator_id INTEGER REFERENCES users (id),
    created_at TIMESTAMP
);

CREATE TABLE exercises
(
    id SERIAL PRIMARY KEY,
    ordinal INTEGER,
    name TEXT NOT NULL,
    question TEXT,
    course_id INTEGER REFERENCES courses (id),
    chapter_id INTEGER REFERENCES chapters (id),
    creator_id INTEGER REFERENCES users (id),
    created_at TIMESTAMP
);

CREATE TABLE choices
(
    id SERIAL PRIMARY KEY,
    correct BOOLEAN,
    description TEXT NOT NULL,
    exercise_id INTEGER REFERENCES exercises (id),
    created_at TIMESTAMP
);

CREATE TABLE answers
(
    exercise_id INTEGER REFERENCES exercises (id),
    choice_id INTEGER REFERENCES choices (id),
    user_id INTEGER REFERENCES users (id),
    answered_at TIMESTAMP
);
```

## <a name="toteutus"></a>Toteutus tällä hetkellä (Välipalautus 3)

Tällä hetkellä sovelluksen toiminnallisuuksista on toteutettu seuraavaa:

Ennen kirjautumista käyttäjäjä voi:

- Tarkastella etusivua
- Kirjautua sisään tunnuksella ja salasanalla
- Luoda uuden tunnuksen

Kirjauduttuaan käyttäjä voi:

- Tarkastella etusivua
- Hallita kursseja:
  - Hakea kursseja
  - Tarkastella kurssien sivuja
  - Ilmoittautua kursseille
  - Luoda uuden kurssin
- Hallita, tarkastella ja käyttää kurssien sisältöä:
  - Luoda kursseille uusia lukuja, jotka sisältävät luvun järjestysluvun, nimen ja tekstiä
  - Muokata jo luotuja lukuja
  - Luoda lukujen alle tehtäviä sisältäen tehtävän järjestysluvun, nimen, kysymyksen ja käyttäjän määrittelemän määrän vastausvaihtoehtoja (vaihtoehtoja on vähintään yksi, useampi voi olla oikein)
  - Vastata lukujen tehtäviin (vain kerran)
  - Nähdä oliko oma vastaus oikein vai väärin ja mikä/mitkä olisivat olleet oikeita vastauksia
  - Nähdä kurssin tehtävien yhteenvedon (kpl vastauksista oikein, väärin ja vastauksia yhteensä)

Huomaa, että alkuperäiseen suunnitelmaan nähden, sovelluksesta puuttuu vielä seuraavia olennaisia toimintoja:

- Käyttäjäroolien ja sisällön hallinta:
  - Eri käyttäjäroolit ja toimintojen rajaus roolin perusteella (esim. kurssisisältöjen hallinta
  - Kurssisisältöjen näkyvyys sen perusteella onko käyttäjä ilmoittautunut vai ei (nyt ilmoittautumisella ei ole väliä)
  - Käyttäjän henkilökohtainen yhteenveto

Toisin sanoen, kaikki käyttäjät ovat samanarvoisia ja voivat sekä nähdä että muokata sisältöä riippumatta siitä, onko käyttäjä oikeasti opettaja vai oppilas tai ilmottautunut kurssille vai ei.

## <a name="kirjautuminen"></a>Kirjautuminen Herokuun

Sovellukseen pääsee Herokussa osoitteessa: https://tso-harjoitustyo.herokuapp.com/ .

Voit luoda itsellesi omat testitunnukset/-tunnuksia sovelluksen sivulta https://tso-harjoitustyo.herokuapp.com/register.

On suositeltavaa luoda erilaisia kursseja, kurssien alle lukuja ja lukujen alle tehtäviä. Koita myös ratkaista tekemiäsi tehtäviä. Kokeile rohkeasti löydätkö ohjelmasta virheitä syötteillä, joihin ei olla toistaiseksi kehitysvaiheessa varauduttu.

[Palaa ylös](#ylos)