import re
import json
from .apartment import Apartment


def extract_if_only_one_match(obj_name, article, regex):
    results = set(re.findall(regex, article))
    if len(results) == 0:
        return None
    elif len(results) == 1:
        return results.pop()
    else:
        raise ValueError(f'Multiple results in {obj_name}, please improve regex.\nresults: {results}')


def parse_conso_energetique(article):
    """
    La conso est suivi la plupart du temps de 'kwh'
    """
    conso = extract_if_only_one_match('conso energetique', article, '(\d+)\s?kwh')
    return int(conso) if conso else conso


def parse_surface(article):
    """
    Recupere la surface de l'appart comme etant la surface max trouvee.
    """
    results = set((int(x) for x in re.findall('(\d+)\s?m2', article)))
    if len(results) == 0:
        return None
    else:
        return max(results)


def parse_pieces(article):
    """
    La nb de pieces est suivi la plupart du temps de 'piece(s)'
    """
    pieces_v1 = extract_if_only_one_match('nombre pieces v1', article, '\s(\d)\s?pieces?\s')
    pieces_v2 = extract_if_only_one_match('nombre pieces v2', article, 'pieces?\s(\d)\s')
    pieces = pieces_v1 or pieces_v2
    return int(pieces) if pieces else pieces


def parse_prix(article):
    """
    La prix est suivi la plupart du temps de '€' et est compris entre 10000 et 1000000
    """
    results = set((int(x.replace(' ', '')) for x in re.findall('(\d{2,3}\s?\d{3})\s?€', article)))
    if len(results) == 0:
        return None
    else:
        return max(results)


def parse(article):
    with open('preview_before.txt', 'w') as preview:
        preview.write(article)

    normalized = article.lower()            \
                    .replace('é', 'e')      \
                    .replace('è', 'e')      \
                    .replace('²', '2')      \
                    .replace('\n', ' ')     \
                    .replace('\t', ' ')     \
                    .replace('\xa0', ' ')

    normalized = re.sub(' +', ' ', normalized)

    with open('preview.txt', 'w') as preview:
        preview.write(normalized)
    
    parse_result = {
        'prix_euros': parse_prix(normalized),
        'surface_m2': parse_surface(normalized),
        'nombre_pieces': parse_pieces(normalized),
        'conso_energetique': parse_conso_energetique(normalized),
        'parking': 'parking' in normalized,
        'garage': 'garage' in normalized
    }
    
    return parse_result

import io
from lxml import etree, html as ehtml
class PageParser:
    def __init__(self, url, body):
        self.url = url
        self.tree = self.extract_payload_tree(body)
        self.html = self.get_html_payload(self.tree)
        self.text = self.get_raw_payload(self.tree)

    def extract_payload_tree(self, body):
        """
        Extract interesting content from the whole page.
        """
        tree   = ehtml.parse(io.StringIO(body.replace('>', '> ')))
        if 'leboncoin.fr' in self.url:
            subtree = tree.xpath('//*[@id="grid"]/article')[0]
        else:
            subtree = tree.xpath('//body')[0]
        return subtree
        

    def get_html_payload(self, tree):
        """
        Convert tree content to html string
        """
        return ehtml.tostring(tree, pretty_print=True, method="html").decode('utf-8')


    def text_content(self, tag):
        try:
            return tag.text_content()
        except ValueError:
            return ' '
        

    def get_raw_payload(self, html):
        """
        Get text out of interesting content.
        """
        return ''.join(self.text_content(tag) + ' ' for tag in html)


    def text_by_xpath(self, xpath, cast=None, default=None):
        try:
            string_value = self.tree.xpath(xpath)[0].text_content()
            return string_value if cast is None else cast(string_value)
        except Exception as e:
            return default

    
    def enrich_data(self, data):
        if 'leboncoin.fr' in self.url:
            classe_energetique = self.text_by_xpath(
                '//div[@data-qa-id="criteria_item_energy_rate"]//div[contains(@class, "EnergyCriteria")]/div[contains(@class, "active")]')
            emission_ges = self.text_by_xpath('//div[@data-qa-id="criteria_item_ges"]//div[contains(@class, "EnergyCriteria")]/div[contains(@class, "active")]')[0]
            surface_m2 = extract_if_only_one_match('enrich:surface', self.text_by_xpath('//div[@data-qa-id="criteria_item_square"]'), '(\d+)\s?m')
            print('enriched surface', surface_m2)
            data['surface_m2'] = int(surface_m2)
            data['classe_energetique'] = classe_energetique.strip() if classe_energetique else 'E' # TODO: let user select default value
        return data
    

    def parse(self):
        """
        Raw parse
        """
        with open('preview.html', 'w') as preview:
            preview.write(self.html)
        data = self.enrich_data(parse(self.text))
        apart = Apartment(**data)
        print(json.dumps(apart.dump(), indent=4))
        return apart.dump()
