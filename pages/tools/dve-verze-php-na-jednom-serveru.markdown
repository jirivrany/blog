# Dvě verze PHP na jednom serveru

Vývoj jazyka PHP kráčí kupředu mílovými kroky. To je dobře, protože na PHP je
pořád ještě co vylepšovat. Jenže se díky tomu docela často stane, že aplikace
napsaná, odladěná a funkční přestane po aktualizaci PHP pracovat. Může, ale i
nemusí to být špatně napsaným kódem. To teď není tak důležité. Důležité je, že
vývojář PHP zkrátka dost často potřebuje provozovat PHP v určité konkrétní
starší verzi. Jaké má možnosti?

1. neaktualizovat PHP
2. použít nějaký server s touto verzí - nejčastěji virtuální
3. použít dvě instance web serveru, každou s jinou verzí PHP
4. použít dvě verze PHP na jedné instanci serveru
5. určitě ještě nějaké další…

Řekněme, že varianta jedna je tu opravdu jen do počtu. Pokud chcete držet krok s dobou,
musíte pracovat i s aktuální verzí jazyka, a možná spíš i s nějakou betou verze
příští.

Varianta 2. je dobrá, ale u většiny serverů a to i těch virtuálních je na ně
potřeba nějak dostat data z lokálního disku. Tedy obvykle alespoň git commit a push. 
Funkční, ale trochu pomalé. Ne každá změna kterou v kódu udělám je tak velká, aby si
zasloužila commit.

