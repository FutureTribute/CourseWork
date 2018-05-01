import json


class Game:
    """ Game class """
    def __init__(self, data):
        """
        :param data: dict with data about game
        """
        self.id = data["id"]  # game id in database
        self.name = data["Name"]  # game name
        self.image = data["Picture"]  # path to game image
        self.description = data["Description"]  # game description
        self.isFavorite = data["Favorite"]  # is favorite logical variable
        self.data = data  # full info


class Data:
    """Class that works with data file and contains all info about games"""
    __instance = None

    def __new__(cls):
        if Data.__instance is None:
            Data.__instance = object.__new__(cls)
        return Data.__instance

    def __init__(self):
        self.list = list()  # list for all games
        self.fullData = json.load(open("Data"))  # retrieving all games from file
        for game in self.fullData:
            # try:
            #     assert isinstance(game["id"], int) and isinstance(game["Name"], str) \
            #             and isinstance(game["Picture"], str) and isinstance(game["Description"], str) \
            #             and isinstance(game["Favorite"], bool), "Wrong data"
                self.list.append(Game(game))
            # except AssertionError:
            #     pass
        self.__gamesList = list()
        for game in self.list:
            self.__gamesList.append(game.id)

    def showFav(self):
        """
        Favorite games list
        :return: list of games
        """
        listFav = list()
        for game in self.list:
            if game.isFavorite:
                listFav.append(game)
        return listFav

    def showSearch(self, text):
        """
        List of games, that match the search query
        :param text: search string
        :return: list of games
        """
        assert isinstance(text, str), "Incorrect usage"
        text = text.lower()
        listSearch = list()
        for game in self.list:
            res = KMP(game.name.lower(), text)
            if res is not None:
                listSearch.append(game)
        return listSearch

    def addGame(self, name, desc, image):
        """
        Adds the game to the database
        :param name: game name
        :param desc: game description
        :param image: path to game image
        """
        id = max(self.__gamesList) + 1
        name = name.replace('"', '')
        desc = desc.replace('"', '')
        # for symbol_id in range(len(name)):
        #     if name[symbol_id] == '"':
        #         name[symbol_id] = ""
        # print(len(desc))
        # for symbol_id in range(len(desc)):
        #     print(symbol_id, end="")
        #     print(name[symbol_id])
        #     if name[symbol_id] == '"':
        #         name[symbol_id] = ""
        with open(image, 'rb') as f:
            bytesData = f.read()
        counter = 0
        while True:
            try:
                # filename = "images/" + name + image[-4:]
                filename = "images/{}{}.{}".format(name, counter, image[-3:])
                counter += 1
                with open(filename, "xb") as f:
                    f.write(bytesData)
                break
            except FileExistsError:
                continue
        game_dict = {"id": id, "Name": name, "Description": desc, "Picture": filename, "Favorite": False}
        self.fullData.append(game_dict)
        with open("Data", "w") as f:
            json.dump(self.fullData, f)
        self.list.append(Game(self.fullData[-1]))
        self.__gamesList.append(id)

    def gameObject(self, objId):
        """
        Looks for needed game in the list of games
        :param objId: id of the game
        :return: game object
        """
        assert isinstance(objId, int), "Incorrect usage"
        for game in self.list:
            if game.id == objId:
                return game

    def jsonUpdateFav(self, game, fav):
        """
        Updating game 'favorite' state
        :param game: game object
        :param fav: new 'favorite' state
        """
        assert isinstance(game, Game) and isinstance(fav, bool), "Incorrect usage"
        # game.data["Favorite"] = fav
        self.fullData[self.__gamesList.index(game.id)]["Favorite"] = fav
        with open("Data", "w") as f:
            json.dump(self.fullData, f)


def KMP(S, subS):
    """
    KMP algorithm
    :param S: source string
    :param subS: search query
    :return: found or not
    """
    t = [0] * len(subS)
    j = 0
    for i in range(1, len(subS)):
        while j > 0 and subS[i] != subS[j]:
            j = t[j-1]
        if subS[i] == subS[j]:
            j += 1
        t[i] = j

    m = k = 0
    while k < len(S) and m < len(subS):
        if subS[m] == S[k]:
            m += 1
            k += 1
        elif m == 0:
            k += 1
        else:
            m = t[m - 1]
    else:
        if m == len(subS):
            return k - m
        else:
            return None
