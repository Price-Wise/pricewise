import uuid


class Item:
    def __init__(self, name, price, store, url, imageURL, description):
        self.id = str(uuid.uuid4())
        self.name = name
        self.price = price
        self.store = store
        self.url = url
        self.imageURL = imageURL
        self.description = description
        self.currency = "USD"

    def __str__(self):
        return f"Item(name={self.name}, price={self.price}, store={self.store}, url={self.url}, imageURL={self.imageURL}, description={self.description})"

    def __repr__(self):
        return self.__str__()