Varianta 3 funguje velmi dobře na Windows. Je to vlastně z nouze ctnost, ale
díky absenci balíčkovacího systému a nutnosti instalovat si vše ručně je velmi
snadné vzít si dvě různé verze nějakého WAMP řešení, třeba [EasyPhp](http://www.easyphp.org/) a provozovat
je vedle sebe.

Na Linuxu je vše v pořádku, pokud potřebuju jen aktuální verzi. Jakmile
potřebuju ještě nějakou další, začne být balíčkovací systém tak trochu přítěž.
Díky závislostem mezi balíčky není možné  si jen tak nainstalovat starší
PHP balíček a doufat, že to nějak bude fungovat. Nebude. Ale i tady je samozřejmě
možné nainstalovat si druhou instanci Apache a PHP, jen je potřeba použít
kompilaci zdrojových kódů, místo hotových binárek.

Není ale nutné překládat si celého Apache, dvě verze PHP (vlastně i víc) je možné
provozovat i na jednom. Postačí k tomu některé rozšiřující moduly - např.
mod_fcpgi nebo mod_fastcgi a Apache virtuální server.

## Case study - PHP 2.6.17

Zbytek článku popisuje jednu konkrétní instalaci. Píšu to hlavně proto, že
patrně budu muset za čas tyto kroky opakovat a ušetří mi to opětovné procházení
slepých uliček.  Pro jedu starší aplikaci potřebuju mít k dispozici PHP 5.2.
Aktuálně mám ale na počítači už PHP 5.5. Takže jak na to?

Základem je přeložit si příslušnou verzi PHP. Zdrojáky starších verzí jsou k
dispozici v [archivu na webu PHP](http://cz1.php.net/releases/). 
Stačí tedy najít a stáhnout co potřebuju - v mém případě 5.2.17 - poslední verzi v řadě 5.2. 

Vlastní instalace začíná konfigurací. Konfigurační script má opravdu hoooodně voleb.
Nejsnadnější způsob, jak si určit ty které jsou potřeba, je podívat se pomocí
funkce _phpinfo()_ na parametry PHP na produkčním stroji. Případně si to trochu
proškrtat o věci které bezpečně vím že nepoužívám.  Naopak je potřeba doplnit
několik důležitých voleb. Prefix - neboli adresář, do kterého se zapíše výsledek
kompilace, cestu ke konfiguračnímu souboru a konečně podporu fastcgi.

    :::bash
    ./configure --prefix=/usr/local/php52 --with-config-file-path=/etc/php52 \ 
    --with-config-file-scan-dir=/etc/php52/php.d --with-libdir=lib64 \
    --with-mysql --with-mysqli --enable-fastcgi --enable-force-cgi-redirect \
    --enable-mbstring --disable-debug --disable-rpath --with-bz2 --with-curl \
    --with-gettext --with-iconv --with-gd --with-mcrypt --with-pcre-regex --with-zlib

Podle toho jaké si vyberu technologie, jsou pro překlad potřeba různé knihovny.
Takže třeba pro knihovnu gd potřebuju balíček gd-devel a tak dále. Na Fedoře 19
je problém s balíčkem mysql-devel protože ten je v konfliktu s maria-db-devel.
Správný balík se jmenuje mysql-comunity-devel.

Další problém je s knihovnou libxml2. Ta je potřeba k překladu PHP. Problém je,
že starší verze PHP obsahují chybu, která se projeví pokud se použije libxml
2.9. a lepší. Což je samozřejmě aktuální případ. Bavíme se tu ale o 6 let starém
zdrojáku, takže na tuto chybu samozřejmě existuje [patch](https://mail.gnome.org/archives/xml/2012-August/txtbgxGXAvz4N.txt). Mám tu pro jistotu i jeho mirror.

Patch se aplikuje příkazem

    :::bash
    patch -p0 -b < php-old.patch

Pokud konfigurace proběhene v pořádku, následuje klasická mantra make, make
install. Pouštět make test asi nemá moc smysl, bavíme se tu o legacy kódu. Pokud
šlo všechno jak má, tak se v adresáři  /usr/local/php52 nachází nová instalace
starého PHP.

Dál je potřeba vytvořit adresář pro konfigurační soubor a ten do něj nahrát.
Doporučené nastavení php máme k dispozici spolu se zdrojáky.

    :::bash
    mkdir /etc/php52 cp php.ini-recommended /etc/php52/php.ini

PHP můžeme provozovat různě, ne jen přes mod_php. Právě toho využijeme a druhou
verzi proženeme přes mod_fcpgi. K tomu je potřeba nejprve vytvořit konfigurační
wrapper - soubor _/usr/local/php52/bin/fcgiwrapper.sh_ .

Měl by obsahovat toto:

    :::bash

    #!/bin/bash 
    PHP_FCGI_MAX_REQUESTS=10000 
    export PHP_FCGI_MAX_REQUESTS 
    exec /usr/local/php52/bin/php-cgi

Cíl už je na dohled. Zbývá vytvořit dva virtuální servery. Pro ně potřebujeme
DNS jména. Není ale nutné hned utíkat za správcem DNS pro vaší doménu. Pro
vývojářský stroj docela postačí lokální a testovací jména - local, localdomain,
example.com atd.. Do souboru /etc/hosts tedy můžeme napsat například tento
řádek:

    :::bash
    127.0.0.1 web1.local web2.local

Zbývá vypnout stávající konfiguraci php a fcpgi. Na Fedoře jsou konfigurační
soubory pro jednotlivé moduly v adresáři _/etc/httpd/conf.d/_ Stačí tedy ty
příslušné přejmenovat a nahradit je konfigurací virtuálních strojů. Ta moje má
podobu:

    :::bash
    #1st virtual host, use mod_php and rpm instaled php
    <VirtualHost *:80>
            ServerName web1.local
            DocumentRoot "/var/www/web1"

            <ifmodule mod_php5.c>
                    <FilesMatch \.php$>
                            AddHandler php5-script .php
                    </FilesMatch>
            </IfModule>

            <Directory "/var/www/web1">
                    DirectoryIndex index.php index.html index.htm
                    Options -Indexes
                    Order allow,deny
                    Allow from all
            </Directory>

    </VirtualHost>
    #
    #2nd virtual host, use mod_fcgid, run php-5.2
    #
    <VirtualHost *:80>
            ServerName web2.local
        DocumentRoot "/var/www/web2"
            
            <IfModule mod_fcgid.c>
                    AddHandler fcgid-script .php
                    FCGIWrapper /usr/local/php52/bin/fcgiwrapper.sh
            </IfModule>

            <Directory "/var/www/web2">
                    DirectoryIndex index.php index.html index.htm
                    Options -Indexes +ExecCGI
                    AllowOverride All
                    Order allow,deny
                    Allow from all
            </Directory>

    </VirtualHost>


Pak už stačí jen restartovat Apache a zkontrolovat že vše běží jak má. K tomu se
zase nejlépe hodí funkce _phpinfo()_, umístěná do index souborů v adresářích web1 a web2. 
Které si předtím samozřejmě vytvořím že...

Celá instalace i konfigurace se provádí pod rootem, eventuelně sudo.

Poslední zádrhel přichází už v samotné aplikaci. Nebo spíš v souboru _.htaccess_
kterým obvykle provádíme přesměrování všech requestů na front controller.
Přepisovací pravidlo musí vypada maličko jinak než obvykle:

    :::bash
    RewriteRule ^(.+)$ index.php?$0 [PT,L,QSA]

A to je vše. Existují samozřejmě i další postupy, tohle je jen jeden z mnoha.

## Zdroje
* [Install multiple version of php on one server](http://linuxplayer.org/2011/05/intall-multiple-version-of-php-on-one-server)
* [How To Use Multiple PHP Versions (PHP-FPM & FastCGI) With ISPConfig 3 (Ubuntu 12.10)](http://www.howtoforge.com/how-to-use-multiple-php-versions-php-fpm-and-fastcgi-with-ispconfig-3-ubuntu-12.10)


