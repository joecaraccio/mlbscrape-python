

class Player(object):
    """ A base class for hitters and pitchers
    """
    def __init__(self, first_name, last_name, pitchfx_id, baseball_reference_id, team, hand):
        """ Constructor
        :param first_name: first name of the player
        :param last_name: last name of the player
        :param id: Pitch FX ID of the player
        :param team: team abbreviation of the player
        :param hand: the hand the player uses to play his position
        """
        self.first_name = first_name
        self.last_name = last_name
        self.pitch_fx_id = int(pitchfx_id)
        self.baseball_reference_id = baseball_reference_id
        self.team = str(team)
        self.draft_kings_points = 0
        self.playing_hand = hand

    @staticmethod
    def game_id_to_date(game_id):
        """ Extract the date from an MLB game ID
        :param game_id: the MLB game ID uniquely identifying this game
        :return: a string representing the date
        """
        game_id = str(game_id)
        date_fields = game_id.split("/")
        return str(date_fields[0] + "/" + date_fields[1] + "/" + date_fields[2])

    @staticmethod
    def inning_str_to_outs(innings):
        """ Convert innings to outs
        Note: the convention here is the typical baseball convention (i.e. 21.1 is
        21 innings and 1 out)
        :param innings: a string representation of the innings
        :return: Integer representing the amount of outs
        """
        partial_outs = int(str(innings).split(".")[1])
        whole_innings = int(str(innings).split(".")[0])
        assert partial_outs >= 0 and partial_outs < 3
        return 3*whole_innings + partial_outs

    @staticmethod
    def inning_str_to_float(innings):
        """ Convert a string representation of innings to a float representation
        Note: ex. 21.1 = 21.3333
        :param innings: a string representation of the innings
        :return: Float representing the amount of innings
        """
        partial_outs = int(str(innings).split(".")[1])
        whole_innings = int(str(innings).split(".")[0])
        return whole_innings + float(partial_outs)/3

    @staticmethod
    def era_to_er(era, innings):
        """ Convert an earned run average to the amount of earned runs
        :param era: string representation of the ERA
        :param innings: Float representation of the amount of innings
        :return: Integer representation of the earned runs
        """
        return round(float(era)*innings/9)
