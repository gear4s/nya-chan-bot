from .base_query import BaseQuery
from database import Constants


class Select(BaseQuery):
    __slots__ = ('_highprio', '_all', '_distinctrow', '_straight_join', '_distinct', '_big_result', '_small_result',
                 '_buffer_result', '_calc_rows', '_group_by', '_having')

    def __init__(self, table_name, all_items=False, distinct=False, distinctrow=False, high_priority=False, limit=None,
                 order=None, where=None, items=None, straight_join=False, big=False, small=False, buffer=False,
                 calc_rows=False, group_by=False, having=False):
        super().__init__(table_name=table_name, limit=limit, order=order, where=where, items=items)

        self._highprio = high_priority
        self._straight_join = straight_join

        self._all = all_items
        self._distinct = distinct
        self._distinctrow = distinctrow

        self._big_result = big
        self._small_result = small
        self._buffer_result = buffer

        self._calc_rows = calc_rows
        self._group_by = group_by
        self._having = having

    def items(self, *args):
        self._items = args
        return self

    def limit(self, limit):
        if not isinstance(limit, int):
            return self
        self._limit = limit
        return self

    def order(self, limit):
        self._order = limit
        return self

    def where(self, *args, **kwargs):
        self._where = args, kwargs
        return self

    @property
    def all(self):
        self._all = not self._all
        self._distinct = False
        self._distinctrow = False
        return self

    @property
    def distinct(self):
        self._all = False
        self._distinct = not self._distinct
        self._distinctrow = False
        return self

    @property
    def distinctrow(self):
        self._all = False
        self._distinct = False
        self._distinctrow = not self._distinctrow
        return self

    @property
    def straight_join(self):
        self._straight_join = not self._straight_join
        return self

    @property
    def high_priority(self):
        self._highprio = not self._highprio
        return self

    @property
    def big(self):
        self._big_result = not self._big_result
        self._small_result = False
        return self

    @property
    def small(self):
        self._small_result = not self._small_result
        self._big_result = False
        return self

    @property
    def buffer(self):
        self._buffer_result = not self._buffer_result
        return self

    @property
    def calc_rows(self):
        self._calc_rows = not self._calc_rows
        return self

    def group(self, item, rollup=False):
        self._group_by = (item, rollup)
        return self

    def having(self, cond):
        self._having = cond
        return self

    @property
    def build(self):
        query = Constants.Templates.SELECT
        param_tuple = ()

        if self._all:
            modifier = "ALL "
        elif self.distinct:
            modifier = "DISTINCT "
        elif self._distinctrow:
            modifier = "DISTINCTROW "
        else:
            modifier = ""

        if self._highprio:
            modifier += "HIGH_PRIORITY "

        if self._straight_join:
            modifier += "STRAIGHT_JOIN "

        if self._big_result:
            modifier += "SQL_BIG_RESULT "
        elif self._small_result:
            modifier += "SQL_SMALL_RESULT "

        if self._buffer_result:
            modifier += "SQL_BUFFER_RESULT "

        items = "`, `".join(self._items)
        query = query.format(modifier=modifier, table=self._table_name, item=items)

        if self._where:
            where_query, where_param_tuple = self._build_where()
            query += where_query
            param_tuple += where_param_tuple

        if isinstance(self._group_by, tuple) and type(self._group_by[0]) in [tuple, str]:
            item = self._group_by[0]
            rollup = self._group_by[1]

            query += " GROUP BY "
            if isinstance(item, str):
                query += item
            else:
                query += ", ".join(item)

            if rollup:
                query += " WITH ROLLUP"

        if self._having:
            query += f" HAVING {self._having}"

        if self._order:
            token = self._order[0]
            if token not in "<=>":
                return self
            self._order = (self._order[1:], Constants.token_to_order.get(token, ""))
            query += f" ORDER BY {self._order[0]} {self._order[1]}"

        return query, param_tuple
