"""Matching utils."""
import os
import json
import pickle


class ProductMatcher:
    """Match item with specific product's brand & model."""

    def __init__(self, pickle_path, skip_brands_path, normalized_brands_path):
        """Variable initialization."""
        self.pickle_path = pickle_path
        self.normalized_brands_path = normalized_brands_path

        with open(skip_brands_path, 'r') as fp:
            self.skip_data = json.load(fp)

        self.data = self.load_data()

        self.marcas_added = 0
        self.modelos_added = 0

    def load_data(self):
        """Load data from pickle file."""
        with open(self.pickle_path, 'rb') as fp:
            data = pickle.load(fp)

        return data

    def match_product(self, item):
        """Match item with a specific brand & model product."""
        item['marca'] = item['marca'].lower().strip() \
            if item['marca'] else None

        item['modelo'] = item['modelo'].lower().strip() \
            if item['modelo'] else None

        self.add_marca_modelo(item)

        if item['marca'] is None:
            item = self.match_marca(item)

        if item['modelo'] is None:
            item = self.match_modelo(item)

        if not item['marca'] or not item['modelo']:
            pass
        else:
            with open(self.normalized_brands_path, 'r') as fp:
                brands = json.load(fp)

                for normalized_brand, alternatives in brands.items():
                    if item['marca'].upper() in alternatives:
                        item['marca'] = normalized_brand.lower()
                        break

        return item

    def match_marca(self, item):
        """Try to match product's brand from it's title."""
        title = item['title']
        marcas = self.data
        marcas = filter(None, marcas)

        if title:
            for marca in sorted(marcas, key=len, reverse=True):
                if marca in title.lower():
                    item['marca'] = marca
                    return item

        return item

    def match_modelo(self, item):
        """Try to match product's model name from it's title."""
        title = item['title']

        if item['marca'] is not None:
            modelos = self.data[item['marca']]
            modelos = filter(None, modelos)

            for modelo in sorted(modelos, key=len, reverse=True):
                if modelo in title.lower():
                    item['modelo'] = modelo
                    return item

        return item

    def add_marca_modelo(self, item):
        """Add brand & model to pickle file."""
        if item['marca'] in self.skip_data['brands']:
            item['marca'] = None
            item['modelo'] = None

        if item['marca'] not in self.data:
            if item['marca'] is not None:
                self.data[item['marca']] = []
                self.marcas_added += 1

        if item['marca'] is not None:
            if item['modelo'] in self.skip_data['models']:
                item['modelo'] = None

            if item['modelo'] not in self.data[item['marca']]:
                if item['modelo'] is not None:
                    self.data[item['marca']].append(item['modelo'])
                    self.modelos_added += 1

    def save(self):
        """Save data to pickle file."""
        with open(self.pickle_path, 'wb') as fp:
            pickle.dump(self.data, fp)
