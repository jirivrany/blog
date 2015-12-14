#Python Dekorátory

Dekorátory slouží k ovlivnění chování funkcí či metod, aniž bychom je přímo modifikovali. 
Klasickým příkladem je @memoize - ukládání výsledků složité funkce do memcache pro zrychlení opakovaného použití.

Pro pochopení dekorátorů potřebujete nejprve pochopit klíčové vlastnosti funkcí v Pythonu. Funkce je objekt, jako 
všechno ostatní. Proto můžete funkci přiřadit jiné jméno, předat jí jako parametr do jiné funkce, vrátit jako výsledek volání funkce a také funkce do sebe vnořovat, podobně jako třeba prvky seznamu.

Začněme jiným jménem, to je velmi jedoduché:

    :::python
    #jine jmeno pro funkci
    def clasic(words):
      freq = {}
      for word in words:
          if word in freq:
              freq[word] += 1
          else:
              freq[word] = 1

      return freq

    nove_jmeno = clasic  

Také na parametru není asi nic zásadně složitého:

    :::python
    def volany_ucastnik(param_fce): 
        print "Zrovna tvrde pracuju"
        param_fce()
        print 'uz je to udelano'

    def nejaka_jina_funkce():
        print '@TODO dulezita funkce'

    volany_ucastnik(nejaka_jina_funkce)

Proč by tedy funkce nemohla vrátit jinou funkci?:

    :::python
    def promluv(slovo, styl = 'nahlas'):
        
        def nahlas():
            return slovo.upper()+'!'
        
        def potichu():
            return slovo.lower()+'...'
        
        if (styl == 'nahlas'):
            return nahlas
        else:
            return potichu

    slovo = promluv('test')
    print slovo()

Také vnořené funkce jsou poměrně známé a nejde o žádné "Python only" specifikum: 

    :::python
    def vnejsi():
        x = 3
        def vnitrni():
            print "vnitrni tiskne poprve x : {}".format(x)
            y = x #vnitrni funkce ma pristup k hodnotam vnejsi, ale nemuze je menit!
            print "vnitrni tiskne podruhe x : {}".format(y+1)
        
        vnitrni()    
        print "vnejsi tiskne x : {}".format(x)    


    vnejsi()

Kombinací všech čtyř vlastností můžeme vytvořit funkci, která přijme **funkci jako argument**, v rámci své vnitřní funkce tento **argument zavolá** a výsledek **vrátí v podobě této vnitřní funkce**. Aby to mělo nějaký praktický význam, je volání argumentu doplněno o nějaký další kód - například ono uložení výsledku výpočtu do cache. 

Představte si tedy například funkci, která vytiskne výsledek argumentu (tedy jiné funkce) na standardní výstup a doplní ho o stručný komentář. 

    :::python
    def printer(worker):
        def wrapper(arg):
            y = worker(arg)
            print "vysledek vasi funkce je: {}".format(y)

        return wrapper

 Výsledkem funkce printer je tedy opět funkce, která vyžaduje zadání jednoho argumentu. Ten následně předává funkci worker, která ho potřebuje k výpočtu. Výsledek funkce worker se vytiskne na obrazovku hned jak je k dispozici. Funkci printer můžeme použít následovně:

    :::python
    def mocnina(x):
        return x*x

    mocnina_vystup = printer(mocnina)
    mocnina_vystup(3)    

Výsledkem volání bude "vysledek vasi funkce je: 9". Funkce mocnina tedy "najednou tiskne", i když to předtím neuměla. A to aniž bychom nějak změnili její kód. Nadále zůstává čistou funkcí bez vedlejších efektů. 

Doplnili jsme ale její chování - odekorovali jsme jí. Funkce printer je tedy dekorátor. Tento způsob volání dekorátoru není ale příliš praktický. Původní funkce dostává vlastně nové jméno, což může komplikovat čtení a hledání chyb. V případě že použíjeme zápis:

    :::python
    def mocnina(x):
        return x*x

    printer(mocnina)(3)

může být kód pro někoho ještě víc nepřehledný a složitější na pochopení. Protože Python má dobrou čitelnost kódu v základní zenové mantře, přináší pro dekorátory zjednodušenou syntaxi v podobě @decorator.  

Funkci mocnina tedy můžeme se stejným výsledkem zapsat a zavolat takto:

    :::python
    @printer
    def mocnina(x):
        return x*x

    mocnina(3)

Chování bude identické, ale zápis je stručnější a přehlednější. Navíc v tomto případě nemusíme měnit ani kód, který dekorovanou funkci volá a dekorátory tak můžeme přidávat a odebírat podle potřeby.    

Na závěr se podívejte na slibovaný dekorátor @memoize - který můžete použít pro ukládání výsledků náročných funkcí pro jejich opakované použití.

    :::python
    import functools

    def memoize(obj):
        cache = obj.cache = {}

        @functools.wraps(obj)
        def memoizer(*args, **kwargs):
            key = str(args) + str(kwargs)
            if key not in cache:
                cache[key] = obj(*args, **kwargs)
            return cache[key]
        return memoizer    
    
Funkce wraps z balíčku functools slouží pro uchování kontextu původní funkce - jména, dokumentačního řetězce a dalších. To umožňuje mimo jiné snadnější hledání případných chyb. Magické proměnné *args a **kwargs zajistí, že dekorované funkci jsou korektně předány všechny její argumenty. Dekorátor je tak univerzální.

A to je jako úvod do problematiky dekorátorů v Pythonu vše. Memoize a řadu dalších prakticky použitelných dekorátorů najdete ve wiki [PythonDecoratorLibrary](https://wiki.python.org/moin/PythonDecoratorLibrary).    
