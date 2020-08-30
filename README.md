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

Sovelluksen käsittelemät sivupyynnöt toteutetaan moduulissa routes.py eikä sen funktiolilla ole suoraa yhteyttä tietokantaan, vaan se kutsuu moduuleita users.py, courses.py tai course_contents.py riippuen siitä, mitä tietoa käsitellään. Käyttäjätietojen käsittelyyn liittyvät pyynnöt käsitellään users.py kautta, kurssien  tietojen lukemisen ja tallennuksen hoitaa courses.py ja kurssien sisältöjen (lukujen ja tehtävien) lukemisesta ja tallentamisesta vastaa course_contents.py.

Sovelluksessa käytettävien tietojen pysyväistallennuseen käytetään PostgreSQL-tietokantaa.

### <a name="dbrakenne"></a>Tietokannan rakenne

Tietokannassa on käytössä seuraavat taulut:
- Users (sovelluksen käyttäjätiedot)
- Roles (käyttäjäroolit)
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
    last_name TEXT,
    role_id INTEGER REFERENCES roles (id)
);

CREATE TABLE roles
(
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE
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

Lisäksi tietokantaan lisätään käyttöönoton yhteydessä roolit opiskelijalle, opettajalle ja ylläpitäjälle:
```
INSERT INTO roles (name)
VALUES ('student'), ('teacher'), ('admin');
```

## <a name="toteutus"></a>Toteutus (loppupalautus)

Sovelluksen toteutus on kuvattu alla käyttäjäroolit huomioiden.

Ennen kirjautumista kaikki käyttäjät voivat:

- Tarkastella etusivua
- Kirjautua sisään tunnuksella ja salasanalla
- Luoda uuden *opiskelija*-tasoisen tunnuksen

Kirjauduttuaan *kaikki *käyttäjät voivat:

- Tarkastella etusivua
- Hakea kursseja
- Ilmoittautua kursseille
- Katsoa kurssien etusivua sisältäen kurssin opettajan, kurssien kuvauksen ja osallistujat
- Ilmoittauduttaan kurssille:
  - Tarkastella kurssin lukuja
  - Ratkaista kurssin lukujen tehtäviä ja nähdä oliko vastaus oikein vai väärin sekä mitkä vastauksista olisi olleet oikein
      - Opettajien ja ylläpitäjien vastauksia ei tallenneta tietokantaan, vaan he voivat kokeilla vastauksia rajattomasti ja tarkastella, miltä sivu näyttää opiskelijan näkökulmasta. 
      - Opiskelijat voivat vastata vain kerran ja tieto tallentuu tietokantaan

Kirjauduttuaan vain *opettajat* ja *ylläpitäjät* voivat:

- Tarkastella kurssien sisältöä eli lukuja ja tehtäviä ilmoittautumatta
- Luoda uuden kurssin, jolloin käyttäjä lisätään automaattisesti kurssin vastuuopettajaksi. (Tätä ei voi tällä hetkellä muuttaa)
- Ilmottauduttuaan kurssille tai luotuaan itse kurssin:
  - Tarkastella kurssin tehtävien vastausten yhteenvetoa kurssin etusivulla
  - Luoda uusia lukuja ja muokata vanhoja
  - Luoda uusia tehtäviä lukujen alle tai luoda vanhoja

Kirjauduttuaan vain *ylläpitäjät* voivat:
- Muokata kurssien sisältöä (lukuja ja tehtäviä) ilmottautumatta
- Tarkastella kaikkia käyttäjätunnuksia ja muokata näiden tietoja (etunimi, sukunimi, käyttäjärooli)

## <a name="kirjautuminen"></a>Kirjautuminen Herokuun

Sovellukseen pääsee Herokussa osoitteessa: https://tso-harjoitustyo.herokuapp.com/ .

Sovelluksesta löytyy valmiiksi seuraavat käyttäjätunnukset:

- Opiskelija: 
  - käyttäjänimi: "opiskelija", salasana: "student"
- Opettaja:
  - käyttäjänimi: "opettaja" salasana: "teacher"
- Ylläpitäjä:
  - käyttäjänimi: "yllapitaja" salasana: "admin"

Voit myös halutessasi luoda itsellesi omat testitunnukset/-tunnuksia sovelluksen sivulta https://tso-harjoitustyo.herokuapp.com/register.

[Palaa ylös](#ylos)