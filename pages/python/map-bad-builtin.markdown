#Map - bad builtin?

Funkce **map**, **reduce** a **filter** jsou důležité stavební prvky funkcionálních programů. Má je i Python i když samozřejmě nejde o čistě funkcionální jazyk.

Jenomže, když některou z těchto funkcí použijeme [Pylint](http://www.pylint.org/) nám zobrazí varování. Prý jde o použití nevhodné built-in funkce. Konkrétně W0141 - _Used builtin function 'map' (bad-builtin)_. Jak velká chyba je použití těchto funkcí? Je opravdu hodně nevýhodné oproti forcyklu nebo generátoru seznamů?

##Jednou větou

Pro složitější výpočty nebo větší data jsou tyto funkce v Pythonu o něco pomalejší než doporučovaná alternativa. Deprecated ale rozhodně nejsou, historie šla zkrátka jiným směrem. A v některých jednoduchých případech je použití funkce map dokonce nejrychlejší kód. Jestli vás zajímá jak a proč, čtěte dál.

##K čemu jsou vlastně map, reduce a filter?

Začněme funkcí **map**. Tu používáme vždy, když chceme na všechny prvky nějakého seznamu (či jiného iterátoru) aplikovat nějakou jinou funkci. Například, chceme všechny čísla zkonvertovat na řetězec. Klasický imperativní přístup je přes forcyklus:

    :::python        
    cisla = [10, 20, 30]
    znaky = []
    for cis in cisla:
        znaky.append(str(cis))

Stejný výsledek dostaneme také pomocí **generátoru seznamů**, což je způsob v Pythonu preferovaný a doporučovaný.
    
    :::python        
    cisla = [10, 20, 30]
    znaky = [str(cis) for cis in cisla]
    
Kód je kratší, pokud znáte syntax tak i přehlednější. A také běží rychleji. Ještě kratší zápis je v tomto případě použití funkce map.

    :::python        
    cisla = [10, 20, 30]
    znaky = map(str, cisla)

Funkce **filter** má stejně jako map svou funkcionalitu už v názvu. Umožňuje nám vybrat z původní množiny jen určité hodnoty. Například vypsat pouze ta, která jsou dělitelná 20:

    :::python        
    cisla = [10, 20, 30]
    result = []
    for cis in cisla:
        if cis % 20 == 0:
          result.append(str(cis))

List generátor bude opět kratší. 

    :::python        
    cisla = [10, 20, 30]
    result = [cis for cis in cisla if cis % 20 == 0]
    
A konečně filter, pro který ale budeme potřebovat nějakou funkci. Tu si můžeme definovat předem a nebo můžeme použít lambda funkci.    

    :::python        
    cisla = [10, 20, 30]
    result = filter(lambda x: x % 20 == 0, cisla)

Zbývá nám **reduce**. Ta umožňuje zredukovat původní seznam, většinou na jednu hodnotu. Například součin či součet původního listu. Generátor seznamů využít nemůžeme, protože jeho výsledkem je opět list. Proto je preferovný Python zápis v tomto případě forcyklus.

    :::python        
    cisla = [10, 20, 30]
    soucin = 1
    for cis in cisla:
        soucin *= cis

Reduce funkce nám vytvoří stejný výsledek takto:
    
    :::python        
    from operator import mul
    cisla = [10, 20, 30]
    soucin = reduce(mul, cisla)

A nebo můžeme použít lambda funkci:
    
    :::python        
    cisla = [10, 20, 30]
    soucin = reduce(lambda x,y:x*y, cisla)
   
Tak a můžeme se pomalu přesunout k tomu, proč vlastně jsou tyhle funkce na černé listině. 

##Jak to bylo a jak to je?

Všechny tři funkce se běžně používají v LISPu. Odtud je někdo přepsal i do Pythonu. Už v roce 2005 ale Guido Van Rossum napsal článek o tom, že v Pythonu 3 tyto funkce nebudou. Jmenuje se [The fate of reduce() in Python 3000](http://www.artima.com/weblogs/viewpost.jsp?thread=98196). Je v něm hodně výhrad k těmto funkcím a dost důvodů proč měly být z Pythonu vyřazeny. Ale už v úvodu Guido naznačuje, že čeká značné negativní ohlasy. 

Čas šel jak šel, *map* i *filter* jsou stále součástí built-in prostoru a to i v Pythonu 3.4. Rozdíl je ten, že nevracejí *list* ale *generátor*. I *reduce* zůstala, jen je v přesunutá do balíčku *functools*. Ani [PEP8](http://www.python.org/dev/peps/pep-0008/) neříká nic o tom, že by použití těchto funkcí nebyl dobrý coding style. Jen Pylint si stále vede svou. 

##Co je nejrychlejší?

Jedním z důvodů proč jsou generátory seznamů doporučovaný zápis je právě jejich rychlost. Ale v praxi samozřejmě záleží na konkrétní úloze a nemusí to platit vždy. Nejprve zkusme jednoduchý převod všech slov na VELKÁ PÍSMENA. 

    :::python  
    def listcompr(oldlist):
        return [s.upper() for s in oldlist]

    def mapfce(oldlist):
        return map(str.upper, oldlist)

    def forloop(oldlist):
        newlist = []
        for word in oldlist:
            newlist.append(word.upper())
        return newlist

Při jednoduchém benchmarku pomocí modulu timeit kdy každou funkci voláme 10x na list o 1100000 prvků je funkce map dokonce nejrychlejší, i když v Pythonu 2.7.5. není rozdíl proti list generátoru nijak dramatický. Výrazně ovšem zaostává for cyklus.

    :::bash
    Python 2.7.5
    listcompr
    1.4677 s
    mapfce
    1.4575 s
    forloop
    2.1368 s

Srovnatelných výsledků  dosáhneme i v případě podobně jednoduchých operací s čísly. Tak zkusme raději nějaké složitější počítání uvnitř mapované funkce. Třeba sha512 hash. 


    :::python
    import hashlib

    def hash_word(word):
        '''
        returns sha512 hash
        '''
        mes = hashlib.sha512()
        mes.update(word)
        return mes.hexdigest()

    def listcompr(oldlist):
        return [hash_word(s) for s in oldlist]

    def mapfce(oldlist):
        return map(hash_word, oldlist)

    def forloop(oldlist):
        newlist = []
        for word in oldlist:
            newlist.append(hash_word(word))
        return newlist

Tady už je na tom funkce map je o něco hůře. Pokud necháme vypočítat hash pro každé slovo z listu o 110000 položkách, a to opět 10x pro každou funkci, zdá se být rychlejším i klasický forcyklus. 
 
    :::bash
    Python 2.7.5.
    listcompr
    2.1001 s
    mapfce
    2.2371 s
    forloop
    2.1885 s

Poslední test - zkusíme co se stane, když vedle map použijeme ještě filter na výsledky. Třeba s trochou matematiky. Řekněme, že bychom k něčemu potřebovali vypočítat dekadické logaritmy čísel, která jsou po vynásobení pětkou dělitelná sedmi. 

    :::python
    from math import log

    def listcompr(oldlist):
        return [log(s) for s in oldlist if s * 5 % 7 == 0]

    def mapfilter(oldlist):
        return map(log, filter(lambda x: x * 5 % 7 == 0, oldlist))

    def forloop(oldlist):
        newlist = []
        for c in oldlist:
            if c * 5 % 7 == 0:
                newlist.append(log(c))
        
        return newlist

Při benchmarku pro čísla do 1 milionu a 10 opakováních je dvojice filter + map nejpomalejší. Forcyklus i generátor řeší oba výpočty v jednom průchodu listem. Naproti tomu filter při prvním průchodu vrátí nový list, na který je teprve aplikována funkce map. 

    :::bash
    Python 2.7.5.
    listcompr
    1.1560 s
    mapfilter
    1.7829 s
    forloop
    1.2487 s

##Závěr
Pro menší data jsou všechny tři přístupy rychlostně srovnatelné. List generátory jsou nejrychlejší, což se ale projeví až při větších datových objemech. Pro řadu běžných úloh bude rozdíl prakticky neměřitelný. 

Map, reduce ani filter nejsou deprecated funkce. Pylint je v tomto případě až zbytečně striktní. Všechny tři funkce jsou stále součástí built-in a nic nenasvědčuje tomu, že by měly být odstraněny.  

Také klasický forcyklus prošel zřejmě v novejších verzích Python interpretu optimalizací a je rychlostně srovnatelný s list generátorem. 

Kompletní zdrojové kódy ukázek jsou jako [obvykle k dispozici](https://gist.github.com/jirivrany/8951802).


