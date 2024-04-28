
class PlayerException(Exception):
    
##this is used to catch whether its a specific players turn or not.
##I have a dictionary of commands with "player" being a key. if the value is not
##either player_1 or player_2 then a dictionary exception will occur

    def __init__(self, player, message='it is not your turn yet'):
        super().__init__(message)
        self.player = player
        self.message=message

    def __str__(self):
        return f'{self.player} {self.message}'
    def wait(self):
        return f'{self.player} {self.message}'
