# GruntJS - nechte nudnou práci strojům

Příklad použití Grunt JS pro automatizaci rutinních činností, předvedený na
setkání vývojařů GDG SCL Liberec 5.12.2013.

## Story
Bylo nebylo Ramesh Nair sepsal docela pěknou javascriptovou kalkulačku viz. http://calc.hiddentao.com/

Na desktopu funguje bezvadně, z mobilu už je to trochu slabší, takže jsem kód trochu přepsal a ovládání pomocí
myši a klávesnice předělal na touch události. Mimo jiné.

Protože LTE datové přenosy fungují jen v reklamách a 3G sítě jen na vybraných místech v Praze, chceme mít kód na mobilním zařízení co nejmenší. Nebo alespoň já. Takže proč výsledný javascript trochu nezmenšit? A co je dneska na světě lepší pro zmenšování javascriptu, než [Google Closure compiler](https://developers.google.com/closure/compiler/?hl=cs) v advanced režimu.

Closure compiler přebírá při spouštění řadu parametrů, navíc ho budu spouštět opakovaně. To je úkol jak dělaný pro nějakého pomocníka. Kdysi jsem na to měl bat soubor ve Windows. Ale v Linuxu mi nefunguje. Asi by se na to dal napsat Bash či Python skript...

Ale kdepak. Ve světě javascriptu je dneska pomocníkem číslo jedna [GruntJS](http://gruntjs.com/ "Grunt JS").

## Začínáme

Grunt běží nad **nodeJS**, stejně jako všechny jeho pluginy. Díky tomu ho můžete použít na všech platformách, pro které existuje node.js. Pro Closure compiler potřebujeme také Javu.

Nejprve je potřeba nainstalovat Grunt klienta a to jako jako globální npm balíček. Uděláme to příkazem:

    :::bash
    npm install -g grunt-cli


Základem __gruntování__ jsou dva konfigurační soubory. _Package.json_ nám ohlídá závislosti projektu a _Gruntfile.js_ je hlavním konfiguračním souborem pro jednotlivé úkoly, které bude Grunt řešit. Package json vytvoříme v aktuálním adresáři příkazem:

    :::bash
    npm init

_Gruntfile.js_ může být prozatím prázdný, naplní ho jednotlivé úkoly. Nejprve ale potřebujeme samotný grunt-task aby je měl kdo vykonávat.

    :::bash
    npm install grunt --save-dev

Volba **_--save-dev_** je velice užitečná - do konfiguračního souboru _package.json_ nám zaregistruje závislost na Gruntjs včetně verze. Takže to nemusíme řešit ručně. Konfigurační soubor bude vypadat nějak takhle:

    :::json
    {
      "name": "simplecalc",
      "version": "0.0.1",
      "description": "simple calculator and grunt demo",
      "author": "Jiri Vrany",
      "license": "MIT",
      "devDependencies": {
        "grunt": "~0.4.2"
      }
    }

Stav projektu na začátku, včetně této konfigurace, najdete v [prvním commitu](https://github.com/jirivrany/gdgscl-grunt-demo/tree/cb973805a5ab2cc814d7be320a47c605a4d59f8b) do vzorového repozitáře. Commitoval jsem průběžně (nebo se o to aspoň snažil), takže v [historii repozitáře](https://github.com/jirivrany/gdgscl-grunt-demo/commits/master) můžete sledovat jak se jednotlivé konfigurační soubory v čase měnily.

## Nastupuje compiler
[Closure compiler task](https://github.com/gmarty/grunt-closure-compiler) pro grunt se instaluje stejně jako všechny ostatní pomocí npm. Closure compiler je potřeba si stáhnout samostatně. V konfiguračním souboru _gruntfile.js_ pak musíme nastavit správnou cestu ke kompilátoru - _closurePath_. Celý konfigurační soubor s jedním úkolem pro grunta, vypadá takhle:

    :::javascript
    module.exports = function(grunt) {

        grunt.loadNpmTasks('grunt-closure-compiler');
        
        grunt.initConfig({
            'closure-compiler': {
                frontend: {
                    closurePath: 'tools/closure',
                    js: 'app/calc.js',
                    jsOutputFile: 'dist/calc.js',
                    maxBuffer: 500,
                    options: {
                        compilation_level: 'ADVANCED_OPTIMIZATIONS',
                        language_in: 'ECMASCRIPT5_STRICT'
                    }
                }
            }
        });

        // Default task(s).
        grunt.registerTask('default', [
          'closure-compiler',
          ]);
    };

Grunt pracuje jako NodeJS modul, a celá konfigurace je uzavřena do JS funkce. Základní konfigurační direktivy jsou _loadNpmTask_ - pro načtení úlohy, _initConfig_ - pro konfigurace a _registerTask_, pro vytváření komplexnějších úloh složených z několika úkolů. Načítání jednotlivých npm lze automatizovat za pomocí package.json, ale pro začátek je to takto přehlednější.

Konfigurace je hotová, takže můžeme překládat. Pokud je soubor _calc.js_ v adresáři app správně anotovaný a přeložitelný, objeví se nám výsledek v adresáři dist. Samozřejmě, že až po té co úlohu spustíme. A protože máme registrovaný výchozí task - _default_, stačí k tomu jen příkaz:

    :::bash
    grunt


Můžeme ale pustit i konkrétní úlohu, v tomto případě tedy _closure-compiler_, víc jich zatím nemáme:

    :::bash
    grunt closure-compiler


A to je celé. Od této chvíle se zase už zase můžu měnit kód a nechat closure compiler pracovat. A nebo můžu použít grunt k tomu, abych měl té automatiky ještě trochu více.

## Další úlohy

Grunt toho umí opravdu hodně. [Pluginů](http://gruntjs.com/plugins/) pro jednotlivé úlohy bude hodně přes 100. Jen od samotných vývojářů Grunta (tzv. _contrib_ pluginů) je jich už 30. Pro daný problém - tedy mobilní aplikaci jsem v ukázce použil ještě:

* [grunt-contrib-cssmin](https://github.com/gruntjs/grunt-contrib-cssmin) pro minikaci css
* [grunt-contrib-htmlmin](https://github.com/gruntjs/grunt-contrib-htmlmin) pro minifikaci html
* [grunt-contrib-watch](https://github.com/gruntjs/grunt-contrib-watch) pro opakované spouštění úloh, pokud se změní nějaký hlídaný soubor
* [grunt-contrib-jshint](https://github.com/gruntjs/grunt-contrib-jshint)  pro statickou kontrolu javascriptu

Všechny pluginy je vhodné instalovat s přepínačem --save-dev. Všechny použité pluginy jsou vidět ve [finální verzi konfiguračního souboru](https://github.com/jirivrany/gdgscl-grunt-demo/blob/master/Gruntfile.js). A všechny  mají dobrou a přehlednou dokumentaci (chtěl jsem napsat samozřejmě, ale ono to tak samozřejmé není).

Pokud by bylo třeba, šlo by přidávat další a další pluginy. Například pro spouštění různých testů: [Mocha](https://github.com/kmiyashiro/grunt-mocha), [Jasmine](https://github.com/gruntjs/grunt-contrib-jasmine), [Qunit](https://github.com/gruntjs/grunt-contrib-qunit). [Dokonce to jde i paralelně](https://github.com/sindresorhus/grunt-concurrent). Také můžete překládat coffee script či less. No zkrátka na co si člověk vzpomene a ještě hromadu věcí o kterých možná ani neví, že existují.

Jedním z dalších plusů celého řešení je, že pokud si uděláte klon tohoto repozitáře, stačí v adresáři napsat jen:

    :::bash
    npm install

Grunt a všechny další pluginy se nainstalují tak, jak jim to určil konfigurační soubor. Stačí tedy jen přidat Closure compiler (bower task jsem pro něj zatím nenašel) a vše je připraveno k práci - na jiném počítači, u kolegy v týmu a tak dále.

Grunt je výborný nástroj, který vás odstíní od nudné a rutinní činnosti a umožní vám se soustředit na to, co je na vývoji aplikací zábavné - tedy samotné programování. Tak se nebojte a začněte __gruntovat__.

