#Python Dictionary snadno a rychle

Důvody proč programovat v Pythonu jsou určitě jiné než rychlost běhu výsledných aplikaci.
To ale není důvod rezignovat na různé možnostmi optimalizace a zrychlení vlastního kódu. V tomhle článku se konkrétně podíváme na slovníky -
dictionary, jejich vytváření a naplňování daty.

##Jednou větou

Nejrychlejší způsob v Pythonu 2.7. i 3.3. je použít _defaultdict_ z balíčku _collections_. Jestli chcete vědět proč a jak,
čtěte dál.

##Modelová úloha

[Slovníky](http://docs.python.org/2/library/stdtypes.html#dict) jsou skvělá datová struktura.
Zejména pokud máme nějaká data, ve kterých potřebujeme
chtít opakovaně vyhledávat. Základem jejich implementace je totiž [hašovací tabulka](http://cs.wikipedia.org/wiki/Ha%C5%A1ovac%C3%AD_tabulka).

Pěkným příkladem použití slovníku je základní frekvenční analýza slov
v dokumentu. Tedy česky řečeno, chceme spočítat kolikrát se dané slovo v dokumentu
vyskytuje. Při řešení tohoto problému musíme opakovaně prohledávat množinu již známých slov a inkrementovat čítač. Takže jak na to?

##Implementace

První postup který většinu lidí napadne, je projít postupně vstupní pole slov a testovat, zda již slovo ve slovníku je nebo není.
Pokud není, přidáme nový klíč, pokud je, zvedneme počet výskytů o jedničku. Algoritmus můžeme zapsat
například takto:

    :::python
    def clasic(words):
      freq = {}
      for word in words:
          if word in freq:
              freq[word] += 1
          else:
              freq[word] = 1

      return freq

Podmínka existence klíče je nutná, protože bez ní bychom při už prvním slově skončili s výjimkou KeyError.
Tu samozřejmě můžeme zachytávat. To v Pythonu preferovaný přístup - říkáme tomu
[EAFP](http://docs.python.org/2/glossary.html). Je snadnější požádat o prominutí,
než o povolení. V programování dobré, ale v reálném životě to raději nezkoušejte. 
Fotit si bez povolení například vojenskou základnu by vám taky nemuseli prominout vůbec.

Tento kód je o
něco málo rychlejší, protože si ušetříme jedno hledání klíče ve slovníku. Ale protože hledání klíče
ve slovníku je rychlé, je v tomto případě úspora relativně malá.
    
    :::python
    def clasic_try(words):
        freq = {}
        for word in words:
            try:
                freq[word] += 1
            except KeyError:
                freq[word] = 1

        return freq   

Alternativním přístupem je využít [metodu _get_](http://docs.python.org/2/library/stdtypes.html#dict),
která buď vrátí hodnotu pro daný klíč, a nebo hodnotu výchozí.

    :::python
    def dictget(words):
      freq = {}
      for word in words:
          freq[word] = freq.get(word, 0) + 1

      return freq

Kód je kratší, odpadlo nám testování klíče. Respektive je ukryto v implementaci metody get. S
rychlostí je na tom ovšem výrazně hůře než první varianta. Při opakovaném zpracování větších dat,
bude rozdíl docela výrazný. Proč tomu tak je?

Jde o to volání metody get, které se provádí opakovaně. Pokud zavoláme nějakou metodu či funkci, interpret Pythonu
nejprve prohledá lokální jmenný prostor (například prostor konkrétní funkce), pokud nenajde, pokračuje prostorem globálním (modul)
a nakonec prostorem built-in, tedy samotnou implementací Pythonu. A i když jsou všechny jmenné prostory reprezentovány slovníkem, není to právě
nejrychlejší operace. Proto pro rychlost platí pravidlo: **opakovaným voláním globálních funkcí
 je lepší se vyhnout**. 

 Můžeme toho dosáhnout například tím, že si vytvoříme lokální jméno pro danou metodu.
Lokální prostor se prohledává první a je menší. Kód tedy lehce upravíme na:


    :::python
    def dictget_loc(words):
      freq = {}
      lget = freq.get
      for word in words:
          freq[word] = lget(word, 0) + 1

      return freq

Nicméně, jak si za chvilku ukážeme, i tahle varianta je díky opakovanému volání funkce o něco
pomalejší než první příklad. 

**Nejrychlejší** a zároveň asi nejelegantnější způsob je použít
 [_defaultdict_ z balíčku _collections_](http://docs.python.org/2/library/collections.html#collections.defaultdict). Tento speciální slovník se hodí vždy, když pracujeme s
hodnotami jednoho a téhož typu. V tomto případě s čísly (int), ale může to být klidně také _list_, _set_ a
další.

    :::python        
    def defdic(words):
        freq = defaultdict(int)
        for word in words:
            freq[word] += 1

        return dict(freq)

Závěrečné přetypování zpět na klasický slovník není vyloženě nutné, protože i s typem defaultdict
lze dále pracovat. Ale v rámci srovnání a testování dat je potřeba, aby nám
všechny funkce vracely objekt stejného typu.

##Benchmark
Co takhle nějaká konkrétní čísla na podporu tvrzení, že _defaultdict_ je nejrychlejší? 

Jednoduchý
benchmark za využití modulu [timeit](http://docs.python.org/2/library/timeit.html) a románu
[Les Misérables](http://en.wikipedia.org/wiki/Les_Mis%C3%A9rables) od Victora Huga získaného na [www.guttenberg.org](http://www.gutenberg.org/ebooks/135) ukazuje následující časy:

    :::bash
    Python 2.7.6.
    100 calls of function defdic took 6.9335911274 seconds
    clasic
    100 calls of function clasic took 8.97921204567 seconds
    clasic_try
    100 calls of function clasic_try took 8.96289992332 seconds
    dictget
    100 calls of function dictget took 11.6839268208 seconds
    dictget_loc
    100 calls of function dictget_loc took 9.17192482948 seconds

Victor byl pracovitý autor, a tak má txt soubor 3.2MB a 3322651 slov. Každý slovník se vytvářel 100x z dat uložených v paměti.

Opět se tedy potvrdilo pravidlo, že built-in funkcionalita je většinou rychlejší, než stejný kód napsaný přímo v Pythonu. Přesněji řečeno, to platí pro CPython, tedy nejrozšířenější z Python interpretů napsaný v jazyce C. 

Srovnáním interpretů můžeme vše zakončit. Předchozí výsledky byly z Pythonu 2.7.6. Python 3.3.2 spuštěný na stejném stroji i datech dosáhl kupodivu horších výsledků. Kupodivu proto, že všeobecně bývá 3 považována za rychlejší.
        
    :::bash
    Python 3.3.2.
    defdic
    100 calls of function defdic took 8.296376697000596 seconds
    clasic
    100 calls of function clasic took 9.956151381000382 seconds
    clasic_try
    100 calls of function clasic_try took 9.65847917300016 seconds
    dictget
    100 calls of function dictget took 12.220012431000214 seconds
    dictget_loc
    100 calls of function dictget_loc took 10.357736971000122 seconds


A jak je na tom [PyPy](http://pypy.org/) - interpret napsaný v [RPythonu](https://code.google.com/p/rpython/) využívající JIT compiler? Výsledky jsou výrazně jiné:

    :::bash
    PyPy 2.2.1 with GCC 4.8.2.
    defdic
    100 calls of function defdic took 7.35373306274 seconds
    clasic
    100 calls of function clasic took 6.84745502472 seconds
    clasic_try
    100 calls of function clasic_try took 6.14175105095 seconds
    dictget
    100 calls of function dictget took 6.44395112991 seconds
    dictget_loc
    100 calls of function dictget_loc took 6.13185596466 seconds

Čistý Python kód, tedy funkce _classic_ či _dictget_ běží v PyPy rychleji, než kompilovaný C modul defaultdict v Pythonu 2.7.6.  
PyPy je podle mě velmi zajímavý projekt. Můžeme o tom [diskutovat](http://stackoverflow.com/questions/18946662/why-shouldnt-i-use-pypy-over-cpython-if-pypy-is-6-3-times-faster), můžeme o [tom vést spory](http://stackoverflow.com/questions/2970108/pypy-what-is-all-the-buzz-about) a můžeme s tím nesouhlasit, ale to je tak všechno, co proti tomu můžeme dělat :) Samozřejmě to neznamená, že to má být od zítřka váš hlavní interpret, na to je ještě brzy. Ale sledovat se to určitě vyplatí, pokud vás Python baví.

[Kompletní zdrojový kód všech variant](https://gist.github.com/jirivrany/8704099) včetně měřící funkce je samozřejmě k dispozici.
    




        

      

