# Sculptura Tarbatum

Tartu linna skulptuuride, mälestuskivide ja mälestustahvlite loend.

Olemasolevad allikad:

* register.muinas.ee
* et.wikipedia.org/wiki/Tartu_skulptuuride_loend
* skulptuuridtartus.weebly.com
* monument.ee
* ajalooline.tartu.ee
* "Nostalgiline Tartu" FB rühm

Palju puudujääke, vähemtähtsad monumendid pole kuskil kirjaski.


Entry:
* ID 						int
* Reg Nr?					str		
* Nimi						str
* Tüüp						str/FK
* Liik						str/FK
* Aadress					str
* Arvel/registreeritud		DateTime
* Viimati nähtud			DateTime
* Koordinaadid 				str?
* Kirjeldus					str
* Galerii					Image[]
* Välislingid				str[]
* Autor						User


Image:
* ID 						int
* entry						int/FK
* orig_filename				str
* filename 					str
* URL 						str
* thumb_URL 				str
* identifier				str
* uploader					User


User:
* ID 						int
* username					str
* full_name					str
* email						str
* password_hash				str
