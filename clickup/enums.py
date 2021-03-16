from enum import Enum


class Priority(Enum):
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
    def clickup_priority_value(self):
        if self is self.urgent:
            return 1
        elif self is self.high:
            return 2
        elif self is self.normal:
            return 3
        elif self is self.low:
            return 4


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

    @property
    def preview_name(self):
        if self is self.urgent:
            return "Наивысший"
        elif self is self.high:
            return "Высокий"
        elif self is self.normal:
            return "Средний"
        elif self is self.low:
            return "Низкий"
        elif self is self.NOT_SET:
            return "Не установлено"


class Tags(Enum):
    frontend = "frontend"
    backend = "backend"
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

    @property
    def preview_name(self):
        if self is self.frontend:
            return "Клиентская разработка"
        elif self is self.backend:
            return "Серверная разработка"
        elif self is self.bug:
            return "Ошибка"
        elif self is self.supporting:
            return "Продукт | Поддержка"
        elif self is self.feature:
            return "Реализация идеи"


class Teams(Enum):
    owner = 1
    admin = 2
    member = 3
    guest = 4
    not_set = 5

    @property
    def preview_name(self):
        if self is self.owner:
            return "Управленцы"  # Переопределение значения внутри компании
        elif self is self.admin:
            return "Менеджеры"  # Переопределение значения внутри компании
        elif self is self.member:
            return "Разработчики"  # Переопределение значения внутри компании
        elif self is self.member:
            return "Гости"
        else:
            return "Не установлено"


class ClickUpEvents(Enum):
    task_assignee = "taskAssigneeUpdated"  # Обновление в назначении Исполнителя
    comment_post = "taskCommentPosted"  # Добавление комментария к задаче


class ClickUpAssigneeTypes(Enum):
    add = "assignee_add"
    remove = "assignee_rem"


class ClickUpTaskStatusType(Enum):
    done = "done"
    open = "open"

    @property
    def preview_name(self):
        if self is self.done:
            return "Выполненные"
        elif self is self.open:
            return "Открытые"
        else:
            return "Не известно"


