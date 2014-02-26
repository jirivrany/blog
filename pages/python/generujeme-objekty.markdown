#Generujeme objekty neboli object comprehension 

Python má elegantní postup pro generování objektů typu list, dictionary a set. Anglicky se mu říká list (dict, set) comprehension. Český překlad není tak docela ustálený, většinou se ale mluví o _generátoru seznamů_ nebo o _generátorové notaci seznamů_. Ten druhý překlad je podle mě maličko přesnější.

Ale ať už tomu budeme říkat tak či tak, jde o velice užitečnou věc. Vyplatí se tento postup znát a používat. Python není jediný jazyk ve kterém se tyto objektové generátory objevují. Má je například také Ruby, Lisp (a tudíž i Clojure), Haskell, Scala, Perl a další. Vesměs tedy jazyky podporující (či přímo vyžadující) funkcionální programování. 

Matematické pozadí má tento přístup v [set builder notation](http://en.wikipedia.org/wiki/Set-builder_notation). To je způsob zápisu podmínek, za kterých ze členů množiny M vytváříme členy nové množiny N.  A přesně tímto způsobem je tato notace převedena i do programovacích jazyků. Vlastně jen zaměníme jednu syntax za jinou a můžeme generovat. 

##Seznamy

Začneme seznamy, protože jejich generátorová notace je v Pythonu nejdéle. Už od verze 2.0. Jde o doporučený přístup, mimo jiné i proto, že je většinou rychlejší než alternativní formy zápisu. 
 Měl by ho znát každý, kdo to s programováním v tomto jazyce myslí vážně. 

Řekněme, že máme k dispozici seznam přirozených čísel menších než 100 a chceme z něj vytvořit seznam druhých mocnin čísel dělitelných 7. 

Zápis bude vypadat následovně :

    ::python
    cisla = [x ** 2 for x in range(1, 100) if x % 7 == 0]

Výraz v lomených závorkách začíná vzorcem pro výpočet prvků nového seznamu. Pomocí operátoru __in__ procházíme původní seznam. V tomto případě vytvořený funkcí _range_. A nakonec následuje filtrovací podmínka. 

Alternativní zápis by byl samozřejmě pomocí forcyklu na několik řádek. Pokud máme jeden list k procházení a jednu nebo žádnou podmínku, je situace jednoduchá a přehledná. Procházet můžeme krom listu i všechny ostatní iterovatelné datové typy - set, tuple, string a další.  

Když chceme filtrů nasadit více můžeme buď použít složený logický výraz, nebo prostě seřadit podmínky za sebou podle priority. To druhé v případě, že pracujeme s logickým součinem. Je to obvykle rychlejší, zejména pokud nám již první podmínka odfiltruje většinu prvků. Nebo v případě, že je filtrů více než 2 a vyhodnocení složeného výrazu tak trvá déle.  

    ::python
    [s.upper() for s in oldlist if s[0] == 'm' and s[-1] == 's']

    [s.upper() for s in oldlist if s[0] == 'm' if s[-1] == 's']

Co v případě vnořených for cyklů? Tady se občas trochu tápe. Ale stačí si pamatovat, že nejprve zapisujeme vnější cyklus a až pak vnitřní. Vnitřní cyklus je tudíž až na konci celého zápisu. 

Jednoduchý příklad kombinace dvou řetězců. Nejprve pomocí vnořených cyklů.

    ::python
    res = []
    for k in 'abc':
        for j in 'def':
            res.append(k+j)

Generátorová notace - pamatujte, že vnitřní cyklus nakonec.
    
    ::python
    res = [p + q for p in 'abc' for q in 'def']

Výsledek bude v obou případech stejný seznam ['ad', 'ae', 'af', 'bd', 'be', 'bf', 'cd', 'ce', 'cf']. Tento kartézský součin bychom samozřejmě mohli vygenerovat i jinak, například pomocí funce _product()_ z modulu _itertools_.    
      
##Slovníky

Od Pythonu 2.7 máme k dispozici stejný princip také pro vytváření slovníků. Logika věci je stejná, rozdíl je pouze v syntaxi zápisu. 
Řekněme, že potřebujeme vytvořit slovník, ve kterém klíčem budou slova převedená na malá písmena a hodnotou bude délka příslušného slova. Výchozí množinou je nějaký list slov, získaný třeba při zpracování www stránky. 

    ::python
    delky = {x.lower():len(x) for x in words}

Stručné, přehledné. Syntaxe je stejná jako při zápisu slovníku, rozdíl je pouze v dynamickém generování klíčů i hodnot.    

##Množiny

Zbývají nám množiny. Matematicky vzato je samozřejmě množinou i seznam. Datový typ __set__ je ale speciální a velice užitečný datový typ. Jde vlastně o slovník bez hodnot - pouze s klíči. Stejně jako klíče ve slovníku musí být totiž i prvky množiny unikátní. Takže i syntaxe pro generování množin je stejná jako v případě slovníku. Jen si odpustíme dvojtečku a hodnotu. 

V případě, že jsou v původním objektu nějaké duplicitní hodnoty, do nové množiny se uloží pouze jednou. To ale platí i v případě, že množinu vytvoříme pomocí built-in funkce _set_. 

Vygenerujeme tedy stejná čísla jako v prvním příkladu, ale tentokrát bude výsledný typ set. Ten se vyplatí používat vždy, když budeme v datech chtít opakovaně něco vyhledávat. Na rozdíl od listu ale nemá definované uspořádání.

    cisla = {x ** 2 for x in range(1, 100) if x % 7 == 0} 
