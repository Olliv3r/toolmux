BEGIN TRANSACTION;
CREATE TABLE Tools (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        name TEXT NOT NULL,
        name_package TEXT NOT NULL,
        alias_package TEXT NOT NULL,
        link_package TEXT NOT NULL,
        category_package TEXT NOT NULL,
        dependencies_package TEXT NOT NULL,
        name_installer TEXT NULL,
        type_install TEXT NOT NULL
        );
INSERT INTO "Tools" VALUES(1,'Metasploit Framework','metasploit-framework','msfconsole','https://raw.githubusercontent.com/ivam3/termux-packages/gh-pages/ivam3-termux-packages.list','exploration tools','wget','ivam3-termux-packages.list','apt not official');
INSERT INTO "Tools" VALUES(2,'Apktool','Apktool-termux','apktool','https://github.com/h4ck3r0/Apktool-termux','reverse engineering','git','','git');
INSERT INTO "Tools" VALUES(3,'Nmap','nmap','nmap','https://github.com/nmap/nmap','information collection','libc++ liblua54 libpcap libssh2 openssl pcre resolv-conf zlib','','apt');
INSERT INTO "Tools" VALUES(4,'AcodeX','acodex-server','acodex-server','https://raw.githubusercontent.com/bajrangCoder/acode-plugin-acodex/main/installServer.sh','web applications','nodejs','installServer.sh','npm');
INSERT INTO "Tools" VALUES(5,'Data Social','dataSocial','datasocial','https://github.com/Olliv3r/dataSocial','social engineering','git','a','git');
DELETE FROM "sqlite_sequence";
INSERT INTO "sqlite_sequence" VALUES('Tools',5);
COMMIT;
