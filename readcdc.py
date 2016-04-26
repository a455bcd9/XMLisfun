import requests
from lxml import etree
import base64
from io import StringIO, BytesIO
import psycopg2
from datetime import datetime

# Override file's encoding
xmlparser = etree.XMLParser(encoding='UTF-8')
tree = etree.parse('example.xml', xmlparser)
root = tree.getroot()

results = root.findall('FICHE')

for result in results:
    juridiction = result.find('JURIDICTION')
    if juridiction != None:
        juridiction = juridiction.text
    else:
        juridiction = ''

    chambres_found = result.findall('CHAMBRES/CHAMBRE')
    chambres = []
    for chambre in chambres_found:
        chambres.append(chambre.text)

    reference = result.find('REFERENCE')
    if reference != None:
        reference = reference.text
    else:
        reference = ''

    numeros_rapport_found = result.findall('NUMEROS_RAPPORT/NUMERO_RAPPORT')
    numeros_rapport = []
    for numero_rapport in numeros_rapport_found:
        numeros_rapport.append(numero_rapport.text)

    numero_arpeges = result.find('NUMERO_ARPEGES')
    if numero_arpeges != None:
        numero_arpeges = numero_arpeges.text
    else:
        numero_arpeges = ''

    rapporteurs_found = result.findall('RAPPORTEURS/RAPPORTEUR')
    rapporteurs = []
    for rapporteur in rapporteurs_found:
        rapporteurs.append(rapporteur.text)

    reviseurs_found = result.findall('REVISEURS/REVISEUR')
    reviseurs = []
    for reviseur in reviseurs_found:
        reviseurs.append(reviseur.text)

    type_doc = result.find('TYPE_DOC')
    if type_doc != None:
        type_doc = type_doc.text
    else:
        type_doc = ''

    dates_seance_found = result.findall('DATES_SEANCE/DATE_SEANCE')
    dates_seance = []
    for date_seance in dates_seance_found:
        date_string = date_seance.text
        date_object = datetime.strptime(date_string, '%d/%m/%Y')
        dates_seance.append(date_object)

    date_doc = result.find('DATE_DOC')
    if date_doc != None:
        date_doc = date_doc.text
        date_doc = datetime.strptime(date_doc, '%d/%m/%Y')
    else:
        date_doc = ''

    date_lecture = result.find('DATE_LECTURE')
    if date_lecture != None:
        date_lecture = date_lecture.text
        date_lecture = datetime.strptime(date_lecture, '%d/%m/%Y')
    else:
        date_lecture = ''

    titre = result.find('TITRE')
    if titre != None:
        titre = titre.text
    else:
        titre = ''

    # URL
    ft_sfname = result.find('FT_SFNAME')
    if ft_sfname != None:
        ft_sfname = ft_sfname.text
    else:
        ft_sfname = ''

    contenu = ''
    contenu_html_64 = result.find('FT_SFNAME__CONTENU')
    if contenu_html_64 != None:
        contenu_html_iso = base64.b64decode(contenu_html_64.text).decode('ISO-8859-15')
        htmlparser = etree.HTMLParser()
        tree_html = etree.parse(StringIO(contenu_html_iso), htmlparser)
        body = tree_html.xpath('/html/body/*')

        # Get the HTML code
        for string in body:
            contenu += etree.tostring(string, pretty_print=True, method="html", encoding='UTF-8')

# Database part...
