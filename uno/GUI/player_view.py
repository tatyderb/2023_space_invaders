from abc import ABC, abstractmethod
import pygame

from GUI.card_view import ViewCard
from GUI.config import GEOM
from card import Card
from deck import CardList
from player import Player


class ViewDeck:
    fake_card = Card('red', 0)  # нужна только для отрисовки рубашки

    def __init__(self, bounds: pygame.Rect):
        self.vc = ViewCard(ViewDeck.fake_card, bounds.x, bounds.y, face_up=False)
        self.bounds = bounds

    def draw(self, display: pygame.Surface):
        self.vc.draw(display)


class ViewHeap(ViewDeck):
    def __init__(self, top_card: Card, bounds: pygame.Rect):
        self.vc = ViewCard(top_card, bounds.x, bounds.y, face_up=True)
        self.bounds = bounds


class VPlayer(ABC):
    def __init__(self, player: Player, bounds: pygame.Rect, face_up: bool = False):
        self.player = player
        self.bounds = bounds
        x_list, y = VPlayer.place_cards(self.player.hand, bounds)
        # рука и пустое место под взятую карту
        self.hand = [ViewCard(card, x, y, face_up) for card, x in zip(self.player.hand, x_list)]
        self.hand.append(ViewCard(None, x_list[-1], y, face_up))

    def draw(self, display: pygame.Surface):
        for vc in self.hand:
            vc.draw(display)

    def get_vcard(self, pos):
        for i, cv in enumerate(self.hand):
            if cv.inside(pos):
                return cv, i
        return None, None

    @property
    def empty(self):
        return self.hand[-1]

    @staticmethod
    def place_cards(card_list: CardList, bounds: pygame.Rect):
        """ Распологает карты в рамках bounds, центрируя, расстояние между картами card_dx,
        если не влезает, то карты накладываются друг на друга.
        """
        width, height = GEOM['card']
        dx = GEOM['dx_card']
        y = bounds.y + (bounds.height // 2 - height // 2)

        amount = len(card_list) + 1
        w = amount * width + (amount - 1) * dx
        compact = w + GEOM['xgap'] * 2 > bounds.width
        if compact:
            x0 = bounds.x + GEOM['xgap']
            dw = (bounds.width - 2 * GEOM['xgap']) // amount
            x_list = [x0 + dw * i for i in range(amount)]
        else:
            x0 = bounds.x + (bounds.width // 2 - w // 2)
            x_list = [x0 + (width + dx) * i for i in range(amount)]
        return x_list, y


class VInteractivePlayer(VPlayer):
    def __init__(self, player: Player, bounds: pygame.Rect):
        super().__init__(player, bounds, face_up=True)


class VBotPlayer(VPlayer):
    pass
