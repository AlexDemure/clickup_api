from enum import Enum


class PriorityEnumsByEmoji(Enum):
    urgent = "urgent"
    high = "high"
    normal = "normal"
    low = "low"
    NOT_SET = "NOT_SET"

    @property
    def priority_value(self):
        if self is self.urgent:
            return 5
        elif self is self.high:
            return 4
        elif self is self.normal:
            return 3
        elif self is self.low:
            return 2
        elif self is self.NOT_SET:
            return 1

    @property
    def emoji(self):
        if self is self.urgent:
            return "🔴"  # Красный круг
        elif self is self.high:
            return "🟠"  # Оранжевый круг
        elif self is self.normal:
            return "🔵"  # Синий круг
        elif self is self.low:
            return "⚪️"  # Белый круг
        elif self is self.NOT_SET:
            return "❔"  # Вопросительный знак


class TagsEnumsByEmoji(Enum):
    bug = "bug"
    supporting = "supporting"
    feature = "feature"

    @property
    def priority_value(self):
        if self is self.bug:
            return 3
        elif self is self.supporting:
            return 2
        elif self is self.feature:
            return 1
        else:
            return 0

    @property
    def emoji(self):
        if self is self.bug:
            return "📛" # Пламя
        elif self is self.supporting:
            return "🔩"  # Молоток
        elif self is self.feature:
            return "💰"  # Деньги

