from abc import ABC, abstractmethod


class SuperWin(ABC):

    @abstractmethod
    def up_input(self):
        self.up_input()

    @abstractmethod
    def left_input(self):
        self.left_input()

    @abstractmethod
    def right_input(self):
        self.right_input()

    @abstractmethod
    def down_input(self):
        self.down_input()

    @abstractmethod
    def click_input(self):
        self.click_input()

    @abstractmethod
    def flag_input(self):
        self.flag_input()

    @abstractmethod
    def reset_input(self):
        self.reset_input()

    @abstractmethod
    def exit_input(self):
        self.exit_input()
